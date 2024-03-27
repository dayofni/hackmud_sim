
from time import sleep

from hackmud_sim                import HackmudServer
from hackmud_sim.colour.hackmud import parse_hackmud_string
from hackmud_sim.colour.data    import TEST_STRING

print(parse_hackmud_string(TEST_STRING))

"""
with HackmudServer() as server:

    server.db.create_user("chandrian")
    server.db.update_script("chandrian", "blue_flame", "function(c, a){#ns.sys.breach()}")
    
    server.db.get_script("chandrian", "blue_flame")
    
    while True:
        ...
"""
