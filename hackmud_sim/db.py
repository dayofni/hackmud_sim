
import pymongo

from typing import Any, Union

class HackmudDatabase:
    
    def __init__(self) -> None:
        
        self.db = pymongo.MongoClient("localhost", 27017)
        
        self.player_data = self.db["player_data"]
        self.scripts     = self.db["scripts"]
        
        self.users = {}
    
    def create_user(self, user: str) -> None:
        
        assert user not in self.users, f"User {user} already exists!"
        
        # Creates a user using the db
        
        self.users[user] = {
            "data":    self.player_data[user],
            "scripts": self.scripts[user]
        }
    
    def i(self, user, data: Union[Any, list[Any]]) -> None:
        
        if (type(data) not in [list, tuple]):
            self.users[user]["data"].insert_one(data)
        
        else:
            self.users[user]["data"].insert_many(data)
        
        print(self.users[user])
    
    def f(self, user): ...
    
    def r(self, user): ...
    
    def u(self, user): ...

a = HackmudDatabase()
a.create_user("dayofni")

a.i("dayofni", {"game": "hello_world"})