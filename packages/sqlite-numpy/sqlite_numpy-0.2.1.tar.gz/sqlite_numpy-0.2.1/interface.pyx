# cython: language_level=3

import collections
from libc.stdlib cimport free
import time
import warnings

cimport interface

interface.initialize()


class Error(Exception):
    pass


class UnsupportedError(Error):
    pass


class ResourceClosedError(Error):
    pass


cdef exception_from_error_code(int error_code):
    if interface.INCONSISTENT_COLUMN_TYPE==error_code:
        return UnsupportedError("Column values have several types")
    elif interface.NULL_IN_INT_COLUMN==error_code:
        return UnsupportedError("NULL value in int column")

cdef class StatementProxy:
    cdef interface.sqlite3_stmt* statement

    @staticmethod
    cdef StatementProxy create(interface.sqlite3_stmt* statement):
        cdef StatementProxy proxy = StatementProxy.__new__(StatementProxy)
        proxy.statement = statement
        return proxy

    def __cinit__(self):
        self.statement = NULL

cdef class Results:
    cdef void** data
    cdef int size

    @staticmethod
    cdef Results create():
        cdef Results results = Results.__new__(Results)
        return results

    def __cinit__(self):
        self.data = NULL
        self.size = 0

    def free(self):
        free(self.data)
        self.data = NULL
        self.size = 0


cdef class ResultProxy:
    cdef Database _db
    cdef interface.Query _query
    cdef str _sql_statement

    @staticmethod
    cdef ResultProxy execute(str sql, dict bind_params, Database db):
        # Call to __new__ bypasses __init__ constructor
        cdef ResultProxy proxy = ResultProxy.__new__(ResultProxy)
        cdef int ret
        cdef bytes byte_string
        cdef const char* c_sql
        proxy._db = db
        proxy._sql_statement = sql
        interface.init(&proxy._query)
        proxy._query.statement = db._get_statement(sql)
        if proxy._query.statement == NULL:
            byte_string = sql.encode()
            c_sql = byte_string
            with nogil:
                ret = interface.prepare(db._db, &proxy._query, c_sql)
            if ret!=interface.OK:
                raise Error(f"Error while preparing query {sql}")
        for index, value in enumerate(bind_params.values()):
            if isinstance(value, int):
                ret = interface.sqlite3_bind_int64(
                    proxy._query.statement,
                    index + 1,
                    <interface.sqlite3_int64>value
                )
            elif isinstance(value, float):
                ret = interface.sqlite3_bind_double(
                    proxy._query.statement,
                    index + 1,
                    value
                )
            else:
                ret = interface.sqlite3_bind_text(
                    proxy._query.statement,
                    index + 1,
                    str(value).encode(),
                    len(value),
                    <void(*)(void *)>interface.SQLITE_TRANSIENT
                )
            if ret!=interface.OK:
                raise Error(f"Error while binding parameter '{value}'")
        with nogil:
            ret = interface.execute(db._db, &proxy._query)!=interface.OK
        if ret!=interface.OK:
            raise Error(f"Error while executing query {sql}")
        return proxy

    def __del__(self):
        self.close()

    def fetchall(self):
        cdef dict arrays = {}
        cdef int read_size
        cdef int size_increment = 100
        cdef int i
        cdef Results results = Results.create()
        if not self._query.statement:
            raise Error(f"Proxy already closed")

        try:
            read_size = self.alloc_and_read(results, size_increment)
            while read_size==size_increment:
                # exponential allocation strategy to amortize the reallocation
                size_increment = int(0.5*results.size)
                read_size = self.alloc_and_read(results, size_increment)
            # free unused memory at the end of results due to exponential memory
            # allocation strategy
            with nogil:
                results.data = interface.alloc_results(
                    &self._query,
                    results.data,
                    results.size
                )
            for i in range(self._query.column_count):
                column_name = self._query.column_names[i].decode()
                arrays[column_name] = interface.create_numpy_array(
                    results.data[i],
                    results.size,
                    self._query.column_types[i]
                )
        finally:
            results.free()
            self.close()
        return arrays

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def fetchmany(self, int count):
        cdef Results results = Results.create()
        cdef dict arrays = {}
        cdef int i
        if self.closed:
            raise ResourceClosedError(f"Proxy already closed")
        try:
            self.alloc_and_read(results, count)
            # free potential unused memory at the end of results
            with nogil:
                results.data = interface.alloc_results(
                    &self._query,
                    results.data,
                    results.size
                )
            for i in range(self._query.column_count):
                column_name = self._query.column_names[i].decode()
                arrays[column_name] = interface.create_numpy_array(
                    results.data[i],
                    results.size,
                    self._query.column_types[i]
                )
        finally:
            if results.size<count:
                self.close()
            results.free()
        return arrays

    @property
    def closed(self) -> bool:
        return self._query.column_names==NULL

    def close(self):
        interface.finalize(&self._query, 1)
        self._db._add_statement_to_cache(self._sql_statement, self._query.statement)

    cdef inline int alloc_and_read(self, Results results, int size_increment) except -1:
        cdef int read_size
        with nogil:
            results.data = interface.alloc_results(
                &self._query,
                results.data,
                results.size + size_increment
            )
        if results.data==NULL:
            raise UnsupportedError("Unknown value type in query")
        with nogil:
            read_size = interface.read_chunk(
                &self._query,
                results.data,
                results.size,
                size_increment
            )
        if read_size<0:
            interface.free_results(&self._query, results.data)
            raise exception_from_error_code(read_size)
        results.size += read_size
        return read_size


cdef class Database:
    cdef str _path
    cdef interface.sqlite3 *_db
    cdef object _statement_cache
    cdef int _max_statement_cache_size

    if interface.SQLITE_MISUSE==interface.sqlite3_config(
        interface.SQLITE_CONFIG_MULTITHREAD
    ):
        warnings.warn("Couldn't setup sqlite to multi-threaded mode")

    def __cinit__(self, path: str, max_statement_cache_size: int = 100):
        self._path = path
        self._db = NULL
        self._statement_cache = collections.OrderedDict()
        self._max_statement_cache_size = max_statement_cache_size

    def __enter__(self) -> "Database":
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def open(self) -> None:
        if interface.sqlite3_open(self._path.encode(), &self._db)!=interface.SQLITE_OK:
            raise Error(f"Error opening database file {self._path}")

    @property
    def closed(self) -> bool:
        return self._db == NULL

    def close(self) -> None:
        cdef StatementProxy proxy
        for proxy in self._statement_cache.values():
            interface.sqlite3_finalize(proxy.statement)
        self._statement_cache.clear()
        if interface.sqlite3_close(self._db)!=interface.SQLITE_OK:
            raise Error(f"Error while closing database file {self._path}")
        self._db = NULL

    def execute(self, sql_statement: str, bind_params: dict = None) -> ResultProxy:
        assert not self.closed, "Cannot execute, database has been closed"
        bind_params = bind_params or {}
        return ResultProxy.execute(sql_statement, bind_params, self)

    def load_extension(self, name: str) -> None:
        interface.sqlite3_load_extension(self._db, name.encode(), NULL, NULL)

    def statement_cache_size(self) -> int:
        return len(self._statement_cache)

    cdef _add_statement_to_cache(
        self,
        str sql_statement,
        interface.sqlite3_stmt* statement
    ):
        cdef StatementProxy proxy
        self._statement_cache[sql_statement] = StatementProxy.create(statement)
        if len(self._statement_cache)>self._max_statement_cache_size:
            oldest = next(iter(self._statement_cache))
            proxy = self._statement_cache.pop(oldest)
            interface.sqlite3_finalize(proxy.statement)

    cdef interface.sqlite3_stmt* _get_statement(self, str sql_statement):
        cdef StatementProxy proxy
        try:
            proxy = self._statement_cache[sql_statement]
            self._statement_cache.move_to_end(sql_statement)
            return proxy.statement
        except KeyError:
            return NULL
