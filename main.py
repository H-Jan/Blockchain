
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






