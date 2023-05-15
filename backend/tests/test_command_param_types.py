import unittest

from core.db import DB
from meta.command_param_types import Const, Any, Int


class TestCommandParams(unittest.IsolatedAsyncioTestCase):
    db = DB()

    async def test_const(self):
        a = Const('abc', is_optional=True)
        self.assertEqual(a.name, "abc")
        self.assertEqual(a.is_optional, True)
        self.assertRaises(Exception, Const, 'ab c')
        self.assertEqual(a.process_matches([None]), None)
        self.assertEqual(a.process_matches([" a"]), "a")
        self.assertEqual(a.get_regex(), r'(\s+abc)?')
        self.assertEqual(a.get_name(), '[abc]')
        a.is_optional = False
        self.assertEqual(a.get_name(), 'abc')

    async def test_int(self):
        a = Int('abc', is_optional=True)
        self.assertEqual(a.name, "abc")
        self.assertEqual(a.is_optional, True)
        self.assertRaises(Exception, Int, 'ab c')
        self.assertEqual(a.process_matches([None]), None)
        self.assertEqual(a.process_matches([" 1"]), 1)
        self.assertEqual(a.process_matches([1]), 1)
        self.assertEqual(a.get_regex(), r'(\s+[0-9]+)?')

        self.assertEqual(a.get_name(), '[abc]')
        a.is_optional = False
        self.assertEqual(a.get_name(), 'abc')

    async def test_any(self):
        a = Any('abc', is_optional=True)
        self.assertEqual(a.name, "abc")
        self.assertEqual(a.is_optional, True)
        self.assertRaises(Exception, Any, 'ab c')
        self.assertEqual(a.process_matches([None]), None)
        self.assertEqual(a.process_matches([" a"]), "a")
        self.assertEqual(a.get_regex(), r'(\s+.+?)?')

        self.assertEqual(a.get_name(), '[abc]')
        a.is_optional = False
        self.assertEqual(a.get_name(), 'abc')
