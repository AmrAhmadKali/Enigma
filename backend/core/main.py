import asyncio
import json

import websockets
from websockets.exceptions import ConnectionClosedError
from websockets.legacy.server import WebSocketServerProtocol, WebSocketServer

from meta.decorators import instance
from meta.registry import Registry


@instance("app")
class Server(WebSocketServer):

    def init(self, paths, reg: Registry):
        self.modules = paths
        self.registry = reg
        self.host, self.port = "0.0.0.0", 25500
        self.loop = asyncio.get_event_loop()

        self.stop = self.loop.create_future()

    def startup(self):
        self.loop.run_until_complete(self.server())

    async def process_request(self, path, request_headers):
        print(path, request_headers)

    async def server(self):
        async with websockets.serve(self.ws_handler, self.host, self.port):
            await self.stop

    async def ws_handler(self, websocket: WebSocketServerProtocol, path):
        data = {}  # save client data in here
        try:
            async for msg in websocket:
                data = json.loads(msg)
                print(f'Received: {msg} via {path} from {websocket.id}')
                await websocket.send(msg)
        except ConnectionClosedError:
            pass
