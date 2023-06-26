import json
import time
import typing
import uuid
from typing import Tuple

from websockets.legacy.server import WebSocketServerProtocol

from meta.base_module import BaseModule
from meta.command_param_types import Hex
from meta.decorators import instance, command
from meta.dict_object import DictObject

if typing.TYPE_CHECKING:
    from core.db import DB


@instance()
class DBController(BaseModule):
    bitmask = 2 ** 63 - 1
    def inject(self, reg) -> None:
        self.db: DB = reg.get_instance('db')

    @command(command="save",
             params=[],
             description="Save the current backend state into the DB")
    async def save(self, _: WebSocketServerProtocol, _1: DictObject) -> Tuple[int, str]:
        """
        Generates a UUID, which gets linked to a copy of the current connection-storage.
        May be loaded again by using load <key> - where <key> is the response of this command.
        """
        uid = uuid.uuid4().int & self.bitmask
        timeout = time.time()
        await self.db.exec('DELETE FROM storage WHERE timeout <?', [timeout])
        while await self.db.query('SELECT "" from storage where UUID=? and timeout < ?', [uid, timeout]):
            uid = uuid.uuid4().int & self.bitmask
        await self.db.exec('INSERT INTO storage(UUID, data, timeout) VALUES (?, ?, ?)',
                           [uid, json.dumps(_1), time.time() + 7 * 24 * 60 * 60])
        return 200, hex(uid ^ self.bitmask)

    @command(command="load",
             params=[Hex('uuid')],
             description="Load backend settings from a given UUID")
    async def load(self, _: WebSocketServerProtocol, storage: DictObject, uid) -> Tuple[int, str]:
        """
        Loads the Storage which was previously saved with "save"
        """
        data = await self.db.query_single('SELECT data FROM storage where UUID=? and timeout > ?',
                                          [uid ^ self.bitmask, time.time()])
        if not data:
            return 400, "There's no Save stored matching this UUID"
        storage.update(json.loads(data.data))
        return 200, "Preset loaded!"
