
import pymongo
import pymongo.results

from bson import ObjectId

from subprocess import Popen
from os         import makedirs, getcwd
from os.path    import exists, dirname, join, realpath
from time       import time
from typing     import Any, Callable, Optional, Union

class HackmudCursorWrapper:
    
    """
    Incomplete. Only using array and first for now.
    
    I'm fairly certain JSON only allows dict[str, Any]
    """
    
    def __init__(self, cursor) -> None:
        self.cursor = cursor
    
    def first(self) -> dict[str, Any]: # HIGHLY INEFFICIENT
        return list(self.cursor)[0]
        
    def array(self) -> list[dict[str, Any]]:
        return list(self.cursor)
        
    def count(self) -> int:
        ...
    
    def each(self, function: Callable):
        ...
        
    def distinct(self, key):
        ...
        
    def sort(self):
        ...
        
    def skip(self, num: int): # incomplete
        self.cursor.skip(num)
        
    def limit(self, num: int): # incomplete
        self.cursor.limit(num)
        
    def close(self): # incomplete
        self.cursor.close()


class HackmudDatabase:
    
    def __init__(self, db_path=None, port=1337) -> None:
        
        assert type(port) == int, "Port needs to be an int."
        
        self.mongo_server = None
        self.db_path      = db_path
        self.host         = "localhost", 
        self.port         = port     # 1337 game, dude
        
        self.mongo_out = None
    
    def __enter__(self):
        
        #! Step 1: Load MongoDB
        #! Steo 2: Start client.
        
        self.start_mongodb(self.db_path, self.port)
        self.start_client(self.host, self.port)
        
        return self

    def __exit__(self, *exc: Any) -> None:
        self.mongo_server.terminate() # kill the server
        self.mongo_out.close()
    
    def start_mongodb(self, db_path: Optional[str], port: int) -> None:
        
        current_dir = dirname(realpath(__file__))
        
        # set it to be hackmud_sim/db/data, get absolute path
        
        if not db_path:
            db_path = join(current_dir, "data")
        
        # check to see if the data folder exists
        # if not, create it
        
        if not exists(db_path):
            makedirs(db_path)
        
        # Create steam to pipe cmd to
            
        self.mongo_out = open(join(getcwd(), "mongodb_server.log"), "w")
        
        # run mongod commands and init the database
        
        command = " ".join([join(current_dir, "mongod"), f"--dbpath {db_path}", f"--port {port}"])
        
        self.mongo_server = Popen(command, stdout=self.mongo_out)
    
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
    
    def i(self, user, data: Union[dict[str, Any], list[dict[str, Any]]]) -> None:
        
        if (type(data) not in [list, tuple]):
            mdb_result = self.users[user]["#db"].insert_one(data)
        
        else:
            mdb_result = self.users[user]["#db"].insert_many(data)
        
        if not mdb_result.acknowledged:
            return {
                "n": 0,
                "ok": False,
                "opTime": {"t": time()}
            }
        
        return {
            "n": 1 if type(mdb_result) == pymongo.results.InsertOneResult else len(mdb_result.inserted_ids),
            "ok": True,
            "opTime": {"t": time()}
        }
    
    def f(self, user: str, query: dict[str, Any], *projection) -> None:
        
        if projection:
            cursor = self.users[user]["#db"].find(query, projection=projection[0])
        else:
            cursor = self.users[user]["#db"].find(query)
        
        # wraps the cursor so we're using hackmud syntax
        
        return HackmudCursorWrapper(cursor)
        
    
    def r(self, user: str, query: dict[Any, Any]) -> None:
        mdb_result = self.users[user]["#db"].delete_many(query)
        
        if not mdb_result.acknowledged:
            return {
                "n": 0,
                "ok": False,
                "opTime": {"t": time()}
            }
        
        return {
            "n": mdb_result.deleted_count,
            "ok": True,
            "opTime": {"t": time()}
        }
    
    def u(self, user): ...
    
    def u1(self, user): ...
    
    def us(self, user): ...
    
    def ObjectId(self):
        return {"$oid": str(ObjectId())}

    # #db.ObjectId() Generates a MongoDB ObjectId.
    
    # go through upload comms from game and add them here
    
    # edit
    # dir
    # up (delete public private shift)
    # down
    # DELETE
    # scripts
    #
    #help