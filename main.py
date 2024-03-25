
from hackmud_sim    import HackmudServer

with HackmudServer() as server:

    server.db.create_user("dayofni")
    
    print(server.db.ObjectId())