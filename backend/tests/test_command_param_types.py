import unittest

from core.db import DB
from meta.command_param_types import Const, Any, Int, Rotor, Reflector, Multiple, Hex


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

    async def test_hex(self):
        a = Hex('abc', is_optional=True)
        self.assertEqual(a.name, "abc")
        self.assertEqual(a.is_optional, True)
        self.assertRaises(Exception, Int, 'ab c')
        self.assertEqual(a.process_matches([None]), None)
        self.assertEqual(a.process_matches([" 0x1"]), 1)
        self.assertEqual(a.process_matches([1]), 1)
        self.assertEqual(a.get_regex(), r'(\s+(0x)?[0-9a-fA-F]+)?')

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

    async def test_rotor(self):
        a = Rotor('abc', is_optional=True)
        self.assertEqual(a.name, "abc")
        self.assertEqual(a.is_optional, True)
        self.assertRaises(Exception, Any, 'ab c')
        self.assertEqual(a.process_matches([None]), None)
        self.assertEqual(a.process_matches([" Engima I-R1"]), "Engima I-R1")
        self.assertEqual(a.get_regex(), r'(\s+Enigma .+?-R[1-8])?')

        self.assertEqual(a.get_name(), '[abc]')
        a.is_optional = False
        self.assertEqual(a.get_name(), 'abc')

    async def test_reflector(self):
        a = Reflector('abc', is_optional=True)
        self.assertEqual(a.name, "abc")
        self.assertEqual(a.is_optional, True)
        self.assertRaises(Exception, Any, 'ab c')
        self.assertEqual(a.process_matches([None]), None)
        self.assertEqual(a.process_matches([" Reflector A"]), "Reflector A")
        self.assertEqual(a.get_regex(), r'(\s+Reflector [A-Z]+?)?')

        self.assertEqual(a.get_name(), '[abc]')
        a.is_optional = False
        self.assertEqual(a.get_name(), 'abc')

    async def test_multiple(self):
        a = Multiple(Reflector('abc'))
        self.assertEqual(a.get_name(), "abc*")
        self.assertRaises(Exception, Any, 'ab c')
        self.assertEqual(["Reflector A", "Reflector C", "Reflector B"],
                         a.process_matches([" Reflector A Reflector C Reflector B", " Reflector A"]))
        self.assertEqual(a.get_regex(), r'((\s+Reflector [A-Z]+?){1,})')

        self.assertEqual(a.get_name(), 'abc*')
