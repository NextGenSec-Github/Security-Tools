import hashlib
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f'{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}'
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        # Mining by trying different nonce values
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.create_genesis_block()

    def create_genesis_block(self):
        # Manually constructing a block with index zero and arbitrary previous hash
        genesis_block = Block(0, [], time.time(), '0'*64)
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check current block's hash
            if current.hash != current.calculate_hash():
                return False
            
            # Check block's hash with previous block's hash
            if current.previous_hash != previous.hash:
                return False
                
        return True

# Instantiate and test the blockchain
blockchain = Blockchain()
blockchain.add_block(Block(1, ['Ebear sends 5 BTC to Ebear1'], time.time(), blockchain.get_latest_block().hash))
# Modify the transactions in the second block to make it invalid
blockchain.add_block(Block(2, ['Ebear3 sends 100 BTC to Ebear2'], time.time(), blockchain.get_latest_block().hash))

# Check if the blockchain is valid
print('Is Blockchain valid?', blockchain.is_chain_valid())
