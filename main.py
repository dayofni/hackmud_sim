
from hackmud_sim import HackmudServer

from time import sleep

with HackmudServer() as server:

    server.db.create_user("dayofni")
    
    print(server.db.ObjectId())
    
    sleep(5)