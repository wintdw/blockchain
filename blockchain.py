import block
import time

DIFF = 5

class Blockchain:
    def __init__(self):
        self.unconfirmed_txns = []
        self.chain = []
        self.genesis_block()

    def genesis_block(self):
        if len(self.chain) == 0: 
            b = block.Block(0, [], time.time(), "0")
            b.hash = b.compute_hash()
            self.chain.append(b)

    def last_block(self):
        return self.chain[-1]

    # Add txn to unconfirmed_txns
    def add_txn(self, sender, recp, amt):
        self.unconfirmed_txns.append({"sender": sender, "recipient": recp, "amount": amt})

    def get_unconfirmed_txns(self):
        return self.unconfirmed_txns

    def get_amount(self, user):
        amt = 0
        for block in self.chain:
            for txn in block.txns:
                if user == txn["sender"]:
                    amt -= txn["amount"]
                if user == txn["recipient"]:
                    amt += txn["amount"]
        return amt

    ##### Core of mining #####
    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * DIFF):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        prev_hash = self.last_block().hash
        if prev_hash != block.prev_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * DIFF) and block_hash == block.compute_hash())

    def mine(self):
        # nothing to confirm
        if not self.unconfirmed_txns:
            return False
        last_block = self.last_block()
        new_block = block.Block(last_block.index+1, self.unconfirmed_txns, time.time(), last_block.hash)
        proof = self.proof_of_work(new_block)
        success = self.add_block(new_block, proof)
        if success is True:
            self.unconfirmed_txns = []
        return new_block.index
    #####
