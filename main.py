
from hackmud_sim.db import HackmudDatabase

with HackmudDatabase() as db:

    db.create_user("dayofni")

    print(db.f("dayofni", {"_id": "hello_world"}, "hello"))
    
    print(db.ObjectId())