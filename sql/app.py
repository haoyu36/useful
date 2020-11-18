# -*- coding: utf-8 -*-

import pymysql


HOST = 'localhost'
PORT = 3306
USER = 'web'
PASSWORD = '123456'
DB = 'movies'


class Database:
    _cursor = None

    def __init__(self, charset='utf8', autocommit=True):
        self.conn = pymysql.connect(
                host=HOST, user=USER,
                port=PORT, password=PASSWORD,
                db=DB, charset='utf8')
        self.conn.autocommit(autocommit)
        self.uri = f'mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'

    def __repr__(self):
        return f'<Database {self.uri}>'

    def close(self):
        self.conn.close()

    def _execute(self, query, raw=True, *args, **kwargs):
        cursor_cls = None if raw else pymysql.cursors.SSDictCursor
        if self._cursor is not None:
            self._cursor.close()
        self._cursor = cursor = self.conn.cursor(cursor_cls)
        err = None
        try:
            cursor.execute(query, args, **kwargs)
        except pymysql.err.DatabaseError as e:
            err = e
            self.conn.rollback()
        else:
            return cursor

        if err is not None:
            self._cursor.close()
            self.close()
            raise err

    def _normalize_where_query(self, dct):
        return ' AND'.join(f'{k}="{v}"' for k, v in dct.items())

    def insert(self, table, data):
        keys = ','.join(data)
        values = ','.join(['%s'] * len(data))
        sql = f'INSERT INTO {table}({keys}) VALUES({values})'
        cursor = self._execute(sql, True, *data.values())
        return cursor.lastrowid

    def insertmany(self, table ,keys, items):
        assert isinstance(keys, list)
        values = ','.join(['%s'] * len(keys))
        sql = f'INSERT INTO {table}({",".join(keys)}) VALUES({values})'
        cursor = self.conn.cursor()
        try:
            return cursor.executemany(sql, items)
        except pymysql.err.DatabaseError:
            self.close()
            raise

    def query(self, sql, raw=False, **kwargs):
        cursor = self._execute(sql, raw=raw, **kwargs)
        if raw:
            return cursor.fetchall()
        # return (Row(row) for row in cursor)

    def update(self, table, data, where=None, force=False):
        assert where is not None or force
        query = ','.join(f'{k}="{v}"' for k, v in data.items())
        sql = f'UPDATE {table} SET {query}'

        if where and len(where):
            query = self._normalize_where_query(where)
            sql += f' WHERE {query}'
        cursor = self._execute(sql)
        return cursor.rowcount

    def delete(self, table, where=None, force=False):
        assert  where is not None or force
        sql = f'DELETE FROM {table}'

        if where and len(where):
            query = self._normalize_where_query(where)
            sql += f' WHERE {query}'

        cursor = self._execute(sql)
        return cursor.rowcount

    def select(self, table, fields='*', where=None, order=None, start=0,
               limit=None):
        sql = f"SELECT {','.join(fields)} FROM `{table}`"

        if where and len(where):
            query = self._normalize_where_query(where)
            sql = f'{sql} WHERE {query}'

        if order is not None:
            sql += f' ORDER BY {order}'

        if limit:
            sql += f' LIMIT {start}, {limit}'

        cursor = self._execute(sql, raw=False)
        return (Row(row) for row in cursor)



class Row(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    def __repr__(self):
        repr_string = ','.join(f'{k}={v}' for index, (k, v) in enumerate(
            self.items()) if index < 3)

        if len(self) > 3:
            repr_string += '...'

        return f'<{self.__class__.__name__} {repr_string}>'
