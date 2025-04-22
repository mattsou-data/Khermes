import main as m
import objects as obj
from message.msgexceptions import *

SUCCESS_COUNT = 0
FAIL_COUNT = 0

# ----------------------------- Task 2 Unit Tests ------------------------------
def test_validate_peer_str_0():
    name = "Test Peer String Validation 256.2.3.4:18018"
    expected = type(ErrorInvalidFormat(""))

    peer_str = "256.2.3.4:18018"

    actual = None

    try:
        m.validate_peer_str(peer_str)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_peer_str_1():
    name = "Test Peer String Validation 1.2.3.4.5:678"
    expected = type(ErrorInvalidFormat(""))

    peer_str = "1.2.3.4.5:678"

    actual = None

    try:
        m.validate_peer_str(peer_str)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_peer_str_2():
    name = "Test Peer String Validation  1.2.3.4:2000000"
    expected = type(ErrorInvalidFormat(""))

    peer_str = " 1.2.3.4:2000000"

    actual = None

    try:
        m.validate_peer_str(peer_str)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_peer_str_3():
    name = "Test Peer String Validation nodotindomain:1234"
    expected = type(ErrorInvalidFormat(""))

    peer_str = "nodotindomain:1234"

    actual = None

    try:
        m.validate_peer_str(peer_str)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_peer_str_4():
    name = "Test Peer String Validation kermanode.net"
    expected = type(ErrorInvalidFormat(""))

    peer_str = "kermanode.net"

    actual = None

    try:
        m.validate_peer_str(peer_str)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_peer_str_5():
    name = "Test Peer String Validation 128.128.128.128:18018"
    expected = None

    peer_str = "128.128.128.128:18018"

    actual = None

    try:
        m.validate_peer_str(peer_str)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_peer_str_6():
    name = "Test Peer String Validation kermanode.net:18018"
    expected = None

    peer_str = "kermanode.net:18018"

    actual = None

    try:
        m.validate_peer_str(peer_str)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_peers_msg_0():
    name = "Test Validation of Peers Msg With Missing Key"
    expected = type(ErrorInvalidFormat(""))

    peers_msg = {
        "type" : "peers"
    }

    actual = None

    try:
        m.validate_peers_msg(peers_msg)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_peers_msg_1():
    name = "Test Validation of Peers Msg With Wrong Key"
    expected = type(ErrorInvalidFormat(""))

    peers_msg = {
        "type" : "peers",
        "peer" : [
            "kermanode.net:18017",
            "138.197.191.170:18018"
        ]
    }

    actual = None

    try:
        m.validate_peers_msg(peers_msg)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_peers_msg_2():
    name = "Test Validation of Peers Msg With Additonal Key"
    expected = type(ErrorInvalidFormat(""))

    peers_msg = {
        "type" : "peers",
        "peers" : [
            "kermanode.net:18017",
            "138.197.191.170:18018"
        ],
        "key" : "value"
    }

    actual = None

    try:
        m.validate_peers_msg(peers_msg)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_peers_msg_3():
    name = "Test Validation of Valid Peers Msg"
    expected = None

    peers_msg = {
        "type" : "peers",
        "peers" : [
            "kermanode.net:18017",
            "138.197.191.170:18018"
        ]
    }

    actual = None

    try:
        m.validate_peers_msg(peers_msg)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_hash_cb_tx():
    name = "Test Hash Calculation on Coinbase Transaction"
    expected = "d46d09138f0251edc32e28f1a744cb0b7286850e4c9c777d7e3c6e459b289347"

    obj_dict = {
            "height": 0,
            "outputs": [
                {
                    "pubkey": "85acb336a150b16a9c6c8c27a4e9c479d9f99060a7945df0bb1b53365e98969b",
                    "value": 50000000000000
                }
            ],
            "type": "transaction"
        }

    actual = obj.get_objid(obj_dict)

    return (name, expected, actual)

def test_hash_tx():
    name = "Test Hash Calculation on Transaction"
    expected = "895ca2bea390b7508f780c7174900a631e73905dcdc6c07a6b61ede2ebd4033f"

    obj_dict = {
        "inputs": [
            {
                "outpoint": {
                    "index": 0,
                    "txid": "d46d09138f0251edc32e28f1a744cb0b7286850e4c9c777d7e3c6e459b289347"
                },
                "sig": "6204bbab1b736ce2133c4ea43aff3767c49c881ac80b57ba38a3bab980466644cdbacc86b1f4357cfe45e6374b963f5455f26df0a86338310df33e50c15d7f04"
            }
        ],
        "outputs": [
            {
                "pubkey": "b539258e808b3e3354b9776d1ff4146b52282e864f56224e7e33e7932ec72985",
                "value": 10
            },
            {
                "pubkey": "8dbcd2401c89c04d6e53c81c90aa0b551cc8fc47c0469217c8f5cfbae1e911f9",
                "value": 49999999999990
            }
        ],
        "type": "transaction"
    }

    actual = obj.get_objid(obj_dict)

    return (name, expected, actual)

def test_hash_gen_block():
    name = "Test Hash Calculation on Genesis Block"
    expected = "00002fa163c7dab0991544424b9fd302bb1782b185e5a3bbdf12afb758e57dee"

    obj_dict = {
        "T" : "0000abc000000000000000000000000000000000000000000000000000000000" ,
        "created" : 1671062400,
        "miner" : "Marabu" ,
        "nonce" : "00000000000000000000000000000000000000000000000000000000005bb0f2" ,
        "note" : "The New York Times 2022-12-13: Scientists Achieve Nuclear Fusion Breakthrough With Blast of 192 Lasers" ,
        "previd" : None,
        "txids" : [],
        "type": "block"
    }

    actual = obj.get_objid(obj_dict)

    return (name, expected, actual)

def test_validate_object():
    name = "Test Validation of Object With no Type"
    expected = type(ErrorInvalidFormat(""))

    dict_obj = {
        "type": "invalid_type",
        "inputs": [
            {
                "outpoint": {
                    "txid": "f71408bf847d7dd15824574a7cd4afdfaaa2866286910675cd3fc371507aa196" ,
                    "index": 0
                },
                "sig": "3869a9ea9e7ed926a7c8b30fb71f6ed151a132b03fd5dae764f015c98271000e7da322dbcfc97af7931c23c0fae060e102446ccff0f54ec00f9978f3a69a6f0f"
            }
        ],
        "outputs": [
            {
                "pubkey": "077a2683d776a71139fd4db4d00c16703ba0753fc8bdc4bd6fc56614e659cde3" ,
                "value": 5100000000
            }
        ]
    }

    actual = None

    try:
        obj.validate_object(dict_obj)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_tx_0():
    name = "Test Validation of Valid Transaction"
    expected = None

    dict_tx = {
        "type": "transaction",
        "inputs": [
            {
                "outpoint": {
                    "txid": "f71408bf847d7dd15824574a7cd4afdfaaa2866286910675cd3fc371507aa196" ,
                    "index": 0
                },
                "sig": "3869a9ea9e7ed926a7c8b30fb71f6ed151a132b03fd5dae764f015c98271000e7da322dbcfc97af7931c23c0fae060e102446ccff0f54ec00f9978f3a69a6f0f"
            }
        ],
        "outputs": [
            {
                "pubkey": "077a2683d776a71139fd4db4d00c16703ba0753fc8bdc4bd6fc56614e659cde3" ,
                "value": 5100000000
            }
        ]
    }

    actual = None

    try:
        obj.validate_transaction(dict_tx)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_tx_1():
    name = "Test Validation of Transaction With Missing Input"
    expected = type(ErrorInvalidFormat(""))

    dict_tx = {
        "type": "transaction",
        "outputs": [
            {
                "pubkey": "077a2683d776a71139fd4db4d00c16703ba0753fc8bdc4bd6fc56614e659cde3" ,
                "value": 5100000000
            }
        ]
    }

    actual = None

    try:
        obj.validate_transaction(dict_tx)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_tx_2():
    name = "Test Validation of Transaction With Missing Output"
    expected = type(ErrorInvalidFormat(""))

    dict_tx = {
        "type": "transaction",
        "inputs": [
            {
                "outpoint": {
                    "txid": "f71408bf847d7dd15824574a7cd4afdfaaa2866286910675cd3fc371507aa196" ,
                    "index": 0
                },
                "sig": "3869a9ea9e7ed926a7c8b30fb71f6ed151a132b03fd5dae764f015c98271000e7da322dbcfc97af7931c23c0fae060e102446ccff0f54ec00f9978f3a69a6f0f"
            }
        ]
    }

    actual = None

    try:
        obj.validate_transaction(dict_tx)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_tx_3():
    name = "Test Validation of Transaction With Missing Output Index in Inputs"
    expected = type(ErrorInvalidFormat(""))

    dict_tx = {
        "type": "transaction",
        "inputs": [
            {
                "outpoint": {
                    "txid": "f71408bf847d7dd15824574a7cd4afdfaaa2866286910675cd3fc371507aa196"
                },
                "sig": "3869a9ea9e7ed926a7c8b30fb71f6ed151a132b03fd5dae764f015c98271000e7da322dbcfc97af7931c23c0fae060e102446ccff0f54ec00f9978f3a69a6f0f"
            }
        ],
        "outputs": [
            {
                "pubkey": "077a2683d776a71139fd4db4d00c16703ba0753fc8bdc4bd6fc56614e659cde3" ,
                "value": 5100000000
            }
        ]
    }

    actual = None

    try:
        obj.validate_transaction(dict_tx)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_tx_4():
    name = "Test Validation of Transaction With Wrong Output Value Type"
    expected = type(ErrorInvalidFormat(""))

    dict_tx = {
        "type": "transaction",
        "inputs": [
            {
                "outpoint": {
                    "txid": "f71408bf847d7dd15824574a7cd4afdfaaa2866286910675cd3fc371507aa196"
                },
                "sig": "3869a9ea9e7ed926a7c8b30fb71f6ed151a132b03fd5dae764f015c98271000e7da322dbcfc97af7931c23c0fae060e102446ccff0f54ec00f9978f3a69a6f0f"
            }
        ],
        "outputs": [
            {
                "pubkey": "077a2683d776a71139fd4db4d00c16703ba0753fc8bdc4bd6fc56614e659cde3" ,
                "value": "5100000000"
            }
        ]
    }

    actual = None

    try:
        obj.validate_transaction(dict_tx)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_tx_5():
    name = "Test Validation of Transaction With Wrong Output txid Type in Inputs"
    expected = type(ErrorInvalidFormat(""))

    dict_tx = {
        "type": "transaction",
        "inputs": [
            {
                "outpoint": {
                    "txid": 2
                },
                "sig": "3869a9ea9e7ed926a7c8b30fb71f6ed151a132b03fd5dae764f015c98271000e7da322dbcfc97af7931c23c0fae060e102446ccff0f54ec00f9978f3a69a6f0f"
            }
        ],
        "outputs": [
            {
                "pubkey": "077a2683d776a71139fd4db4d00c16703ba0753fc8bdc4bd6fc56614e659cde3" ,
                "value": 5100000000
            }
        ]
    }

    actual = None

    try:
        obj.validate_transaction(dict_tx)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

# ----------------------------- Task 3 Unit Tests ------------------------------

def test_validate_block_0():
    name = "Test Validation of Valid Block With Notes"
    expected = None

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "miner": "grader" ,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "note": "This block has a coinbase transaction",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_1():
    name = "Test Validation of Valid Block Without Notes"
    expected = None

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_2():
    name = "Test Validation of Block With Wrong T Type"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": 0xabc00000000000000000000000000000000000000000000000000000,
        "created": 1671148800,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_3():
    name = "Test Validation of Block with wrong T"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": "00000000abd00000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_4():
    name = "Test Validation of Block With Wrong created Type"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": "1671148800",
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_5():
    name = "Test Validation of Block With Invalid Long note"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "note": "....................................................................................................................................",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_6():
    name = "Test Validation Block With note With Illegal Characters"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "note": "©",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_7():
    name = "Test Validation of Block With Wrong note Type"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "miner": "grader" ,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "note": 123,
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_8():
    name = "Test Validation of Block With Wrong previd Type"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "miner": "grader" ,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "note": "This block has a coinbase transaction",
        "previd": 0x52a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2,
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_9():
    name = "Test Validation of Block With Invalid previd"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "miner": "grader" ,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "note": "This block has a coinbase transaction",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fz756747f29ef52594d68484bb5e2",
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_10():
    name = "Test Validation of Block With Wrong txids Type"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "miner": "grader" ,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "note": "This block has a coinbase transaction",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a",
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_11():
    name = "Test Validation of Block With Invalid txid Type in txids"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "miner": "grader" ,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "note": "This block has a coinbase transaction",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : [
            0x6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_12():
    name = "Test Validation of Block With Invalid txid in txids"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "miner": "grader" ,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "note": "This block has a coinbase transaction",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1z143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def test_validate_block_13():
    name = "Test Validation of Block With Invalid Additional key"
    expected = type(ErrorInvalidFormat(""))

    block_dict = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": 1671148800,
        "nonce": "1000000000000000000000000000000000000000000000000000000001aaf999",
        "previd": "0000000052a0e645eca917ae1c196e0d0a4fb756747f29ef52594d68484bb5e2",
        "txids" : [
            "6ebfb4c8e8e9b19dcf54c6ce3e1e143da1f473ea986e70c5cb8899a4671c933a"
        ],
        "test" : "",
        "type": "block"
    }

    actual = None

    try:
        obj.validate_block(block_dict)
    except Exception as e:
        actual = type(e)

    return (name, expected, actual)

def unit_test(function):
    global SUCCESS_COUNT, FAIL_COUNT
    name, expected, actual = function()

    match = expected == actual

    if match:
        SUCCESS_COUNT += 1
    else:
        FAIL_COUNT += 1

    print(name)
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")
    print(f"Matches:  {match}")
    print("")

def main():
    print("Executing unit tests\n")

    # Task 2
    unit_test(test_validate_peer_str_0)
    unit_test(test_validate_peer_str_1)
    unit_test(test_validate_peer_str_2)
    unit_test(test_validate_peer_str_3)
    unit_test(test_validate_peer_str_4)
    unit_test(test_validate_peer_str_5)
    unit_test(test_validate_peer_str_6)

    unit_test(test_hash_tx)
    unit_test(test_hash_cb_tx)
    unit_test(test_hash_gen_block)

    unit_test(test_validate_object)
    unit_test(test_validate_tx_0)
    unit_test(test_validate_tx_1)
    unit_test(test_validate_tx_2)
    unit_test(test_validate_tx_3)
    unit_test(test_validate_tx_4)
    unit_test(test_validate_tx_5)

    # Task 3
    # unit_test(test_validate_block_0)
    # unit_test(test_validate_block_1)
    # unit_test(test_validate_block_2)
    # unit_test(test_validate_block_3)
    # unit_test(test_validate_block_4)
    # unit_test(test_validate_block_5)
    # unit_test(test_validate_block_6)
    # unit_test(test_validate_block_7)
    # unit_test(test_validate_block_8)
    # unit_test(test_validate_block_9)
    # unit_test(test_validate_block_10)
    # unit_test(test_validate_block_11)
    # unit_test(test_validate_block_12)
    # unit_test(test_validate_block_13)

    print(f"Tests succeeded: {SUCCESS_COUNT} Tests failed: {FAIL_COUNT}")

if __name__ == "__main__":
    main()