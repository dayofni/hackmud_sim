
# code to handle mongod to be moved here
# because holy fuck I wish I didn't have to touch the cmd
# but apparently I do

from subprocess import Popen
from os         import makedirs, getcwd
from os.path    import exists, dirname, join, realpath

MONGOD = None
OUT    = None

def start_mongod(port: int = 1337) -> None:

    db_path = None # for safety atm, will need consideration.
    
    global MONGOD, OUT
    
    current_dir = dirname(realpath(__file__))
        
    # set it to be hackmud_sim/db/data, get absolute path
        
    if not db_path:
        db_path = join(current_dir, "data")
        
    # check to see if the data folder exists
    # if not, create it
        
    if not exists(db_path):
        makedirs(db_path)
        
    # Create stream to pipe cmd to
            
    OUT = open(join(getcwd(), "mongodb_server.log"), "w")
        
    # run mongod commands and init the database
        
    MONGOD = Popen([join(current_dir, "mongod"), "--dbpath", db_path, "--port", str(port)], stdout=OUT)

def terminate_mongod() -> None:
    MONGOD.terminate()
    OUT.close()