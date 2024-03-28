
import asyncio
import websockets.exceptions

from secrets import token_hex
from typing  import Callable

from websockets.server import serve

class WebsocketHandler:
    
    def __init__(self):
        
        self.callbacks = {
            "join": None,
            "msg":  None,
            "exit": None
        }
        
        self.sockets = {}
        self.ws      = False
    
    def set_callbacks(self, join_callback: Callable, msg_callback: Callable, exit_callback: Callable) -> None:
        
        """
        Sets a callback for when a message arrives in a socket.
        """
        
        self.callbacks = {
            "join": join_callback,
            "msg":  msg_callback,
            "exit": exit_callback
        }
        
    async def start(self, port: int = 8765) -> None:
        
        assert all(list(self.callbacks.values())), "Callback function missing."
        assert not self.ws,                        "Websocket already running."
        assert type(port) == int,                  "Port needs to be an int."
        
        self.ws = asyncio.create_task(self.socket_task(port=port))
        
    async def socket_task(self, port: int = 8765) -> None:
        
        async with serve(self.client_handler, "localhost", port):
            await asyncio.Future()
            
    async def client_handler(self, websocket, _):
        
        user_id = token_hex(32)
        
        self.sockets[user_id] = websocket     # keep a running tally
        await self.callbacks["join"](user_id) # run callback
        
        try:
            
            async for message in websocket:
                await self.callbacks["msg"](user_id, message) # new message, run callback
            
            self.sockets.pop(user_id)             # user's gone
            await self.callbacks["exit"](user_id) # run callback
        
        except websockets.exceptions.ConnectionClosedError: # not sure if this is necessary

            self.sockets.pop(user_id)
            await self.callbacks["exit"](user_id)
    
    async def send_msg(self, user: str, msg: str) -> None:
        
        websocket = self.sockets[user]
        await websocket.send(msg)
    
    async def broadcast_msg(self, users: list[str], msg: str) -> None:
        
        websockets = [self.sockets[user] for user in users]
        
        for ws in websockets:
            await ws.send(msg)