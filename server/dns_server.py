import json
from pathlib import Path
from dns.rrset import RRset
from dns.rdata import Rdata
import dns.message
import dns.query
import dns.exception
import dns.rcode
import dns.rdatatype
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

    def fetch_glue_record_ip(self, additional_servers: list[RRset], record_type: str) -> str:
        res: list[RRset] = []

        for rrset in additional_servers:
            record = dns.rdatatype.to_text(rrset.rdtype) 
            if record == record_type:
                res.append(rrset)
        
        random_idx = random.randint(0, len(res) - 1)
        random_server: Rdata = res[random_idx].pop()
        glue_ip = random_server.to_text()
        return glue_ip


    def resolve_query(self, query: str): 
        
        root_server = self._root_hints["a.root-servers.net"]
        user_query = dns.message.make_query(query, "A")
        res = dns.query.udp(user_query, root_server)
        while True:
            if res.rcode() != dns.rcode.NOERROR:
                print(f'Could not resolve domain: {query}, encountered error: {res.rcode().to_text}' )
                return
            if res.answer:
                answer = None
                for rrset in res.answer:
                    record_type = dns.rdatatype.to_text(rrset.rdtype)
                    if record_type == "A":
                        answer = rrset
                return answer

            if res.authority:
                if res.additional:
                    glue_ip = self.fetch_glue_record_ip(res.additional, "A")
                    res = dns.query.udp(user_query, glue_ip)
                else:
                    random_idx = random.randint(0, len(res.authority) - 1)
                    random_rrset = res.authority[random_idx]
                    record: Rdata = random_rrset.pop()
                    ns_record = record.to_text()[0:len(record.to_text()) - 1]
                    glue_ip: Rdata = self.resolve_query(ns_record).pop()
                    glue_ip = glue_ip.to_text()
                    res = dns.query.udp(user_query, glue_ip)           




