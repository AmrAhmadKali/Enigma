import json
import unittest

from core.command_service import CommandService
from core.db import DB
from core.db_controller import DBController
from core.encryption_controller import EncryptionController
from core.help_controller import HelpController
from core.main import Server
from core.plugboard import Plugboard
from core.rotor_controller import RotorController
from core.rotor_service import RotorService
from meta.dict_object import DictObject
from meta.registry import Registry


class InitTest(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        # First of all, we need to check if the code would even run, prior to testing it..
        self.reg = Registry()
        self.reg.add_instance('app', Server(), True)
        self.reg.add_instance('help', HelpController(), True)
        db = DB()
        self.reg.add_instance('db', db, True)
        await db.connect_db(":memory:")
        self.reg.add_instance('encryption_controller', EncryptionController(), True)
        self.reg.add_instance('rotor_service', RotorService(), True)
        self.reg.add_instance('rotor_controller', RotorController(), True)
        self.reg.add_instance('command_service', CommandService(), True)
        self.reg.add_instance('plugboard', Plugboard(), True)
        self.reg.add_instance('db_controller', DBController(), True)
        app: Server = self.reg.get_instance("app")
        self.reg.load_instances(["core"])
        app.init(["core"], self.reg)

        self.reg.inject_all()
        self.reg.pre_start_all()
        self.reg.start_all()
        self.cs: CommandService = self.reg.get_instance('command_service', True)
        self.cli = self.WebSocketclient()
        self.storage = DictObject({'usages': 0})
        await self.reg.setup_storage(self.storage)

    async def test_0_int(self):
        await self.cs.process_command(self.cli, DictObject({'cmd': 'encrypt', 'params': 'G'}), self.storage)  #
        self.assertEqual(self.cli.abc.status, 200)
        self.assertEqual(self.cli.abc.response, ['U', 'AAB'])
        self.assertEqual(self.storage.usages, 1)

        await self.cs.process_command(self.cli, DictObject({'cmd': 'plugboard', 'sub_cmd': 'set', 'params': 'UB'}),
                                      self.storage)  #
        await self.cs.process_command(self.cli, DictObject({'cmd': 'encrypt', 'params': 'G'}), self.storage)  #
        self.assertEqual(self.cli.abc.status, 200)
        self.assertEqual(self.cli.abc.response, ['I', 'AAC'])
        self.assertEqual(self.storage.usages, 3)

        await self.cs.process_command(self.cli, DictObject(
            {'cmd': 'rotors', 'sub_cmd': 'set', 'params': 'Reflector C Enigma M3-R5 Enigma I-R2 Enigma M3-R8'}),
                                      self.storage)  #
        await self.cs.process_command(self.cli, DictObject({'cmd': 'encrypt', 'params': 'AAAAA' * 16}), self.storage)  #
        self.assertEqual(self.cli.abc.status, 200)
        a = self.cli.abc.response[0]
        await self.cs.process_command(self.cli, DictObject(
            {'cmd': 'rotors', 'sub_cmd': 'set', 'params': 'Reflector C Enigma M3-R5 Enigma I-R2 Enigma M3-R8'}),
                                      self.storage)  #
        await self.cs.process_command(self.cli, DictObject({'cmd': 'encrypt', 'params': a}), self.storage)  #
        self.assertEqual(self.cli.abc.response, ['AAAAA' * 16, 'BHC'])
        self.assertEqual(self.storage.usages, 7)

        await self.cs.process_command(self.cli, DictObject({'cmd': 'rotors', 'sub_cmd': 'offset', 'params': 'CDG'}),
                                      self.storage)  #
        await self.cs.process_command(self.cli, DictObject({'cmd': 'rotors', 'sub_cmd': 'ringoffset', 'params': 'FGU'}),
                                      self.storage)  #
        await self.cs.process_command(self.cli, DictObject({'cmd': 'encrypt', 'params': 'AAAAA' * 16}), self.storage)  #
        self.assertEqual(self.cli.abc.status, 200)
        a = self.cli.abc.response[0]

        await self.cs.process_command(self.cli, DictObject({'cmd': 'rotors', 'sub_cmd': 'offset', 'params': 'CDG'}),
                                      self.storage)  #
        await self.cs.process_command(self.cli, DictObject({'cmd': 'rotors', 'sub_cmd': 'ringoffset', 'params': 'FGU'}),
                                      self.storage)  #
        await self.cs.process_command(self.cli, DictObject({'cmd': 'encrypt', 'params': a}), self.storage)  #
        self.assertEqual(self.cli.abc.response, ['AAAAA' * 16, 'DKI'])
        self.assertEqual(self.storage.usages, 13)

        await self.cs.process_command(self.cli, DictObject(
            {'cmd': 'rotors', 'sub_cmd': 'set', 'params': 'Reflector C Enigma I-R2 Enigma M3-R8'}), self.storage)  #
        await self.cs.process_command(self.cli, DictObject({'cmd': 'encrypt', 'params': 'AAAAA' * 16}), self.storage)  #
        self.assertEqual(self.cli.abc.status, 200)
        a = self.cli.abc.response[0]
        await self.cs.process_command(self.cli, DictObject({'cmd': 'save'}), self.storage)  #
        b = self.cli.abc.response
        await self.cs.process_command(self.cli, DictObject(
            {'cmd': 'rotors', 'sub_cmd': 'set', 'params': 'Reflector C Enigma I-R2 Enigma M3-R8'}), self.storage)  #
        await self.cs.process_command(self.cli, DictObject({'cmd': 'encrypt', 'params': a}), self.storage)  #
        self.assertEqual(self.cli.abc.response, ['AAAAA' * 16, 'HC'])

        await self.cs.process_command(self.cli, DictObject({'cmd': 'load', 'params': b}), self.storage)  #
        self.assertEqual(self.cli.abc.status, 200)

        await self.cs.process_command(self.cli, DictObject({'cmd': 'encrypt', 'params': a}), self.storage)  #
        self.assertNotEqual(self.cli.abc.response, ['AAAAA' * 16, 'HC'])
        await self.cs.process_command(self.cli, DictObject({'cmd': 'dump'}), self.storage)  #
        self.assertEqual(self.cli.abc.response,
                         {'plugboard': {'B': 'U', 'U': 'B'},
                          'rotor_order': [['Enigma M3-R8', 'Enigma I-R2'], 'Reflector C'],
                          'rotorkeyring': {'Enigma I-R2': 0, 'Enigma M3-R8': 0},
                          'rotors': {'Enigma I-R2': 13, 'Enigma M3-R8': 160}, 'usages': 18})
        self.assertEqual(self.storage.usages, 18)

    class WebSocketclient:
        abc = ""

        async def send(self, msg):
            self.abc = DictObject(json.loads(msg))

    async def asyncTearDown(self) -> None:
        db: DB = self.reg.get_instance('db')
        await db._conn.close()
