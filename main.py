import sys
from server.dns_server import Resolver

def main():
    # if len(sys.argv) < 2:
    #     print("usage: python main.py <domain query>")
    #     return

    query = sys.argv[1]
    dns = Resolver(6767)
    # print(dns.resolve_query(query))


if __name__ == "__main__":
    main()