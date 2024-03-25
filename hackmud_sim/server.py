
import asyncio

from hackmud_sim.db import HackmudDatabase

class HackmudServer:
    
    def __init__(self) -> None:
        
        self.channels = {}
        self.users    = ...
        self.db       = HackmudDatabase()
    
    def __enter__(self):
        self.db.__enter__()
        return self

    def __exit__(self, *exc):
        self.db.__exit__(*exc)
    
    async def main():
        
        while True: # while true, do nothing. we do not wish to do anything.
            pass