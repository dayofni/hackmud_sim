
import pymongo

from subprocess import Popen
from os         import makedirs
from os.path    import exists, dirname, join, isdir, realpath

from typing import Any, Optional, Union

class HackmudDatabase:
    
    def __init__(self, db_path=None, host="localhost", port=1337) -> None:
        
        self.mongo_server = None
        self.db_path      = db_path
        self.host         = host
        self.port         = port     # heh l337 5p34k makes a comeback
    
    def __enter__(self):
        
        #! Step 1: Load hackmud database
        #! Steo 2: Start client.
        
        self.start_mongodb(self.db_path, self.port)
        self.start_client(self.host, self.port)
        
        return self

    def __exit__(self, *exc: Any) -> None:
        
        print("\n\n\nkilled the MongoDB server\n\n\n")
        
        self.mongo_server.terminate() # kill the server
    
    def start_mongodb(self, db_path: Optional[str], port: int) -> None:
        
        current_dir = dirname(realpath(__file__))
        
        # set it to be hackmud_sim/db/data, get absolute path
        
        if not db_path:
            db_path = join(current_dir, "data")
        
        # check to see if the data folder exists
        # if not, create it
        
        if not exists(db_path):
            makedirs(db_path)
        
        # run mongod commands and init the database
        
        command = " ".join([join(current_dir, "mongod"), f"--dbpath {db_path}", f"--port {port}"])
        self.mongo_server = Popen(command)
    
    def start_client(self, host: str, port: int) -> None:
        
        self.client = pymongo.MongoClient(host, port)
        
        # Set up the DB.
        
        self.player_db   = self.client["databases"]
        self.player_data = self.client["player_data"]
        self.scripts     = self.client["scripts"]
        
        self.users = {}
    
    def create_user(self, user: str) -> None:
        
        assert user not in self.users, f"User {user} already exists!"
        
        # Creates a user using the db
        
        self.users[user] = {
            "#db":     self.player_db[user],
            "data":    self.player_data[user],
            "scripts": self.scripts[user]
        }
    
    def i(self, user, data: Union[Any, list[Any]]) -> None:
        
        if (type(data) not in [list, tuple]):
            self.users[user]["#db"].insert_one(data)
        
        else:
            self.users[user]["#db"].insert_many(data)
        
        print(self.users[user]["#db"])
    
    def f(self, user): ...
    
    def r(self, user): ...
    
    def u(self, user): ...
    
    def u1(self, user): ...
    
    def us(self, user): ...

    # go through upload comms from game and add them here
    
    # edit
    # dir
    # up (delete public private shift)
    # down
    # DELETE
    # scripts
    #
    #help