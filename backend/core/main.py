import asyncio
import json
import typing

import websockets
from websockets.exceptions import ConnectionClosedError
from websockets.legacy.server import WebSocketServerProtocol, WebSocketServer

from meta.decorators import instance
from meta.dict_object import DictObject
from meta.registry import Registry

if typing.TYPE_CHECKING:
    from core.command_service import CommandService


@instance("app")
class Server(WebSocketServer):

    def init(self, paths, reg: Registry):
        self.modules = paths
        self.registry = reg
        self.host, self.port = "0.0.0.0", 25500
        self.loop = asyncio.get_event_loop()

        self.stop = self.loop.create_future()

    def inject(self, reg):
        self.cmd_service: CommandService = reg.get_instance('command_service')

    async def startup(self):
        async with websockets.serve(self.ws_handler, self.host, self.port):
            await self.stop

    async def ws_handler(self, websocket: WebSocketServerProtocol, path):
        """
        This handler will take care of all incoming connections, and forward their commands to the correct handlers.
        :param websocket: the Client this handler has been allocated for
        :param path: Path used by the Client. Unused in this Project, would allow splitting clients based on it for other use cases.
        """
        print(f'Client connected: {websocket.id}')
        data = DictObject({'usages': 0})
        await Registry.setup_storage(data)
        try:
            async for msg in websocket:
                message = json.loads(msg)
                print(f'Received: {msg} via {path} from {websocket.id}')
                await self.cmd_service.process_command(websocket, DictObject(message), data)
        except ConnectionClosedError:
            pass
        except NameError as e:
            await self.cmd_service.reply(websocket, (500, e.args))
        print(f'Client disconnected: {websocket.id}')
