import json
import sqlite3
import main as m
import objects as obj
from message.msgexceptions import *
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from jcs import canonicalize
import copy
import constants as const
import objects


def create_transaction_coinbase(height,value):
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    pubkey = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    ).hex()
    pri_key = private_key.private_bytes( encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption()).hex()
    tx = {
        "height": height,
        "outputs": [
            {
                "pubkey": pubkey,
                "value": value
            }
        ],
        "type": "transaction"
    }

    obj_id = obj.get_objid(tx)

    return tx, pri_key, obj_id


def verify_tx_signature(tx_dict, sig, pubkey):
    print(tx_dict)
    print(sig)
    print(pubkey)
    print(type(sig))
    print(type(pubkey))
    tx_local = copy.deepcopy(tx_dict)
    for i in tx_local["inputs"]:
        i["sig"] = None

    pubkey_obj = Ed25519PublicKey.from_public_bytes(bytes.fromhex(str(pubkey)))
    sig_bytes = bytes.fromhex(str(sig))

    return Ed25519PublicKey.verify(pubkey_obj, sig_bytes, bytes.fromhex(obj.get_objid(tx_local)))


def sign_input(txid, pri_key):
    private_key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(pri_key))
    signature = private_key.sign(bytes.fromhex(txid))
    return signature.hex()



def create_input(tx, pri_key):
    obj_id = obj.get_objid(tx[0])
    

    input = {
        "outpoint": {
            "txid": obj_id,
            "index": 0
        },
        "sig": None
    }
    sig = sign_input(obj_id, pri_key)
    input["sig"] = sig
    tx_id = obj.get_objid(input)
    return input, tx_id

def create_output(value):
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    pubkey = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    ).hex()
    tx = {"pubkey": pubkey, "value": value}
    pri_key = private_key.private_bytes( encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption()).hex()
    return tx, pri_key

def create_transaction(inputs, outputs):
    tx = {
        "inputs": inputs,
        "outputs": outputs,
        "type": "transaction"
    }
    obj_id = obj.get_objid(tx)
    return tx, obj_id

id_orig = "00002fa163c7dab0991544424b9fd302bb1782b185e5a3bbdf12afb758e57dee"


def create_block(transactions, created, miner, note, previd):
    txids = []
    nonce = "1000000000000000000000000000000000000000000000000000000001aaf999"
    for tx in transactions:
        txids.append(obj.get_objid(tx))
    block = {
        "T": "0000abc000000000000000000000000000000000000000000000000000000000",
        "created": created,
        "miner": miner,
        "nonce": nonce,
        "note": note,
        "previd": previd,
        "txids": txids,
        "type": "block"}
    return block, obj.get_objid(block)

import os

def mine_block(transaction,created, miner, note=None, previd=None):
    block, block_id = create_block(transaction, created , miner, note, previd)
    
    while (int(obj.get_objid(block), 16) > int(const.BLOCK_TARGET, 16)):
        block["nonce"] = os.urandom(32).hex()
        block_id = obj.get_objid(block)
    
    return block, block_id



coinbase1, key_coinbase1, idcoinbase1 = create_transaction_coinbase(1,50000000000000)
coinbase2, key_coinbase2, idcoinbase2 = create_transaction_coinbase(2, 50000000000000)
coinbase3, key_coinbase3, idcoinbase3 = create_transaction_coinbase(4, 50000000000000)


input_transaction_1, id_transaction_1 = create_input([coinbase1], key_coinbase1)
output_transaction_1, pri_key_transaction_1 = create_output(coinbase1["outputs"][0]["value"])
transaction_1, id_transaction_1 = create_transaction([input_transaction_1], [output_transaction_1])

input_transaction_1_1, id_transaction_1_1 = create_input([transaction_1], pri_key_transaction_1)
output_transaction_1_1, pri_key_transaction_1_1 = create_output(transaction_1["outputs"][0]["value"])
transaction_1_1, id_transaction_1_1 = create_transaction([input_transaction_1_1], [output_transaction_1_1])

input_transaction_1_2, id_transaction_1_2 = create_input([transaction_1_1], pri_key_transaction_1_1)
output_transaction_1_2, pri_key_transaction_1_2 = create_output(transaction_1_1["outputs"][0]["value"])
transaction_1_2, id_transaction_1_2 = create_transaction([input_transaction_1_2], [output_transaction_1_2])



input_transaction_2, id_transaction_2 = create_input([coinbase2], key_coinbase2)
output_transaction_2, pri_key_transaction_2 = create_output(coinbase2["outputs"][0]["value"])
transaction_2, id_transaction_2 = create_transaction([input_transaction_2], [output_transaction_2])

input_transaction_2_1, id_transaction_2_1 = create_input([transaction_2], pri_key_transaction_2)
output_transaction_2_1, pri_key_transaction_2_1 = create_output(transaction_2["outputs"][0]["value"])
transaction_2_1, id_transaction_2_1 = create_transaction([input_transaction_2_1], [output_transaction_2_1])




input_transaction_3, id_transaction_3 = create_input([coinbase3], key_coinbase3)
output_transaction_3, pri_key_transaction_3 = create_output(coinbase3["outputs"][0]["value"])
transaction_3, id_transaction_3 = create_transaction([input_transaction_3], [output_transaction_3])

input_transaction_3_1, id_transaction_2_1 = create_input([transaction_3], pri_key_transaction_3)
output_transaction_3_1, pri_key_transaction_3_1 = create_output(transaction_3["outputs"][0]["value"])
transaction_3_1, id_transaction_3_1 = create_transaction([input_transaction_3_1], [output_transaction_3_1])

import time

start = int(time.time()*2)

#block1, id_block1= mine_block([coinbase1], 1671062401, "miner", "block1", "00002fa163c7dab0991544424b9fd302bb1782b185e5a3bbdf12afb758e57dee")
#block2, id_block2 = mine_block([coinbase2], 1671148802, "miner", "block2", str(id_block1))

#block3, id_block3 = mine_block([transaction_2, transaction_1_1], 1671148803, "miner", "block3", str(id_block2))

#block3bis, id_block3bis = mine_block([transaction_2, transaction_1_1], 1671148803, "miner", "block3", str(id_block2))

#block4, id_block4 = mine_block([coinbase3, transaction_2_1, transaction_1_2], 1671148804, "miner", "block4", str(id_block3bis))

#block5, id_block5 = mine_block([transaction_3], 1671148805, "miner", "block5", str(id_block2))

#l = [block1, block2, block3, block3bis, block4, transaction_1, transaction_1_1, transaction_1_2, transaction_2, transaction_2_1, transaction_3, transaction_3_1, coinbase1, coinbase2, coinbase3]

b1 ={'T': '0000abc000000000000000000000000000000000000000000000000000000000', 'created': 1671062401, 'miner': 'miner', 'nonce': '3574d13c86eea358a496e5a8b76b4eedcf398547ed7829d6acaf737303185f03', 'note': 'block1', 'previd': '00002fa163c7dab0991544424b9fd302bb1782b185e5a3bbdf12afb758e57dee', 'txids': ['dbe13639c2fa03d3e383d08db278938d0a7ce7acda366d318df4a9dd94b66c38'], 'type': 'block'}
b2 ={'T': '0000abc000000000000000000000000000000000000000000000000000000000', 'created': 1671148802, 'miner': 'miner', 'nonce': 'c9884fab6b9839ee6648f1254bab622cb7f2c52fbe08b519a888e99505bab223', 'note': 'block2', 'previd': '00000dd23493fc3850c3e0b8d26d7ea47ecadb5a6fba033c22d39f90d2b6d3bd', 'txids': ['576a3f29c8195e48e9ff8e4a0bc08611d1b132f51466055edd4f26d2e9798c5b'], 'type': 'block'}
b3 ={'T': '0000abc000000000000000000000000000000000000000000000000000000000', 'created': 1671148803, 'miner': 'miner', 'nonce': 'c474df88065d9fb7cc2f701fe1bbfc4974ffeef9dcfd9139ef53b1a91256018b', 'note': 'block3', 'previd': '00005f45e75c463be54e6473a5b74cc02c6259aa5578043bbbf4e256c90040a0', 'txids': ['db2a932bd48d187230ca11f8e7a5b4569a0d1d7da7a3df417eb810e94757c3a1', 'a3883ddc8f6edcfd902ef235d2a971cb89869043ed453b2595a8a07366b26596'], 'type': 'block'}     
b3bis ={'T': '0000abc000000000000000000000000000000000000000000000000000000000', 'created': 1671148803, 'miner': 'miner', 'nonce': 'edcfabfa5b128b7010eab3b29e8cc98892b04bb1531f1cf0ed155a61029beebf', 'note': 'block3', 'previd': '00005f45e75c463be54e6473a5b74cc02c6259aa5578043bbbf4e256c90040a0', 'txids': ['db2a932bd48d187230ca11f8e7a5b4569a0d1d7da7a3df417eb810e94757c3a1', 'a3883ddc8f6edcfd902ef235d2a971cb89869043ed453b2595a8a07366b26596'], 'type': 'block'}     
b4 ={'T': '0000abc000000000000000000000000000000000000000000000000000000000', 'created': 1671148804, 'miner': 'miner', 'nonce': '922b778bb2d17fff3cafb5dc2353f3547ac05afbcd1dba11f237000047b0137a', 'note': 'block4', 'previd': '0000723fc24a929a8498c5558649aad2960d1dabdd4507180473f53d785c8853', 'txids': ['cd01f1fb749531b9572d5cbe332bd6738efa897727dab729aebec3dfcc5f6c15', '3fccf262fee1d01e85c4a7703620b2838c473289a4ebde8e96dc595d6f458c97', '9c3ea672d0ac6da98ab9b109ef7a0d5a6baf5f2cd10f050811b0baea609c53db'], 'type': 'block'}
transaction_1 ={'inputs': [{'outpoint': {'txid': 'dbe13639c2fa03d3e383d08db278938d0a7ce7acda366d318df4a9dd94b66c38', 'index': 0}, 'sig': '66cf773075fc12277b56fd9c621226ea262fa27cc21ce7c24892ca2df13c612861ccd9b3a0c6af6add6c7fd40fb9411cf737b87a7ceac38b7453fc37f1f2ba0d'}], 'outputs': [{'pubkey': '4a8ee8b67825aa0756f9b72f54c7ea3af2b6d6a740187ef41a00a4b170d354d1', 'value': 50000000000000}], 'type': 'transaction'}
transaction_1_1 ={'inputs': [{'outpoint': {'txid': '2a86bc6569c81442740e853b1ea766e0cf3a39e2338b595656f1ea0f82ffb9c0', 'index': 0}, 'sig': 'ea945f9990254d8a627885d76923f63b0fd5a8a7792395c295bd887561c7f5e3fda34c84b9c6c47930f625b713ea5b1242ea3ed080a9c67c47369013933ae204'}], 'outputs': [{'pubkey': '94c7d22a22ddab6935db2e4a0e689a5ba750489b9c306489d9f41238269c7f0c', 'value': 50000000000000}], 'type': 'transaction'}
transaction_1_2 ={'inputs': [{'outpoint': {'txid': 'a3883ddc8f6edcfd902ef235d2a971cb89869043ed453b2595a8a07366b26596', 'index': 0}, 'sig': '24f160a711bf114dad33902ebd28e1a47a287a5b000c64628050cdf9f21ab8d9484a37b4b94dd2234395db707e18eb45933499b064ef448254f3f9b19043ad05'}], 'outputs': [{'pubkey': '3dfd27e0c6f850d722373eee01788d3f67d1aaa5de0d942839619b9648827ba3', 'value': 50000000000000}], 'type': 'transaction'}
transaction_2 ={'inputs': [{'outpoint': {'txid': '576a3f29c8195e48e9ff8e4a0bc08611d1b132f51466055edd4f26d2e9798c5b', 'index': 0}, 'sig': '6b688b280ede4f026d280d61e7164ac40bb3c614d9059a7bd850513510f1150442606fd80dbd052bec494781afc82530730fd0b86c5adb3c3e2c29a31be1a109'}], 'outputs': [{'pubkey': '3f8ede093fb9eefbbcdc08f96edb2cbbaf0e1e78158fcd4cfde8d6c51e6772f0', 'value': 50000000000000}], 'type': 'transaction'}
transaction_2_1 ={'inputs': [{'outpoint': {'txid': 'db2a932bd48d187230ca11f8e7a5b4569a0d1d7da7a3df417eb810e94757c3a1', 'index': 0}, 'sig': 'a9fd569584811715af8335cf3c59e7b2b6162a858cab3138fcef33e8158ff1039d77bd192dab03dec54d949eb0c01a1e861324e40413229aeb44f02f15cb700b'}], 'outputs': [{'pubkey': '09e43966f3df1914d745c0d8b2364c26c468493054198f583cb9f8f9689bbb25', 'value': 50000000000000}], 'type': 'transaction'}
transaction_3 ={'inputs': [{'outpoint': {'txid': 'cd01f1fb749531b9572d5cbe332bd6738efa897727dab729aebec3dfcc5f6c15', 'index': 0}, 'sig': '101844e20d8388d78651c3456b22e10d9330dfd1c538f2d172e46b76fbbde35b23b3b27a3434aa64b94c88b5400ac4be331e12999aaf7a3267ce6f4fb8a0aa07'}], 'outputs': [{'pubkey': '3bc6c0f9ffe9cde1bfa6e05258c7a1662deed8805d613ba1aa1dfc54ca175759', 'value': 50000000000000}], 'type': 'transaction'}
transaction_3_1 ={'inputs': [{'outpoint': {'txid': 'df3955e64c4cbecf88fd97eb24381e197e98f7432237a7c54a5e90a43c1c8aab', 'index': 0}, 'sig': '91e39c89822c18021b3818a0f79b19b6f72a2082906420ef3185a0a3d5247de2fb8e1d8b165f2f6c26edd07a261fb06a0ef4d91a4ac3b029846a6e4864c9a20e'}], 'outputs': [{'pubkey': 'a0741c78bb92c47d69143884055c63b4b1dee6507e1a110949931e31ada59922', 'value': 50000000000000}], 'type': 'transaction'}



c1 = {'height': 1, 'outputs': [{'pubkey': 'c69b14ea17121364f5d450676ae2634e784ccb2a88661cd9e7392efb33883fa2', 'value': 50000000000000}], 'type': 'transaction'}
c2 = {'height': 2, 'outputs': [{'pubkey': '2af246a26e51cd2bf0be582689c3a7ee9fa728768803d4d273e09064acfbc982', 'value': 50000000000000}], 'type': 'transaction'}
c3 = {'height': 4, 'outputs': [{'pubkey': '9c80ecb77cbc4472f40b8eb0cce4cad0283ee95aef8ea4a36a87d678ce8d324e', 'value': 50000000000000}], 'type': 'transaction'}