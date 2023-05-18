import unittest

from core.db import DB


class TestDB(unittest.IsolatedAsyncioTestCase):
    db = DB()

    async def test_0_connect(self):
        try:
            # return
            await self.db.connect_db(':memory:')
            t_exec = await self.db.exec('INSERT INTO storage(UUID, data) VALUES(?, ?)', [1, 'data'])
            t_exec2 = await self.db.exec('INSERT INTO storage(UUID, data) VALUES(?, ?)', [2, 'data2'])
            self.assertEqual(t_exec, t_exec2, -1)

            with self.assertRaises(Exception):
                await self.db.exec('INSERT INTO storage(UUID, data) VALUES(?, ?)', [2, 'data3'])
            self.assertEqual(await self.db.query('SELECT * FROM storage where UUID=?', [1]),
                             [{'UUID': 1, 'data': 'data'}])
            self.assertEqual(await self.db.query('SELECT * FROM storage'),
                             [{'UUID': 1, 'data': 'data'}, {'UUID': 2, 'data': 'data2'}])
            self.assertEqual(await self.db.query_single('SELECT * FROM storage'), {'UUID': 1, 'data': 'data'})
        except Exception as e:
            self.fail(e)
        finally:
            await self.db._conn.close()
