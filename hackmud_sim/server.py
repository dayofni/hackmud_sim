
import asyncio

from time    import time
from secrets import token_hex

from websockets.server      import serve

from hackmud_sim.db import HackmudDatabase

class HackmudServer:
    
    def __init__(self) -> None:
        
        self.clients  = {}
        
        self.channels = {}
        self.db       = HackmudDatabase()
    
    def __enter__(self):
        self.db.__enter__()
        return self

    def __exit__(self, *exc):
        self.db.__exit__(*exc)
    
    # Websocket connectivity
    
    async def start_server(self):
        ...
    
    async def start_websocket(self):
        ...
        
    async def client_handler(self):
        ...
    
    # Message handling
    
    async def broadcast_msg(self, channels):
        ...
    
    async def send_msg(self, user):
        ...