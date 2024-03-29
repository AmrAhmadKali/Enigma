import asyncio
import typing
from typing import Tuple

from websockets.legacy.server import WebSocketServerProtocol

from meta.base_module import BaseModule
from meta.command_param_types import Any
from meta.decorators import instance, command
from meta.dict_object import DictObject

if typing.TYPE_CHECKING:
    from core.rotor_service import RotorService


@instance("encryption_controller")
class EncryptionController(BaseModule):

    def inject(self, reg):
        self.rotors: RotorService = reg.get_instance("rotor_service", is_optional=True)
        self.plugboard = reg.get_instance("plugboard", is_optional=True)

    # noinspection PyUnusedLocal
    @command("encrypt", params=[Any('text_to_encrypt', allowed_chars="[a-zA-Z ]")],
             description="Encrypt a given message")
    async def encrypt_cmd(self, ws: WebSocketServerProtocol, storage: DictObject, encrypt_me: str) -> Tuple[int, Any]:
        """
        This command will encrypt a message 'encrypt_me' based on parameters in 'storage'
        :param ws: Client owning the current session which is being handled
        :param storage: Cache dedicated to the Client
        :param encrypt_me: The message which is meant to get encrypted
        :return: Status Code, Encrypted Message
        """
        out = encrypt_me.upper()
        tmp = ""
        if self.plugboard:
            for k in out:
                if k == " ":
                    tmp += k
                    continue
                tmp += self.plugboard.encrypt(storage, k)
            out = tmp
            tmp = ""
            await asyncio.sleep(0)
        if self.rotors:
            for k in out:
                if k == " ":
                    tmp += k
                    continue
                tmp += self.rotors.encrypt(storage, k)
            out = tmp
            tmp = ""
            await asyncio.sleep(0)
        if self.plugboard:
            for k in out:
                if k == " ":
                    tmp += k
                    continue
                tmp += self.plugboard.encrypt(storage, k)
            out = tmp
        key = "".join(self.rotors.convert_to_str(x % 26) for x in reversed(storage.rotors.values()))
        return 200, [out, key]

    @command("decrypt", params=[Any('text_to_decrypt', allowed_chars="[a-zA-Z ]")],
             description="Decrypt a given message")
    async def decrypt_cmd(self, ws: WebSocketServerProtocol, storage: DictObject, decrypt_me: str) -> Tuple[int, Any]:
        """
        This command will decrypt a message 'decrypt_me' based on parameters in 'storage'
        :param ws: Client owning the current session which is being handled
        :param storage: Cache dedicated to the Client
        :param decrypt_me: The message which is meant to get encrypted
        :return: Status Code, Encrypted Message
        """
        return await self.encrypt_cmd(ws, storage, decrypt_me)
