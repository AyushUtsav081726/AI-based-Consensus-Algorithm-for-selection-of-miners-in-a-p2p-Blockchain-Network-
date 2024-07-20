import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
import threading
from flask import Flask, jsonify, request
from threading import Timer

import random
import timeit
import csv

from sklearn.cluster import KMeans
import pandas as pd

class Blockchain:
    array = []
    def __init__(self):
        self.stakers = dict()
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100,staker='none',staker_blocktime=0)
        self.register_node('http://127.0.0.1:5000')

    def register_node(self, address):

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):

        neighbours = self.nodes
        new_chain = None
        new_staker_list = None

        max_length = len(self.chain)

        stakerList = self.nodes
        staker_set_own = []

        for node in stakerList:
            staker_set_own.append(node)

        max_length_staker = len(staker_set_own)

        for node in neighbours:
            try:
                if(node!=url or len(neighbours)<=0):
                    response = requests.get(f'http://{node}/chain')
                    staker_res = requests.get(f'http://{node}/nodes/staker')

                if staker_res.status_code == 200:
                    staker_length = staker_res.json()['total_nodes']
                    staker_list = staker_res.json()['all_nodes']

                    if(staker_length > max_length_staker):
                        max_length_staker = staker_length
                        new_staker_list = staker_list

                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain
            except:
                break
            
        CheckResult = False

        if new_chain:
            self.chain = new_chain
            CheckResult = True

        if new_staker_list:
            self.nodes = set(new_staker_list)
            CheckResult = True

        return CheckResult

    def add_staker(self,address):

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.stakers[parsed_url.netloc] = 0
        elif parsed_url.path:
            self.stakers[parsed_url.netloc] = 0
        else:
            raise ValueError('Invalid URL')

    def new_block(self, proof, previous_hash,staker,staker_blocktime):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'staker':staker,
            'staker_time':staker_blocktime
        }

        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_stake_ai(self, last_block):

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/validate', methods=['GET'])
def validate():

    Stakers = list(blockchain.nodes)
    found=True
    # Replace here with ML Algorithm to get validator
    # validator = MLalgorithm()

    # Current System picks Random Stakers
    validator = Stakers[random.randrange(0, len(Stakers))]

    while(found):
        try:
            dataMiner = {'staker':validator} 
            response = requests.post(f'http://{validator}/mine',json=dataMiner)
            found=False
        except:
            validator = Stakers[random.randrange(0, len(Stakers))]
    
    if response.status_code == 200:
        message = response.json()['message']
        index = response.json()['index']
        transactions = response.json()['transactions']
        proof = response.json()['proof']
        previous_hash = response.json()['previous_hash']

        staker_set_own = blockchain.stakers

        if validator in staker_set_own:
            staker_set_own.update({validator:staker_set_own[validator]+1})

    response = {
        'validator': validator,
        'message': message,
        'index': index,
        'transactions': transactions,
        'proof': proof,
        'previous_hash': previous_hash,
    }
    return jsonify(response), 200

@app.route('/mine', methods=['POST'])
def mine():

    start = timeit.timeit()
    values = request.get_json()
    staker = values.get('staker')
    if staker is None:
        return "Error: Please supply a valid list of nodes", 400

    last_block = blockchain.last_block
    proof = blockchain.proof_of_stake_ai(last_block)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    end = timeit.timeit()
    duration = end - start
    block = blockchain.new_block(proof, previous_hash,staker,duration)
    end = 0 
    start = 0

    response = {
        'staker':staker,
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        print(k)
        return 'Missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/staker', methods=['GET'])
def list_nodes():

    Staker_list=[]
    for node in blockchain.nodes:
        Staker_list.append(node)

    response = {
        'message': 'List of Staker Nodes',
        'all_nodes': Staker_list,
        'total_nodes': len(Staker_list)
    }

    return jsonify(response), 200


@app.route('/stakerdetails', methods=['GET'])
def staker_details():
    chain = blockchain.chain
    stakerDetails = []
    stakerList = set()
    newdetails = {}
    for block in chain:
        # print('- - - - -')
        if(block['index']>1):
            if(block['staker'] not in stakerList):
                stakerList.add(block['staker'])
                newdetails = {
                    'staker': block['staker'],
                    'blocks': 1,
                    'age':0,
                    'faults':0,
                    'time':block['staker_time']
                }
                stakerDetails.append(newdetails)
                newdetails = {}
            else:
                for s in stakerDetails:
                    if(s['staker'] == block['staker']):
                        s['blocks']+=1
                        s['age']=len(chain)-block['index']
                        s['time']+=block['staker_time']
    
    # print(stakerList)
                
    response = {
        'stakerDetails':stakerDetails
    }

    return jsonify(response), 200

def consensus():
    blockchain.resolve_conflicts()

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def displaynow():
    print("Testing BAT")

def staker_details_function():
    chain = blockchain.chain
    stakerDetails = []
    stakerList = set()
    newdetails = {}
    for block in chain:
        if(block['index']>1):
            if(block['staker'] not in stakerList):
                stakerList.add(block['staker'])
                newdetails = {
                    'staker': block['staker'],
                    'blocks': 1,
                    'age':0,
                    'faults':0,
                    'time':block['staker_time']
                }
                stakerDetails.append(newdetails)
                newdetails = {}
            else:
                for s in stakerDetails:
                    if(s['staker'] == block['staker']):
                        s['blocks']+=1
                        s['age']=len(chain)-block['index']
                        s['time']+=block['staker_time']

    return stakerDetails

@app.route('/savetocsv', methods=['GET'])
def convertCSV():
    stakers_dict = staker_details_function()

    csv_file = "Blockchain_Dataset.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['staker','blocks','age','faults','time'])
            writer.writeheader()
            for data in stakers_dict:
                writer.writerow(data)
        response = {
            'message':'File Saved to CSV'
        }
        return jsonify(response), 200
    except IOError:
        response = {
            'message':'I/O error'
        }
        print("I/O error")
        return jsonify(response), 404




if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    url = 'http://127.0.0.1:'+ str(port)

    set_interval(consensus,5)
    blockchain.add_staker(url)
    if(port!=5000):
        jsonINFO = {"nodes": [url]} 
        requests.post('http://127.0.0.1:5000/nodes/register',json=jsonINFO)
        blockchain.register_node(url)

    app.run(host='127.0.0.1', port=port)
