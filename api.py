import blockchain
import json
from fastapi import FastAPI

app = FastAPI()
blockchain = blockchain.Blockchain()

@app.get('/')
def get_chain():
    return blockchain.chain

def get_unconfirmed_txns():
    utxns = blockchain.get_unconfirmed_txns()
    return utxns

@app.get("/txn/{sender}/{recp}/{amt}")
def add_txn(sender: str, recp: str, amt: float):
    blockchain.add_txn(sender, recp, amt)
    return get_unconfirmed_txns()

@app.get('/mine')
def mine():
    blockchain.mine()
    return get_chain()

@app.get('/wallet/{user}')
def get_wallet(user):
    return blockchain.get_amount(user)
