import unittest

from core.db import DB


class TestDB(unittest.IsolatedAsyncioTestCase):
    db = DB()

    async def test_0_connect(self):
        test_uuid = 'INIyvPrPseLxlT9yvfAJTjR-k8_O71jrVR8noBpHg1OzApO3su4SXSafnVpes3fawfmDDrZkRbQT' \
                    'c9LFiO4-eRp_q7WY60ZX4TAFrRqywYWjgznOxxxHjpkZPboQBufNz5hrpBG_al6NELVRpByS7l2_' \
                    'VfjffyrPYx8kGPw2bnA='
        test_uuid2 = 'UKj9_S6f3us9iT5vA6Jf8T5L84QX8e7nCu_H7IwuOezmlU49PhJAiVVSCZ_pSQohye-3LCcwVOV' \
                     '26-4TjoiYhu5tEZ-9MuGQTMek6AQenhsAkGcXOfWLqYUxAKa-eM1EemGARPtKqCUPTWC4hIkYiA' \
                     'EhgdZY00HSeHFNv3HvXNs='

        try:
            # return
            await self.db.connect_db(':memory:')
            t_exec = await self.db.exec('INSERT INTO storage(UUID, data) VALUES(?, ?)', [test_uuid, 'data'])
            t_exec2 = await self.db.exec('INSERT INTO storage(UUID, data) VALUES(?, ?)', [test_uuid2, 'data2'])
            self.assertEqual(t_exec, t_exec2, -1)

            with self.assertRaises(Exception):
                await self.db.exec('INSERT INTO storage(UUID, data) VALUES(?, ?)', [test_uuid2, 'data3'])
            self.assertEqual(await self.db.query('SELECT * FROM storage where UUID=?', [test_uuid]),
                             [{'UUID': test_uuid, 'data': 'data'}])
            self.assertEqual(await self.db.query('SELECT * FROM storage'),
                             [{'UUID': test_uuid, 'data': 'data'}, {'UUID': test_uuid2, 'data': 'data2'}])
            self.assertEqual(await self.db.query_single('SELECT * FROM storage'), {'UUID': test_uuid, 'data': 'data'})
        except Exception as e:
            self.fail(e)
        finally:
            await self.db._conn.close()
