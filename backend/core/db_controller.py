import secrets
import base64
import typing
from itertools import cycle
from typing import Tuple

from websockets.legacy.server import WebSocketServerProtocol

from meta.base_module import BaseModule
from meta.command_param_types import Reflector, Multiple, Rotor, Int, Any
from meta.decorators import instance, command
from meta.dict_object import DictObject

if typing.TYPE_CHECKING:
    from core.db import DB


def _convert(uuid: str) -> str:
    base = _check_padding(uuid)
    encode = base64.urlsafe_b64decode(bytes(base, 'ascii'))
    xor = bytes([_a ^ _b for _a, _b in zip(encode, cycle(b'xAAA'))])
    return base64.urlsafe_b64encode(xor).decode('ascii')


def _check_padding(uuid: str) -> str:
    modulo = len(uuid) % 4
    return uuid if modulo == 0 else uuid + ((4 - modulo) * '=')


@instance()
class DBController(BaseModule):

    def inject(self, reg) -> None:
        self.db: DB = reg.get_instance('db')

    @command(command="uuid",
             params=[],
             description="Generates an UUID for Database and Cookie")
    async def generate_uuid(self, _: WebSocketServerProtocol, _1: DictObject) -> Tuple[int, str]:
        uuid = secrets.token_urlsafe(128)
        # await self.db.exec('INSERT INTO storage(UUID) VALUES (?)', [uuid])
        return 200, _check_padding(uuid)


'''
    @command(command="uuid",
             params=[Any('uuid')],
             description="Deletes the corresponding row from the database")
    async def delete_uuid(self, _: WebSocketServerProtocol, storage: DictObject) -> Tuple[int, str]:
'''
