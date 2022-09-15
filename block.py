from hashlib import sha256
import json

class Block:
    def __init__(self, index, txns, ts, prev_hash, nonce=0):
        self.index = index
        self.ts = ts
        self.txns = txns
        self.prev_hash = prev_hash
        self.nonce = nonce

    def compute_hash(self):
        block_str = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_str.encode()).hexdigest()
