import copy
import sqlite3

import constants as const
import objects
import objects

# get expanded object for 
def fetch_object(oid: str, cur: sqlite3.Cursor) -> dict:
    res = cur.execute("SELECT obj FROM objects WHERE oid = ?", (oid,))
    first_res = res.fetchone()

    if first_res is None:
        raise Exception(f"Object with id {oid} does not exist!")

    return objects.expand_object(first_res[0])

# get utxo for block
def fetch_utxo(bid: str, cur: sqlite3.Cursor) -> list:
    res = cur.execute("SELECT utxoset FROM utxo WHERE blockid = ?", (bid,))
    first_res = res.fetchone()

    if first_res is None:
        raise Exception(f"Block with id {bid} does not exist!")
    
    return objects.expand_object(first_res[0])


def get_all_ancestors(blockid):
    ancestors = []

    con = sqlite3.connect(const.DB_NAME)
    try:
        cur = con.cursor()

        while blockid != const.GENESIS_BLOCK_ID:
            block = fetch_object(blockid, cur)
            print(block)
            if block is None:
                return None

            ancestors.append(block)
            blockid = block['previd']

        return ancestors

    finally:
        con.close()


# return a list of transactions by index
def find_all_txs(txids):
    txs = []
    
    con = sqlite3.connect(const.DB_NAME)
    try:
        cur = con.cursor()
        
        for txid in txids:
            txs.append(fetch_object(txid, cur))
    finally:
        con.close()

    return txs

# return a list of transactions in blocks
def get_all_txids_in_blocks(blocks: list) -> list:
    txids = []
    
    for block in blocks:
        txids.extend(block['txids'])

    return txids

def find_lca_and_intermediate_blocks(tip, blockid):

    con = sqlite3.connect(const.DB_NAME)
    try:
        cur = con.cursor()

        # Get all ancestors for both blocks
        all_old_blocks = get_all_ancestors(tip)
        all_new_blocks = get_all_ancestors(blockid)
        new_blocks = []
        old_blocks = []

        # Find the LCA of the two blocks
        lca = const.GENESIS_BLOCK
        for oldblock in all_old_blocks:
            for newblock in all_new_blocks:
                new_blocks.append(newblock)
                if newblock == oldblock:
                    lca = newblock
                    break
        
        for oldblock in all_old_blocks:
            for newblock in all_new_blocks:
                old_blocks.append(oldblock)
                if oldblock == lca:
                    break

        return lca, new_blocks, old_blocks

    finally:
        con.close()


def rebase_mempool(old_tip, new_tip, mptxids):
    lca, new_blocks, old_blocks = find_lca_and_intermediate_blocks(old_tip, new_tip)
    lca_id = objects.get_objid(lca)
    
    # Fetch the UTXO set at the LCA
    con = sqlite3.connect(const.DB_NAME)
    try:
        cur = con.cursor()
        new_utxo = fetch_utxo(new_tip, cur)
    

        # Create a new mempool with the UTXO set at the LCA
        new_mempool = Mempool(new_tip, new_utxo)
        
        
        # Apply the transactions from the new blocks to the new UTXO set
        for block in reversed(new_blocks):
            for txid in block['txids']:
                tx = fetch_object(txid, cur)
                new_mempool.try_add_tx(tx)

        for block in reversed(old_blocks):
            for txid in block['txids']:
                tx = fetch_object(txid, cur)
                new_mempool.try_add_tx(tx)
        
        # Re-add transactions from the old mempool to the new mempool state
        for txid in mptxids:
            tx = fetch_object(txid, cur)
            new_mempool.try_add_tx(tx)
    finally:    
        con.close()
    
    return new_mempool

# Meaning of the param (probably)
# Base Block ID: The hash or identifier of the block that the mempool is currently based on.
# Base UTXO set: The current state of unspent transaction outputs. Represents available funds.
class Mempool:
    def __init__(self, bbid: str, butxo: dict):
        self.base_block_id = bbid
        self.utxo = butxo
        self.txs = []

    def try_add_tx(self, tx: dict) -> bool:
        if 'height' in tx:
            return False
        
        txid = objects.get_objid(tx)

        # Check if utxos are available and remove them
        for input in tx['inputs']:
            in_txid = input['outpoint']['txid']
            in_index = f"{input['outpoint']['index']}"

            if in_txid not in self.utxo:
                return False
            
            if in_index not in self.utxo[in_txid]:
                return False

            del self.utxo[in_txid][in_index]

            if len(self.utxo[in_txid]) == 0:
                del self.utxo[in_txid]

        # Add new utxos
        for out_index in range(len(tx['outputs'])):
            out = tx['outputs'][out_index]

            if txid not in self.utxo:
                self.utxo[txid] = dict()

            self.utxo[txid][f"{out_index}"] = out['value']

        self.txs.append(txid)
        return True

    def rebase_to_block(self, new_tip: str):
        old_tip = self.base_block_id
        new_mempool = rebase_mempool(old_tip, new_tip, self.txs)
        
        # Update the mempool state
        self.base_block_id = new_mempool.base_block_id
        self.utxo = new_mempool.utxo
        self.txs = new_mempool.txs
