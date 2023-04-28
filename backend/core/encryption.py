import typing

from meta.base_module import BaseModule
from meta.command_param_types import Any
from meta.decorators import instance, command

if typing.TYPE_CHECKING:
    from core.rotor_config import Rotors


@instance("encrypt")
class Encryption(BaseModule):

    def inject(self, reg):
        self.rotors: Rotors = reg.get_instance("rotors", is_optional=True)
        self.plugboard = reg.get_instance("plugboard", is_optional=True)

    # TODO: testing

    @command("encrypt", params=[Any('text_to_encrypt', allowed_chars="[a-zA-Z]")],
             description="Encrypt a given message")
    async def encrypt_cmd(self, ws, storage, encrypt_me):
        """
        :param ws: Client owning the current session which is being handled
        :param storage: Cache dedicated to the Client
        :param encrypt_me: The message which is meant to get encrypted
        :return: Status Code, Encrypted Message
        """
        out = encrypt_me
        tmp = ""
        if self.rotors:
            for k in out:
                tmp += self.rotors.encrypt(storage, k)
            out = tmp
        if self.plugboard:
            for k in out:
                tmp += self.plugboard.encrypt(storage, k)
            out = tmp
        return 200, out

    @command("decrypt", params=[Any('text_to_decrypt', allowed_chars="[a-zA-Z]")],
             description="Decrypt a given message")
    async def decrypt_cmd(self, ws, storage, decrypt_me):
        return await self.encrypt_cmd(ws, storage, decrypt_me)
