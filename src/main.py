from Peer import Peer
import constants as const
from message.msgexceptions import *
from jcs import canonicalize

from typing import Dict
from typing import List

import mempool
import objects
import peer_db

import asyncio
import ipaddress
import json
import random
import re
import sqlite3
import sys

PEERS = set()
CONNECTIONS = dict()
BACKGROUND_TASKS = set()
BLOCK_VERIFY_TASKS = dict()
BLOCK_WAIT_LOCK = None
TX_WAIT_LOCK = None
MEMPOOL = mempool.Mempool(const.GENESIS_BLOCK_ID, {})
LISTEN_CFG = {
        "address": const.ADDRESS,
        "port": const.PORT
}

# Add peer to your list of peers
def add_peer(peer: Peer):
    if peer not in PEERS and peer.host not in const.BANNED_HOSTS:
        print(f"Adding {peer}")

        PEERS.add(peer)
        peer_db.store_peer(peer)

# Add connection if not already open
def add_connection(peer: Peer, queue):
    print(f"Exchanged handshake with {peer}")
    
    # TODO Should the key of the dict be the (to send) msg queue or smth else?
    CONNECTIONS[peer] = queue


# Delete connection
def del_connection(peer: Peer):
    if peer in CONNECTIONS:
        del CONNECTIONS[peer]


# Make msg objects
def mk_error_msg(error_str, error_name) -> dict:
    return {
        "type": "error",
        "name": error_name,
        "msg": error_str
    }


def mk_hello_msg() -> dict:
    return {
        "agent": const.AGENT,
        "type": "hello",
        "version": const.VERSION
    }


def mk_getpeers_msg():
    return {
        "type": "getpeers",
    }


def mk_peers_msg(peers_to_send: set):
    return {
        "type": "peers",
        "peers": Peer.json_encoder(peers_to_send)
    }

def mk_getobject_msg(objid):
    pass # TODO

def mk_object_msg(obj_dict):
    pass # TODO

def mk_ihaveobject_msg(objid):
    pass # TODO

def mk_chaintip_msg(blockid):
    pass # TODO

def mk_mempool_msg(txids):
    pass # TODO

def mk_getchaintip_msg():
    pass # TODO

def mk_getmempool_msg():
    pass # TODO

# parses a message as json. returns decoded message
def parse_msg(msg_str: str) -> dict: 
    try:
        json_str = msg_str.strip()
        msg_dict = json.loads(json_str)
        return msg_dict
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        raise MsgParseException("INVALID_FORMAT")


# Send data over the network as a message
async def write_msg(writer: asyncio.StreamWriter, msg_dict: dict):
    try:
        json_msg = canonicalize(msg_dict)
        byte_msg = json_msg + b'\n'
        writer.write(byte_msg)
        await writer.drain()
        print(f"Sent {byte_msg} to {writer.get_extra_info('peername')}")
    except Exception as e:
        print(f"Failed to send message: {e}")

# Check if message contains no invalid keys,
# raises a MalformedMsgException
def validate_allowed_keys(msg_dict, allowed_keys, msg_type):
    pass # TODO

# Validate the hello message
# raises an exception
def validate_hello_msg(msg_dict):
    pass # TODO

# returns true iff host_str is a valid hostname
def validate_hostname(host_str):
    pass # TODO

# returns true iff host_str is a valid ipv4 address
def validate_ipv4addr(host_str):
    pass # TODO

# returns true iff peer_str is a valid peer address
def validate_peer_str(peer_str):
    pass # TODO

# raise an exception if not valid
def validate_peers_msg(msg_dict):
    pass # TODO

# raise an exception if not valid
def validate_getpeers_msg(msg_dict):
    pass # TODO

# raise an exception if not valid
def validate_getchaintip_msg(msg_dict):
    pass # TODO

# raise an exception if not valid
def validate_getmempool_msg(msg_dict):
    pass # TODO

# raise an exception if not valid
def validate_error_msg(msg_dict):
    pass # TODO

# raise an exception if not valid
def validate_ihaveobject_msg(msg_dict):
    pass # TODO

# raise an exception if not valid
def validate_getobject_msg(msg_dict):
    pass # TODO

# raise an exception if not valid
def validate_object_msg(msg_dict):
    pass # TODO

# raise an exception if not valid
def validate_chaintip_msg(msg_dict):
    pass # todo
    
# raise an exception if not valid
def validate_mempool_msg(msg_dict):
    pass # todo
        
def validate_msg(msg_dict: dict):
    validation_functions = {
        'hello': validate_hello_msg,
        'getpeers': validate_getpeers_msg,
        'peers': validate_peers_msg,
        'getchaintip': validate_getchaintip_msg,
        'getmempool': validate_getmempool_msg,
        'error': validate_error_msg,
        'ihaveobject': validate_ihaveobject_msg,
        'getobject': validate_getobject_msg,
        'object': validate_object_msg,
        'chaintip': validate_chaintip_msg,
        'mempool': validate_mempool_msg,
    }

    msg_type = msg_dict.get('type')

    if msg_type in validation_functions:
        validation_functions[msg_type](msg_dict)
    else:
        raise MsgParseException(const.ERR_NAME_INV_FORMAT)


async def handle_hello_msg(peer: Peer, queue: asyncio.Queue):
    add_connection(peer, queue)
    await queue.put(mk_getpeers_msg())


def handle_peers_msg(msg_dict: dict) -> bool:
    try:
        peers = msg_dict['peers']
        
        for peer_address in peers:
            host, port = peer_address.split(':', 1)
            add_peer(Peer(host, port))

        return True
    except Exception:
        return False


async def handle_getpeers_msg(queue: asyncio.Queue): 
    peers_to_send = set()

    try:
        peer_list = list(PEERS)
        size = min(len(PEERS), const.MAX_PEERS_TO_SEND)
        peers_to_send = random.sample(peer_list, size)
    except Exception as e:
        print(str(e))
    
    print(f"Peers to send: {peers_to_send}")
    
    await queue.put(mk_peers_msg(peers_to_send))


def handle_error_msg(msg_dict, peer_self):
    pass # TODO


async def handle_ihaveobject_msg(msg_dict, writer):
    pass # TODO


async def handle_getobject_msg(msg_dict, writer):
    pass # TODO

# return a list of transactions that tx_dict references
def gather_previous_txs(db_cur, tx_dict):
    # coinbase transaction
    if 'height' in tx_dict:
        return {}

    pass # TODO

# get the block, the current utxo and block height
def get_block_utxo_height(blockid):
    # TODO
    block = ''
    utxo = ''
    height = ''
    return (block, utxo, height)

# get all transactions as a dict txid -> tx from a list of ids
def get_block_txs(txids):
    pass # TODO


# Stores for a block its utxoset and height
def store_block_utxo_height(block, utxo, height: int):
    pass # TODO

# runs a task to verify a block
# raises blockverifyexception
async def verify_block_task(block_dict):
    pass # TODO

# adds a block verify task to queue and starting it
def add_verify_block_task(objid, block, queue):
    pass # TODO

# abort a block verify task
async def del_verify_block_task(task, objid):
    pass # TODO

# what to do when an object message arrives
async def handle_object_msg(msg_dict, peer_self, writer):
    pass # TODO

# returns the chaintip blockid
def get_chaintip_blockid():
    pass # TODO


async def handle_getchaintip_msg(msg_dict, writer):
    pass # TODO


async def handle_getmempool_msg(msg_dict, writer):
    pass # TODO


async def handle_chaintip_msg(msg_dict):
    pass # TODO


async def handle_mempool_msg(msg_dict):
    pass # TODO


async def handle_queue_msg(msg_dict: dict, writer: asyncio.StreamWriter):  
    # TODO Figure out why handle_queue_msg is needed in addition to write_msg
    await write_msg(writer, msg_dict)

def get_peer(writer: asyncio.StreamWriter) -> Peer | None:
    peername = writer.get_extra_info('peername')

    if not peername:
        print("Failed to get peername!")
        return None

    # TODO support address families other than IPv4?
    return Peer(peername[0], peername[1])

async def close_writer(writer: asyncio.StreamWriter):
    try:
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"Failed to close writer: {str(e)}")


async def handle_connection_exception(peername: str, e: Exception,
                                      writer: asyncio.StreamWriter):
    if isinstance(e, asyncio.exceptions.TimeoutError):
        print(f"{peername}: Timeout")
        await write_msg(writer, mk_error_msg("Timeout"))
    elif isinstance(e, MessageException):
        print(f"{peername}: {str(e)}")
        await write_msg(writer, mk_error_msg(e.NETWORK_ERROR_MESSAGE))
    else:
        print(f"{peername}: {str(e)}")
    

def defrag_msg(msg_byte_str: bytes, existing_partial_msg: str
                         ) -> tuple[List[str], str]:
    print(f"Defragmenting: {msg_byte_str}")

    msg_str = existing_partial_msg + msg_byte_str.decode('utf-8')
    partial_msg = ""

    regex = r'(?<!\\)(?:\\\\)*\n' # This Regex is not our own work but taken from the internet
    msg_strings = re.split(regex, msg_str)

    if not msg_str.endswith('\n') or msg_str.endswith('\\n'):
        partial_msg = msg_strings.pop()

    msg_strings_non_empty = list(filter(bool, msg_strings))

    return msg_strings_non_empty, partial_msg


async def handle_recv_msgs(peer: Peer, msg_strings: List[str],
                           queue: asyncio.Queue) -> str | None:
    for msg_str in msg_strings:
        print(f"Handling: {msg_str} from {peer}")

        msg_dict = None

        try:
            msg_dict = parse_msg(msg_str.strip())
            validate_msg(msg_dict)
        except MsgParseException as e:
            return mk_error_msg(e.NETWORK_ERROR_MESSAGE,
                                const.ERR_NAME_INV_FORMAT)

        msg_type = msg_dict.get('type')

        if msg_type == 'hello':
            if peer in CONNECTIONS:
                return mk_error_msg(const.ERR_MSG_TWO_HANDSHAKES,
                                    const.ERR_NAME_INV_HANDSHAKE)
            
            await handle_hello_msg(peer, queue)
        else:
            if peer not in CONNECTIONS:
                return mk_error_msg(const.ERR_MSG_BEFORE_HANDSHAKE,
                                    const.ERR_NAME_INV_HANDSHAKE)
            
            if msg_type == 'getpeers':
                await handle_getpeers_msg(queue)
            elif msg_type == 'peers':
                if not handle_peers_msg(msg_dict):
                    return mk_error_msg(const.ERR_MSG_INV_PEERS,
                                        const.ERR_NAME_INV_FORMAT)


def cancel_task(task: asyncio.Task | None):
    if task is not None and not task.done():
        task.cancel()


async def close_connection(peer: Peer, writer: asyncio.StreamWriter,
                           read_task: asyncio.Task | None,
                           queue_task: asyncio.Task | None):
    print(f"Closing connection with {peer}")
    await close_writer(writer)
    del_connection(peer)
    cancel_task(read_task)
    cancel_task(queue_task)


async def connection_exists(peer: Peer, delay: float):
    await asyncio.sleep(delay)
    return peer in CONNECTIONS


async def handshake_timer(peer: Peer, delay: float,
                                  event: asyncio.Event):
    await asyncio.sleep(delay)
    if peer not in CONNECTIONS:
        event.set()


async def handle_connection(reader: asyncio.StreamReader,
                            writer: asyncio.StreamWriter):
    read_task = None
    queue_task = None
    partial_msg = ""
    queue = asyncio.Queue()
    peer = get_peer(writer)

    if not peer:
        await close_writer(writer)
        return
    
    print(f"New connection with {str(peer)}")

    handshake_timeout = asyncio.Event()

    try:
        asyncio.create_task(handshake_timer(peer, 20, handshake_timeout))
        await queue.put(mk_hello_msg())

        while True:
            msg_byte_str = None

            if handshake_timeout.is_set():
                await write_msg(mk_error_msg(const.ERR_MSG_HANDSHAKE_TIMEOUT,
                                             const.ERR_NAME_INV_HANDSHAKE))
                break

            # Create write and read tasks
            if read_task is None:
                read_task = asyncio.create_task(reader.readline())
            if queue_task is None:
                queue_task = asyncio.create_task(queue.get())

            # wait for network (receive) or queue (send) messages
            done, pending = await asyncio.wait([read_task, queue_task],
                    return_when = asyncio.FIRST_COMPLETED, timeout=1)

            # handle read (received) messages
            if read_task in done:
                msg_byte_str = read_task.result()
                read_task = None

            if msg_byte_str == b'':
                print(f"Connection closed by {peer}")
                break

            # handle queue (to send) messages
            if queue_task in done:
                queue_msg = queue_task.result()
                queue_task = None
                await write_msg(writer, queue_msg)
                queue.task_done()

            # handle msg if it was received (task set to None)
            if read_task is None:
                defrag_msgs, partial_msg = defrag_msg(msg_byte_str, partial_msg)
                error_msg_dict = await handle_recv_msgs(peer, defrag_msgs, queue)

                if error_msg_dict is not None:
                    await write_msg(writer, error_msg_dict)
                    break

    except Exception as e:
        await handle_connection_exception(e)
    finally:
        await close_connection(peer, writer, read_task, queue_task)


async def connect_to_node(peer: Peer):
    if peer in CONNECTIONS:
        return
    
    try:
        reader, writer = await asyncio.open_connection(peer.host, peer.port,
                limit=const.RECV_BUFFER_LIMIT)
    except Exception as e:
        print(f"Could not connect with {peer}: {e}")
        return

    await handle_connection(reader, writer)


async def listen():
    server = await asyncio.start_server(handle_connection, LISTEN_CFG['address'],
            LISTEN_CFG['port'], limit=const.RECV_BUFFER_LIMIT)

    print("Listening on {}:{}".format(LISTEN_CFG['address'], LISTEN_CFG['port']))

    async with server:
        await server.serve_forever()


async def bootstrap():
    tasks = []

    for peer in const.PRELOADED_PEERS:
        add_peer(peer)
        tasks.append(connect_to_node(peer))

    await asyncio.gather(*tasks)


# connect to some peers
async def resupply_connections():
    # TODO More meaningful policy for which peers to connect to
    if len(CONNECTIONS) < const.MAX_CONNECTIONS:
        tasks = []
        
        for peer in PEERS:
            if peer in const.PRELOADED_PEERS:
                continue
            
            tasks.append(connect_to_node(peer))

            if len(CONNECTIONS) == const.MAX_CONNECTIONS:
                break

        await asyncio.gather(*tasks)


async def init():
    global BLOCK_WAIT_LOCK
    BLOCK_WAIT_LOCK = asyncio.Condition()
    global TX_WAIT_LOCK
    TX_WAIT_LOCK = asyncio.Condition()

    PEERS.update(peer_db.load_peers())

    print(f"Peers: {PEERS}")

    bootstrap_task = asyncio.create_task(bootstrap())
    listen_task = asyncio.create_task(listen())

    # Service loop
    while True:
        print("Service loop reporting in.")
        print("Open connections: {}".format(set(CONNECTIONS.keys())))

        # Open more connections if necessary
        await resupply_connections()
        await asyncio.sleep(const.SERVICE_LOOP_DELAY)

    await bootstrap_task
    await listen_task


def main():
    asyncio.run(init())

if __name__ == "__main__":
    if len(sys.argv) == 3:
        LISTEN_CFG['address'] = sys.argv[1]
        LISTEN_CFG['port'] = sys.argv[2]

    main()