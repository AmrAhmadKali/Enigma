import unittest

from core.rotor_controller import RotorController
from core.rotor_service import RotorService
from meta.dict_object import DictObject


class PlugboardTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.rs = RotorService()
        self.rc = RotorController()
        self.str = DictObject()
        self.rc.rotor_service = self.rs
        self.rs.start()

    async def test_0_help(self):
        code, resp = await self.rc.rotors_help_cmd(None, None)
        self.assertEqual(code, 200)
        for rotor in ['Enigma I-R1', 'Enigma I-R2', 'Enigma I-R3', 'Enigma I-R4', 'Enigma I-R5',
                      'Enigma B-R1', 'Enigma B-R2', 'Enigma B-R3', 'Enigma M3-R1', 'Enigma M3-R2',
                      'Enigma M3-R3', 'Enigma M3-R4', 'Enigma M3-R5', 'Enigma M3-R6', 'Enigma M3-R7',
                      'Enigma M3-R8']:
            self.assertIn(rotor, resp)

    async def test_1_set_all(self):
        storage = DictObject()
        code, resp = await self.rc.rotors_set_all_cmd(None, storage, 'Reflector A',
                                                      ['Enigma I-R1', 'Enigma I-R3', 'Enigma I-R2'])
        self.assertEqual(code, 200)
        self.assertEqual(storage, {'rotor_order': [['Enigma I-R2', 'Enigma I-R3', 'Enigma I-R1'], 'Reflector A'],
                                   'rotors': {'Enigma I-R2': 0, 'Enigma I-R3': 0, 'Enigma I-R1': 0},
                                   'rotorkeyring': {'Enigma I-R2': 0, 'Enigma I-R3': 0, 'Enigma I-R1': 0}})

        code, resp = await self.rc.rotors_set_all_cmd(None, storage, 'Reflector X',
                                                      ['Enigma I-R1', 'Enigma I-R3', 'Enigma I-R2'])
        self.assertEqual(code, 400)
        self.assertEqual(storage, {'rotor_order': [['Enigma I-R2', 'Enigma I-R3', 'Enigma I-R1'], 'Reflector A'],
                                   'rotors': {'Enigma I-R2': 0, 'Enigma I-R3': 0, 'Enigma I-R1': 0},
                                   'rotorkeyring': {'Enigma I-R2': 0, 'Enigma I-R3': 0, 'Enigma I-R1': 0}})

        code, resp = await self.rc.rotors_set_all_cmd(None, storage, 'Reflector A',
                                                      ['Enigma I-R9', 'Enigma I-R3', 'Enigma I-R2'])
        self.assertEqual(code, 400)
        self.assertEqual(storage, {'rotor_order': [['Enigma I-R2', 'Enigma I-R3', 'Enigma I-R1'], 'Reflector A'],
                                   'rotors': {'Enigma I-R2': 0, 'Enigma I-R3': 0, 'Enigma I-R1': 0},
                                   'rotorkeyring': {'Enigma I-R2': 0, 'Enigma I-R3': 0, 'Enigma I-R1': 0}})

    async def test_2_set_reflector(self):
        storage = DictObject({'rotor_order': [['Enigma I-R2', 'Enigma I-R3', 'Enigma I-R1'], 'Reflector B'],
                              'rotors': {'Enigma I-R2': 1, 'Enigma I-R3': 2, 'Enigma I-R1': 3}})
        code, resp = await self.rc.reflector_set_cmd(None, storage, None)
        self.assertEqual(code, 200)
        self.assertIn('Reflector A', resp)

        code, resp = await self.rc.reflector_set_cmd(None, storage, 'Reflector A')
        self.assertEqual(code, 200)
        self.assertEqual(storage, {'rotor_order': [['Enigma I-R2', 'Enigma I-R3', 'Enigma I-R1'], 'Reflector A'],
                                   'rotors': {'Enigma I-R2': 0, 'Enigma I-R3': 0, 'Enigma I-R1': 0},
                                   'rotorkeyring': {'Enigma I-R2': 0, 'Enigma I-R3': 0, 'Enigma I-R1': 0}})

        code, resp = await self.rc.reflector_set_cmd(None, storage, 'Reflector X')
        self.assertEqual(code, 400)

    async def test_3_set_rotor_id(self):
        storage = DictObject({'rotor_order': [['Enigma I-R2', 'Enigma I-R3', 'Enigma I-R1'], 'Reflector A'],
                              'rotors': {'Enigma I-R2': 0, 'Enigma I-R3': 0, 'Enigma I-R1': 0}})
        code, resp = await self.rc.rotors_set_single_cmd(None, storage, 1, 'Enigma I-R9')
        self.assertEqual(code, 400)

        code, resp = await self.rc.rotors_set_single_cmd(None, storage, 9, 'Enigma I-R1')
        self.assertEqual(code, 400)

        code, resp = await self.rc.rotors_set_single_cmd(None, storage, 1, 'Enigma I-R5')
        self.assertEqual(code, 200)
        self.assertEqual(storage, {'rotor_order': [['Enigma I-R2', 'Enigma I-R5', 'Enigma I-R1'], 'Reflector A'],
                                   'rotors': {'Enigma I-R2': 0, 'Enigma I-R5': 0, 'Enigma I-R1': 0},
                                   'rotorkeyring': {'Enigma I-R2': 0, 'Enigma I-R5': 0, 'Enigma I-R1': 0}})

    async def test_4_offset_single(self):
        storage = DictObject({'rotor_order': [['Enigma I-R2', 'Enigma I-R3', 'Enigma I-R1'], 'Reflector A'],
                              'rotors': {'Enigma I-R2': 0, 'Enigma I-R3': 0, 'Enigma I-R1': 0}})
        code, resp = await self.rc.rotors_offset_single_cmd(None, storage, 9, 'A')
        self.assertEqual(code, 400)

        code, resp = await self.rc.rotors_offset_single_cmd(None, storage, 1, 'AA')
        self.assertEqual(code, 400)

        code, resp = await self.rc.rotors_offset_single_cmd(None, storage, 1, 'Z')
        self.assertEqual(code, 200)
        self.assertEqual(storage.rotors,
                         {'Enigma I-R2': 0, 'Enigma I-R3': self.rs.convert_to_int('Z')[0], 'Enigma I-R1': 0})

    async def test_5_offset_all(self):
        storage = DictObject({'rotor_order': [['Enigma I-R2', 'Enigma I-R3', 'Enigma I-R1'], 'Reflector A'],
                              'rotors': {'Enigma I-R2': 9, 'Enigma I-R3': 7, 'Enigma I-R1': 3}})
        code, resp = await self.rc.rotors_offset_all_cmd(None, storage, 'ABCD')
        self.assertEqual(code, 400)

        code, resp = await self.rc.rotors_offset_all_cmd(None, storage, 'AAA')
        self.assertEqual(code, 200)
        self.assertEqual(storage.rotors, {'Enigma I-R2': 0, 'Enigma I-R3': 0, 'Enigma I-R1': 0})

        code, resp = await self.rc.rotors_offset_all_cmd(None, storage, 'BCD')
        self.assertEqual(code, 200)
        self.assertEqual(storage.rotors, {'Enigma I-R2': 3, 'Enigma I-R3': 2, 'Enigma I-R1': 1})
