
from hackmud_sim.db import HackmudDatabase

with HackmudDatabase() as db:

    db.create_user("dayofni")
    
    print(db.ObjectId())