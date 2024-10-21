import ipaddress
from typing import Self

"""
host
host_formated == host for hostname and ipv4
"""
class Peer:
    def validate_ipv4(self, ip):
        try:
            ipaddress.IPv4Address(ip)
        except ipaddress.AddressValueError:
            raise ValueError("Invalid IPv4 address: " + ip)

    def __init__(self, host_str: str, port: int):
        self.validate_ipv4(host_str)
        # TODO validate port?

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