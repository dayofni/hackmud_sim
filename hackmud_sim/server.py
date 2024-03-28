
import asyncio

from time import time

from hackmud_sim.db      import HackmudDatabase
from hackmud_sim.sockets import WebsocketHandler

class HackmudServer:
    
    def __init__(self) -> None:
        
        self.channels  = {}
        self.db        = HackmudDatabase()
        self.ws        = WebsocketHandler()
    
    async def __aenter__(self):
        self.db.__enter__()
        
        self.ws.set_callbacks(
            join_callback = self.websocket_join,
            msg_callback  = self.websocket_msg,
            exit_callback = self.websocket_exit
        )
        
        await self.ws.start()
        
        return self

    async def __aexit__(self, *exc):
        self.db.__exit__(*exc)
    
    # Websocket connectivity
    
    async def websocket_join(self, user):
        ...
        
    async def websocket_msg(self, user, message):
        ...
    
    async def websocket_exit(self, user):
        ...
        
    async def client_handler(self):
        ...
    
    # Message handling
    
    async def broadcast_msg(self, channels):
        ...
    
    async def send_msg(self, user):
        ...
        