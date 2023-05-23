import unittest

from core.encryption_controller import EncryptionController
from core.plugboard import Plugboard
from core.rotor_controller import RotorController
from core.rotor_service import RotorService
from meta.dict_object import DictObject


class EncryptionTest(unittest.IsolatedAsyncioTestCase):
    r = RotorService()
    rc = RotorController()
    pg = Plugboard()
    enc = EncryptionController()
    str = DictObject()

    async def test_2_encrypt(self):
        self.r.start()
        self.r.pre_start()
        await self.r.setup(self.str)
        self.enc.rotors = self.r
        self.enc.plugboard = self.pg
        self.str.plugboard = {'S': 'W', 'W': 'S'}
        out = await self.enc.decrypt_cmd(None, self.str, 'ABC DEF')
        # SKP
        self.assertEqual(out, (200, 'WKP TTU'))

    async def test_3_encrypt(self):
        self.r.start()
        self.r.pre_start()
        self.rc.rotor_service = self.r
        await self.r.setup(self.str)
        self.enc.rotors = self.r
        self.enc.plugboard = self.pg
        # self.str.plugboard = {'S': 'W', 'W': 'S'}
        out = await self.enc.decrypt_cmd(None, self.str, 'ABC DEF')
        # SKP
        self.assertEqual(out, (200, 'WKP TTU'))

    async def test_4_encrypt(self):
        self.r.start()
        self.r.pre_start()
        self.rc.rotor_service = self.r
        self.str = DictObject()
        await self.r.setup(self.str)
        await self.rc.rotors_set_all_cmd(None, self.str, 'Reflector B',
                                         ['Enigma M3-R3', 'Enigma M3-R2', 'Enigma M3-R1'])
        self.assertEqual(self.str, {'rotor_order': [['Enigma M3-R1', 'Enigma M3-R2', 'Enigma M3-R3'], 'Reflector B'],
                                    'rotors': {'Enigma M3-R3': 0, 'Enigma M3-R2': 0, 'Enigma M3-R1': 0},
                                    'rotorkeyring': {'Enigma M3-R3': 0, 'Enigma M3-R2': 0, 'Enigma M3-R1': 0}})

        self.enc.rotors = self.r
        self.enc.plugboard = None
        out = await self.enc.decrypt_cmd(None, self.str, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                                                         'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                                                         'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        self.assertEqual(out, (200, 'FTZMGISXIPJWGDNJJCOQTYRIGDMXFIESRWZGTOIUIEKKDCSHTPYOEPVXNHVRWWESFRUXDGWOZDM'
                                    'NKIZWNCZDUCOBLTUYHDZGOVBUYPKOJWBOWSEEMTZFWYGKODTBZDQRCZCIFDIDXCQZOOKVIIOML'))
