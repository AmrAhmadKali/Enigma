import unittest

from core.db import DB
from meta.dict_object import DictObject


class TestDictObject(unittest.IsolatedAsyncioTestCase):
    db = DB()

    async def test_0(self):
        a = DictObject()
        a.b = 1
        a.c = {}
        a.d = [{}, {}]
        self.assertEqual(a.get_value("b"), 1)
        self.assertEqual(a.get_value("c"), {})
        self.assertEqual(a.get_value("d"), [{}, {}])
        self.assertEqual(a.b, 1)
