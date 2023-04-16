import asyncio
import json

import websockets
from websockets.exceptions import InvalidStatusCode, ConnectionClosedOK
from websockets.legacy.client import WebSocketClientProtocol


# Run this little program to spam the Websocket with different
# commands for testing where the WebUI is not implemented yet;
# Adjust the function `internal` accordingly.


class WebsocketClient:

    async def internal(self, uri):
        try:
            async with websockets.connect(uri) as websocket:
                websocket: WebSocketClientProtocol
                await websocket.send(json.dumps({'cmd': 'help'}))
                print(await websocket.recv())
                await websocket.send(json.dumps({'cmd': 'set', 'sub_cmd': "rotor", 'params': [5]}))
                print(await websocket.recv())
                await websocket.send(json.dumps({'cmd': 'set', 'sub_cmd': "rotor", 'params': [5, "string"]}))
                print(await websocket.recv())
                await websocket.send(json.dumps({'cmd': 'set', 'sub_cmd': "rotor", 'params': [5, "str"]}))
                print(await websocket.recv())
        except ConnectionClosedOK:
            return
        except websockets.exceptions.ConnectionClosedError:
            return

    async def monitor(self, uri, method):
        # Auto reconnect
        while True:
            try:
                await method(uri)
                await asyncio.sleep(10)
            except Exception:
                pass

    def __init__(self):
        loop = asyncio.get_event_loop()
        b = loop.create_task(self.monitor("ws://localhost:25500/internal", self.internal))
        loop.run_until_complete(b)


WebsocketClient()
