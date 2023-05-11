import sqlite3
from typing import Any, List

import aiosqlite

from aiosqlite import Connection, Cursor

from meta.base_module import BaseModule
from meta.decorators import instance
from meta.dict_object import DictObject


@instance("db")
class DB(BaseModule):
    # TODO: Move Database to persistent docker volume
    DB_LOCATION = "enigma.db"
    _conn: Connection

    def __init__(self):
        pass

    async def connect_db(self):
        self._conn = await aiosqlite.connect(self.DB_LOCATION)
        self._conn.row_factory = sqlite3.Row
        await self._create_table()

        # Example
        # a = await self.query_single('SELECT * FROM storage')
        # f = open('../test.json')
        # data = json.load(f)
        # datastr = json.dumps(data)
        # var = str(datastr)
        # rows = await self.exec("INSERT INTO storage(UUID, data) VALUES(?, ?)", params=[1, var])
        # a = await self.query_single('SELECT * FROM storage')

    async def _exec_wrapper(self, sql: str, params: List[Any], callback):
        cur: Cursor = await self._conn.cursor()
        string: str = sql.upper()
        try:
            if string.__contains__("UPDATE ") or string.__contains__("INSERT "):
                await cur.execute("BEGIN;")
            await cur.execute(sql, params)
            if string.__contains__("UPDATE ") or string.__contains__("INSERT "):
                await cur.execute("COMMIT;")
        except Exception as e:
            if string.__contains__("UPDATE ") or string.__contains__("INSERT "):
                await cur.execute("ROLLBACK;")
            raise Exception(f"SQL Error: '{str(e)}' for '{sql}' "
                            f"[{', '.join(map(lambda x: str(x), params))}]") from e

        result = await callback(cur)
        return result or None

    async def query_single(self, sql, params=None):
        if params is None:
            params = []

        async def map_results(cur: Cursor):
            row = await cur.fetchone()
            return DictObject(row) if row else None

        return await self._exec_wrapper(sql, params, map_results)

    async def query(self, sql, params=None) -> list[DictObject]:
        if params is None:
            params = []

        async def map_result(cur):
            return list(map(lambda row: DictObject(row), await cur.fetchall()))

        return await self._exec_wrapper(sql, params, map_result)

    async def exec(self, sql, params=None) -> int:
        if params is None:
            params = []

        async def map_result(cur):
            return [cur.rowcount, cur.lastrowid]

        row_count, lastrowid = await self._exec_wrapper(sql, params, map_result)
        self.lastrowid = lastrowid
        return row_count

    async def _create_table(self):
        sql_create_table = """ CREATE TABLE IF NOT EXISTS storage
                                (
                                    UUID integer PRIMARY KEY,
                                    data TEXT
                               ); """
        await self.exec(sql_create_table)
