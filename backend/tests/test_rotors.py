import unittest

from core.rotor_config import Rotors
from meta.dict_object import DictObject


class PlugboardTest(unittest.IsolatedAsyncioTestCase):
    r = Rotors()
    str = DictObject()

    async def test_0_setup(self):
        await self.r.setup(self.str)
        self.assertEqual(self.str, {'rotor_order': [
            ['Enigma I-R3', 'Enigma I-R2', 'Enigma I-R1'],
            'Reflector A'],
            'rotors': {'Enigma I-R3': 0,
                       'Enigma I-R2': 0,
                       'Enigma I-R1': 0}})

    async def test_1_rotation(self):
        # 21
        self.r.start()
        self.r._perform_rotate(self.str)
        self.assertEqual(self.str.rotors['Enigma I-R3'], 1)

        self.r._rotate(self.str, 'Enigma I-R3', 20)
        self.r._perform_rotate(self.str)
        self.assertEqual(self.str.rotors['Enigma I-R1'], 0)
        self.assertEqual(self.str.rotors['Enigma I-R2'], 1)
        self.assertEqual(self.str.rotors['Enigma I-R3'], 22)

        self.r._rotate(self.str, 'Enigma I-R2', 3)
        self.r._rotate(self.str, 'Enigma I-R3', 25)
        self.r._perform_rotate(self.str)
        self.assertEqual(self.str.rotors['Enigma I-R1'], 1)
        self.assertEqual(self.str.rotors['Enigma I-R2'], 5)
        self.assertEqual(self.str.rotors['Enigma I-R3'], 48)

        self.r._rotate(self.str, 'Enigma I-R2', 25)
        self.r._perform_rotate(self.str)
        self.assertEqual(self.str.rotors['Enigma I-R1'], 2)
        self.assertEqual(self.str.rotors['Enigma I-R2'], 31)
        self.assertEqual(self.str.rotors['Enigma I-R3'], 49)

    async def test_2_encrypt(self):
        self.r.start()
        await self.r.setup(self.str)
        self.assertEqual(self.r.encrypt(self.str, 'A'), 'S')
        self.assertEqual(self.r.encrypt(self.str, 'X'), 'U')
