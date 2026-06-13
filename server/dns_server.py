import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOTNAME_SERVERS = BASE_DIR/'root_hints'/'rootname_servers.json'

class Resolver:

    def __init__(self, port: int):        
        try:
            with open(ROOTNAME_SERVERS, 'r') as file:
                self._root_hints = json.load(file)
        except FileExistsError or FileNotFoundError:
            print("Please restore the rootname_servers.json file in /root_hints directory")
        
        print(self._TLDMap)
        pass

    def resolve_query(self, query: str): 
        


        pass


