
import asyncio
import re

from time import time as unix_secs # yeah look I probably shouldn't rename it but ya know it's fine

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
        
        self.clients      = {}
        self.users        = {}
        self.channels     = {"0000": []}
    
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
        
    # Users
    
    def create_user(self, user):
        
        self.users[user] = {
            "channels": [
                "0000"
            ]
        }
        
        self.channels["0000"].append(user)
        
    
    def delete_user(self, user):
        ...
    
    # Channel list
    
    def create_channel(self, channel_name):
        
        self.channels[channel_name] = []
    
    def join_channel(self, user, channel_name):
        
        self.users[user]["channels"].append(channel_name)
        self.channels[channel_name].append(user)
    
    def leave_channel(self, user, channel_name):
        ...
    
    # Websocket connectivity
    
    async def websocket_join(self, user):
        self.users[user] = {"channels": "0000"}
        self.channels["0000"].append(user)
        
    async def websocket_msg(self, user, message):
        
        # commands
        # - sub <channel>
        # - unsub
        # - join
        # -  create
        # - standard (send message to 0000)
        
        command = message.split()[0]
        if command not in ["sub", "unsub", "create"]:
            command = "send"
        else:
            message = message.split(" ")[1:]
        
        if command == "sub":
            
        
        ...
    
    async def websocket_exit(self, user):
        ...
    
    # Message handling
    
    async def broadcast_msg(self, channels):
        
        # determine what users to broadcast to
        
        await self.ws.broadcast_msg()
    
    async def send_msg(self, user):
        
        await self.ws.send_msg()