
from hackmud_sim import HackmudServer

from hackmud_sim.colour.hackmud import parse_hackmud_string
from hackmud_sim.colour.data    import TEST_STRING

print(parse_hackmud_string(TEST_STRING))

"""

from time import sleep

with HackmudServer() as server:

    server.db.create_user("dayofni")
    
    print(server.db.ObjectId())
    
    sleep(5)
"""