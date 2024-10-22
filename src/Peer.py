import ipaddress
from typing import Self

"""
host
host_formated == host for hostname and ipv4
"""
class Peer:
    def validate_domain_name(self, dn: str) -> bool:
        # Conditions taken from project overview 5.3
        if not (3 <= len(dn) <= 50):
            return False
    
        if '.' not in dn[1:-1]:
            return False

        atLeastOneLetter = False

        for char in dn:
            if not (char.isalnum() or char in ['.', '-', '_']):
                return False
            
            if char.isalpha():
                atLeastOneLetter = True

        return atLeastOneLetter
    

    def validate_host(self, host: str):
        try:
            ipaddress.IPv4Address(host)
        except ipaddress.AddressValueError:
            if not self.validate_domain_name(host):
                raise ValueError(f"Could not create Peer! Invalid address: {host}")
            
    def validate_port(self, port: int):
        if not (1 <= port <= 65535):
            raise ValueError(f"Could not create Peer! Invalid port: {port}")

    def __init__(self, host_str: str, port: int):
        self.validate_host(host_str)
        self.validate_port(int(port))

        self.port = int(port)
        self.host_formated = host_str
        self.host = host_str

    def __str__(self) -> str:
        return f"{self.host_formated}:{self.port}"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Peer) and self.host == o.host \
            and self.port == o.port

    def __hash__(self) -> int:
        return hash((self.host, self.port))

    def __repr__(self) -> str:
        return f"Peer: {self}"
    
    @staticmethod
    def json_encoder(obj: list | Self):
        if isinstance(obj, Peer):
            return str(obj)
        elif isinstance(obj, list):
            return [Peer.json_encoder(peer) for peer in obj]
        
        raise TypeError(f"Object is not of type list or Peer!")