
import asyncio

from time import sleep

from hackmud_sim                import HackmudServer
from hackmud_sim.logger         import setup_logger
from hackmud_sim.colour.hackmud import parse_hackmud_string
from hackmud_sim.colour.data    import TEST_STRING

print(parse_hackmud_string(TEST_STRING))


async def main():
    
    setup_logger()
    
    async with HackmudServer() as server:

        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())