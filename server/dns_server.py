import json
from pathlib import Path
import dns.message
import dns.query
import dns.exception
import random
import time

BASE_DIR = Path(__file__).resolve().parent
ROOTNAME_SERVERS = BASE_DIR/'root_hints'/'rootname_servers.json'

class Resolver:

    def __init__(self, port: int):        
        try:
            with open(ROOTNAME_SERVERS, 'r') as file:
                self._root_hints = json.load(file)
        except FileExistsError or FileNotFoundError:
            print("Please restore the rootname_servers.json file in /root_hints directory")
        
        pass

    def resolve_query(self, query: str): 
    
        for ns, root in self._root_hints.items():
            #Hard coded the record type "A"
            user_query = dns.message.make_query(query, "A")
            #Could make use to writing over tcp socket instead but I would need to unserialize data.
            response = dns.query.tcp(user_query, root, timeout=1.0)
            curr_idx = 0
            authority_servers = response.additional
            while authority_servers:
                # if curr_idx >= len(authority_servers):
                #     print("Invalid domain name")
                #     return
                if response.answer:
                    print(response)
                    return
                #Converts the response RRSet object to text and split on " "
                authority_ip = authority_servers.pop().to_text().split(" ")[4]
                print(authority_ip)
                try:
                    response = dns.query.tcp(user_query, authority_ip, timeout= 1.0)
                except dns.exception.Timeout:
                    authority_servers += response.additional
                    time.sleep(0.1)
            
            print(response)
            return response            


        return "Could not correctly parse the input domain"


