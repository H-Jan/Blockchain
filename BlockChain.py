
#Blockchain class
class Blockchain(object):
    def __init__(self):
        #Initial Chain and Trasnaction list
        self.chain=[]
        self.current_transactions=[]
        #Genesis Block
        self.new_block(previous_hash=1, proof=100)

    def proof_of_work(self, last_proof):
        #Consensus algorithm
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        #Validates blocks
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexigest()
        return guess_hash[:4] == "0000"

    def new_block(self, proof, previous_hash=None):
        #Creates new blocks and adds to existing chain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,
            previous_hash: previous_hash or self.hash(self.chain[-1])
        }
        self.current_transactions=[]
        self.chain.append(block)
        return block

    def new_transaction(self):
        #Adds a new transaction to existing transactions
        #Transactions will be sent to the next block, containing sender, recepient, amount
        self.current_transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            }
        )
        return self.last_block['index']+1
        #Simply appends current transaction list with an object containing specified details

    @staticmethod
    def hash(block):
        #Hashing blocks
        #Creates a SHA-256 block hash and ensures dictionary is ordered
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        #Calls and returns the last block of the chain
        return self.chain[-1]

#---------------------- API Integration ----------------------#

# Creating the app node
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-','')
# Initializing blockchain
blockchain = Blockchain()
@app.route('/mine', methods=['GET'])
def mine():
   #Proof of Work Algorithm
   last_block = blockchain.last_block
   last_proof = last_block['proof']
   proof = blockchain.proof_of_work(last_proof)

   #Miner Reward for Contribution
   blockchain.new_transaction(
       sender="0",
       recipient = node_identifier,
       amount = 1,
   )

   #Creation of New Block and Added to Chain
   previous_hash = blockchain.hash(last_block)
   block = blockchain.new_block(proof, previous_hash)
   response = {
       'message': 'The new block has been forged',
       'index': block['index'],
       'transactions': block['transactions'],
       'proof': block['proof'],
       'previous_hash' : block['previous_hash']
   }
   return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    #Checking if required data is there
    required=['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing Values', 400
    
    #Creating new transaction
    index = blockchian.new_transaction(values['sender'], values['recipient', values['amount']])
    response = {'message': f'TRansaction is scheduled to be added to Block No. {index}'}
    return jsonify(response), 201

@app.router('/chain', methods=['GET'])
def full_chain():
   response = {
       'chain' : blockchain.chain,
       'length' : len(blockchain.chain)
   }
   return jsonify(response), 200

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)






