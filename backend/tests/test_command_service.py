import json
import typing
import unittest
from functools import partial

from core.command_service import CommandService
from core.db import DB
from core.encryption_controller import EncryptionController
from core.help_controller import HelpController
from core.main import Server
from core.rotor_controller import RotorController
from core.rotor_service import RotorService
from meta.command_param_types import Any
from meta.dict_object import DictObject
from meta.registry import Registry


class InitTest(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        # First of all, we need to check if the code would even run, prior to testing it..
        typing.TYPE_CHECKING = True
        self.reg = Registry()
        HelpController()
        DB()
        EncryptionController()
        RotorService()
        RotorController()
        CommandService()
        app: Server = self.reg.get_instance("app")
        self.reg.load_instances(["core"])
        app.init(["core"], self.reg)

        self.reg.inject_all()
        self.reg.pre_start_all()
        self.reg.start_all()

    async def test_0_init(self):
        d = DictObject()
        await self.reg.setup_storage(d)
        self.assertNotEqual(d, {})

    class WebSockClient:
        abc = ""

        async def send(self, msg):
            self.abc = DictObject(json.loads(msg))

    async def test_2_command_handler(self):
        cs: CommandService = self.reg.get_instance('command_service', True)

        cli = self.WebSockClient()
        storage = DictObject({'usages': 0})
        await cs.process_command(cli, DictObject({'cmd': 'help'}), storage)
        self.assertEqual(cli.abc.status, 200)
        self.assertEqual(storage.usages, 1)

        await cs.process_command(cli, DictObject({'cmd': '12'}), storage)
        self.assertEqual(cli.abc.status, 404)

        await cs.process_command(cli, DictObject({'cmd': '12', 'params': "abcdef"}), storage)
        self.assertEqual(cli.abc.status, 404)

    async def test_3_reply(self):
        cs: CommandService = self.reg.get_instance('command_service', True)
        cli = self.WebSockClient()
        await cs.reply(cli, 200)
        self.assertEqual(cli.abc, {'status': 200})

    async def test_4_register(self):
        async def mocked_cmd(_, _1):
            pass

        cs: CommandService = self.reg.get_instance('command_service', True)
        rdn = partial(cs.register, mocked_cmd, 'abc', params=[Any('None')],
                      description="Random Test Command",
                      module='core.test',
                      sub_command='def')
        self.assertRaises(Exception, rdn)

    async def test_5_reg(self):
        self.assertEqual(self.reg.get_module_name(HelpController), "core.help_controller")

    async def test_6_reg(self):
        self.assertNotEqual(self.reg._registry, {})
        self.reg.clear()
        self.assertEqual(self.reg._registry, {})
        self.assertRaises(Exception, self.reg.get_instance, 'abc')
        self.reg.add_instance('test', self)
        self.assertRaises(Exception, self.reg.add_instance, "test", self)

        self.assertRaises(Exception, self.reg.add_instance, "aa", self, True)
