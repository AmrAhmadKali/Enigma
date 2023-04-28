import asyncio
import json
import random

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
                await websocket.send(json.dumps({'cmd': 'dump'}))
                await websocket.recv()

                # print(await websocket.recv())
                translate = random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10)
                translate = "".join(translate)
                print(f"Sending Translate Request for: {translate}")
                await websocket.send(json.dumps({'cmd': "encrypt", 'params': [translate]}))
                d = await websocket.recv()
                d = json.loads(d)
                print(f"Received: {d['response']}.. Requesting decryption")
                await websocket.send(json.dumps({'cmd': 'decrypt', 'params': [d['response']]}))
                # print(d := json.loads(await websocket.recv()))
                d = json.loads(await websocket.recv())
                print(
                    f"Received: {d['response']}.. This is {'' if d['response'] == translate else '**NOT** '}the original message")
                # await websocket.send(json.dumps({'cmd': 'set', 'sub_cmd': "rotor", 'params': [5, "str"]}))
                # print(await websocket.recv())
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
