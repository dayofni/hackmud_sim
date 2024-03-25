
import pymongo
import pymongo.results

import hackmud_sim.db.mongod as mongod

from bson import ObjectId

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
    
    def __init__(self, db_path: Optional[str] = None, port: int = 1337) -> None:
        
        """
        # NEVER EVER LET THE USER PICK THE DB_PATH.
        
        ## IF YOU VALUE YOUR COMPUTER. NEVER LET THEM PICK.
        
        AS IS, I CAN STILL THINK OF AN EXPLOIT TO GET AROUND IT.
        
        ONCE PEOPLE HAVE LOOKED AT THIS AND MADE DAMN SURE IT'S SAFE, *DON'T DO IT*!
        
        ### DON'T RISK IT
        """
        
        assert type(port) == int, "Port needs to be an int."
        
        self.mongo_server = None
        self.db_path      = db_path
        self.host         = "localhost", 
        self.port         = port     # 1337 game, dude
        
        self.mongo_out = None
    
    def __enter__(self):
        
        self.start_mongodb(self.db_path, self.port)
        self.start_client(self.host, self.port)
        
        return self

    def __exit__(self, *exc: Any) -> None:
        mongod.terminate_mongod() # kill the server
    
    def start_mongodb(self, db_path: Optional[str], port: int) -> None:
        mongod.start_mongod(port=port)
    
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
    
    def i(self, user, data: Union[dict[str, Any], list[dict[str, Any]]]) -> dict[str, Any]:
        
        start = time() * 1000
        
        if (type(data) not in [list, tuple]):
            mdb_result = self.users[user]["#db"].insert_one(data)
        
        else:
            mdb_result = self.users[user]["#db"].insert_many(data)
        
        if not mdb_result.acknowledged:
            return {
                "n": 0,
                "ok": False,
                "opTime": round((time() * 1000) - start)
            }
        
        return {
            "n": 1 if type(mdb_result) == pymongo.results.InsertOneResult else len(mdb_result.inserted_ids),
            "ok": True,
            "opTime": round((time() * 1000) - start)
        }
    
    def f(self, user: str, query: dict[str, Any], *projection) -> HackmudCursorWrapper:
        
        if projection:
            cursor = self.users[user]["#db"].find(query, projection=projection[0])
        else:
            cursor = self.users[user]["#db"].find(query)
        
        # wraps the cursor so we're using hackmud syntax
        
        return HackmudCursorWrapper(cursor)
    
    def r(self, user: str, query: dict[str, Any]) -> dict[str, Any]:
        
        start = time() * 1000
        
        mdb_result = self.users[user]["#db"].delete_many(query)
        
        if not mdb_result.acknowledged:
            return {
                "n": 0,
                "ok": False,
                "opTime": round((time() * 1000) - start)
            }
        
        return {
            "n": mdb_result.deleted_count,
            "ok": True,
            "opTime": round((time() * 1000) - start)
        }
    
    def u(self, user: str, query: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
        
        start = time() * 1000
        
        mdb_result = self.users[user]["#db"].update_many(query, update)
        
        if not mdb_result.acknowledged:
            return {
                "n": 0,
                "nModified": 0,
                "ok": False,
                "opTime": round((time() * 1000) - start)
            }
        
        return {
            "n": mdb_result.matched_count,
            "nModified": mdb_result.modified_count,
            "ok": True,
            "opTime": round((time() * 1000) - start)
        }
    
    def u1(self, user: str, query: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
        
        start = time() * 1000
        
        mdb_result = self.users[user]["#db"].update_one(query, update)
        
        if not mdb_result.acknowledged:
            return {
                "n": 0,
                "nModified": 0,
                "ok": False,
                "opTime": round((time() * 1000) - start)
            }
        
        return {
            "n": min(1, mdb_result.matched_count),
            "nModified": min(1, mdb_result.modified_count),
            "ok": True,
            "opTime": round((time() * 1000) - start)
        }
    
    def us(self, user: str, query: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
        
        start = time() * 1000
        
        mdb_result = self.users[user]["#db"].update_many(query, update, upsert=True)
        
        if not mdb_result.acknowledged:
            return {
                "n": 0,
                "nModified": 0,
                "ok": False,
                "opTime": round((time() * 1000) - start)
            }
        
        return {
            "n": mdb_result.matched_count,
            "nModified": mdb_result.modified_count,
            "upserted": mdb_result.upserted_id,
            "ok": True,
            "opTime": round((time() * 1000) - start)
        }
    
    def ObjectId(self):
        return {"$oid": str(ObjectId())}
    
    # go through upload comms from game and add them here
    
    # edit
    # dir
    # up (delete public private shift)
    # down
    # DELETE
    # scripts
    #
    #help