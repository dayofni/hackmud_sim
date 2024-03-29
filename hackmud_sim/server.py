
import asyncio

from time import time as unix_secs # yeah look I probably shouldn't do this but it's *very useful*

from hackmud_sim.db      import HackmudDatabase
from hackmud_sim.sockets import WebsocketHandler
from hackmud_sim.logger  import setup_logger

class Client:
    ...

class HackmudServer:
    
    def __init__(self) -> None:
        
        self.db      = HackmudDatabase()
        self.ws      = WebsocketHandler()
        self.logger  = setup_logger(name=__name__)
        
        self.clients  = {}
        self.users    = {}
        self.channels = {}
    
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
        
        msg = f"{user[:4]}: {message}"
        await self.ws.broadcast_msg(list(self.ws.sockets.keys()), msg)
        
        self.logger.info(msg)
    
    async def websocket_exit(self, user):
        ...
    
    # Message handling
    
    async def broadcast_msg(self, channels):
        
        # determine what users to broadcast to
        
        await self.ws.broadcast_msg()
    
    async def send_msg(self, user):
        
        await self.ws.send_msg()