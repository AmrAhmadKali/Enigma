import unittest

from core.db import DB
from core.db_controller import DBController
from meta.dict_object import DictObject


class TestDB(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.db = DB()
        self.dbc: DBController = DBController()
        self.dbc.db = self.db
        await self.db.connect_db(':memory:')

    async def test_0_save(self):
        try:
            data = {"rotor": "ABC"}
            code, reason = await self.dbc.save(None, DictObject(data))
            self.assertEqual(code, 200)

            code2, reason2 = await self.dbc.save(None, DictObject(data))
            self.assertEqual(code2, 200)
            storage = DictObject()
            code, reason = await self.dbc.load(None, storage, 1)
            self.assertEqual(code, 400)
            self.assertNotEquals(storage, data)

            code, reason = await self.dbc.load(None, storage, int(reason2, 16))
            self.assertEqual(code, 200)
            self.assertEqual(storage, data)
        except Exception as e:
            raise e
        finally:
            await self.db._conn.close()

    async def tearDown(self) -> None:
        await self.db._conn.close()
