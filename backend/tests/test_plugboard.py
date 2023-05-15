import unittest

from core.plugboard import Plugboard
from meta.dict_object import DictObject


class PlugboardTest(unittest.IsolatedAsyncioTestCase):
    pg = Plugboard()

    async def test_setup(self):
        d = DictObject()
        await self.pg.setup(d)
        self.assertEqual(d.plugboard, {})

    async def test_pb_set_cmd(self):
        d = DictObject()
        await self.pg.setup(d)

        t1 = await self.pg.pb_set_cmd(None, d, 'AB')
        self.assertEqual(t1, 200)
        t2 = await self.pg.pb_set_cmd(None, d, 'BC')
        self.assertEqual(t2[0], 300)
        t3 = await self.pg.pb_set_cmd(None, d, 'BCD')
        self.assertEqual(t3[0], 400)
        t4 = await self.pg.pb_set_cmd(None, d, '123')
        self.assertEqual(t4[0], 400)
        t5 = await self.pg.pb_set_cmd(None, d, 'BCDE')
        self.assertEqual(t5[0], 300)
        t6 = await self.pg.pb_set_cmd(None, d, 'BCDE')
        self.assertEqual(t6[0], 300)
        t7 = await self.pg.pb_set_cmd(None, d, '13')
        self.assertEqual(t7[0], 400)
        t8 = await self.pg.pb_set_cmd(None, d, 'CB')
        self.assertEqual(t8[0], 300)

        self.assertEqual(d, {'plugboard': {'A': 'B', 'B': 'A'}})
        t9 = await self.pg.pb_set_cmd(None, d, 'AB')
        self.assertEqual(t9, 200)
        self.assertEqual(d, {'plugboard': {}})
        await self.pg.pb_set_cmd(None, d, 'AB')
        t10 = await self.pg.pb_reset_cmd(None, d)
        self.assertEqual(t10, 200)
        self.assertEqual(d, {'plugboard': {}})
