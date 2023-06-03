import os
import time
import unittest

from core.db import DB


class TestDB(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.db = DB()
        await self.db.connect_db(':memory:')

    async def test_0_connect(self):

        try:
            test_uuid = int.from_bytes(os.urandom(4), "big")
            test_uuid2 = int.from_bytes(os.urandom(4), "little")
            timestamp = time.time()
            # return
            t_exec = await self.db.exec('INSERT INTO storage(UUID, data, timeout) VALUES(?, ?, ?)',
                                        [test_uuid, 'data', timestamp])
            t_exec2 = await self.db.exec('INSERT INTO storage(UUID, data, timeout) VALUES(?, ?, ?)',
                                         [test_uuid2, 'data2', timestamp])
            self.assertEqual(t_exec, t_exec2, -1)
            with self.assertRaises(Exception):
                await self.db.exec('INSERT INTO storage(UUID, data, timestamp) VALUES(?, ?, ?)',
                                   [test_uuid2, 'data3', timestamp])
            self.assertEqual(await self.db.query('SELECT * FROM storage where UUID=?', [test_uuid]),
                             [{'UUID': test_uuid, 'data': 'data', 'timeout': timestamp}])
            self.assertEqual(await self.db.query('SELECT * FROM storage'),
                             [{'UUID': test_uuid, 'data': 'data', 'timeout': timestamp},
                              {'UUID': test_uuid2, 'data': 'data2', 'timeout': timestamp}])
            self.assertEqual(await self.db.query_single('SELECT * FROM storage'),
                             {'UUID': test_uuid, 'data': 'data', 'timeout': timestamp})
        except Exception as e:
            raise e
        finally:
            await self.db._conn.close()
