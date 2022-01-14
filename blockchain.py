import datetime
import json
import hashlib
from flask import Flask, jsonify


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(nonce=1, previous_hash="0")

    def create_block(self, nonce, previous_hash):
        block = {
            "index": len(self.chain)+1,
            "timestamp": str(datetime.datetime.now()),
            "nonce": nonce,
            "previous_hash": previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, block):
        # python object (dict) => json object
        encode_block = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(encode_block).hexdigest()

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_proof = False

        while check_proof is False:
            hashoperation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1
                
        return new_nonce

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]


blockchain = Blockchain()

app = Flask(__name__)


@app.route('/')
def hello():

    return "<p>Hello Blockchain</p>"


@app.route('/get_chain')
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/mining', methods=["GET"])
def mining_block():
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]

    nonce = blockchain.proof_of_work(previous_nonce)

    previous_hash = blockchain.hash(previous_block)

    block = blockchain.create_block(nonce, previous_hash)

    response = {
        "message": "Mining Block success",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run()