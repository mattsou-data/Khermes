from Peer import Peer
from typing import Iterable, Set
import os
import csv

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PEER_DB_FILE = os.path.join(SRC_DIR, "peers.csv")

def store_peer(peer: Peer, existing_peers: Iterable[Peer] = None):
    if existing_peers is not None:
        if peer in existing_peers:
            return

    try:
        with open(PEER_DB_FILE, 'a', newline='') as peer_csv:
            writer = csv.writer(peer_csv)
            writer.writerow([peer.host, peer.port])
    except Exception as e:
        print(f"Failed to store peer: {e}")


def load_peers() -> Set[Peer]:
    peers = set()
    
    try:
        with open(PEER_DB_FILE, 'r') as peer_csv:
            csv_reader = csv.reader(peer_csv)
            next(csv_reader)
            
            for row in csv_reader:
                host, port = row
                peers.add(Peer(host, port))

            print(f"Successfully loaded peers!")
    except Exception as e:
        print(f"Failed to load stored peers: {e}")

    return peers
