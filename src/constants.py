from Peer import Peer


PORT = 18018
ADDRESS = "0.0.0.0"
SERVICE_LOOP_DELAY = 10
VERSION = '0.10.0'
AGENT = 'Khermes Node'
LOW_CONNECTION_THRESHOLD = 3
HELLO_MSG_TIMEOUT = 20.0
MAX_PEERS_TO_SEND = 30
MAX_CONNECTIONS = 20
DB_NAME = 'db.db'
RECV_BUFFER_LIMIT = 512 * 1024
BLOCK_TARGET = ""
BLOCK_VERIFY_WAIT_FOR_PREV_MUL = 10
BLOCK_VERIFY_WAIT_FOR_PREV = 1
BLOCK_VERIFY_WAIT_FOR_TXS_MUL = 10
BLOCK_VERIFY_WAIT_FOR_TXS = 1
BLOCK_REWARD = 50_000_000_000_000
GENESIS_BLOCK_ID = "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2"
GENESIS_BLOCK = {
        "T":"00000000abc00000000000000000000000000000000000000000000000000000",
        "created":1671062400,
        "miner":"Marabu",
        "nonce":"000000000000000000000000000000000000000000000000000000021bea03ed",
        "note":"The New York Times 2022-12-13: Scientists Achieve Nuclear Fusion Breakthrough With Blast of 192 Lasers",
        "previd": None,
        "txids":[],
        "type":"block"
}


BANNED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
    '1.0.0.127',
    '192.168.1.1',
    '172.16.0.1',
    '10.0.0.1',
    '8.8.8.8',
]

PRELOADED_PEERS = {
    Peer("128.130.122.101", 18018), # lecturers node
}

ERR_NAME_INV_HANDSHAKE = "INVALID_HANDSHAKE"
ERR_NAME_INV_FORMAT = "INVALID_FORMAT"

ERR_MSG_HANDSHAKE_TIMEOUT = "No handshake message was sent within 20 seconds!"
ERR_MSG_BEFORE_HANDSHAKE = "No other messages must be sent before the handshake!"
ERR_MSG_TWO_HANDSHAKES = "Only one handshake message must be sent!"
ERR_MSG_INV_PEERS = "Invalid list of peers!"