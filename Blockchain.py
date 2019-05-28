import datetime
import hashlib
import json
from flask import flask, jsonify


class blockchain:
    def __init__(self):
        self.chain=[]
        self.create_block(proof=1, previous_hash='0')
    
    def create_block(self, proof, previous_hash):
        block={'index':len(self.chain)+1,'timestamp':str(datetime.datetime.now()),'proof':proof,'previous_hash':previous_hash }
        self.chain.append(block)
        return block
    def get_previous_block(self):
        return self.chain[-1]
   
   #This function is to check if the proof of work mined is valid 
    def proof_of_work(self, previous_proof):
        new_proof =1
        check_proof=False
        while check_proof is False:
            # Used a non-symmetric arithmetic so that the result of the arithmetic operation is not repititive
            # The idea is to make the operation tough to compute but easy to check 
            #str and encode functions are used to make the value compatible to what the hashlib.sha256() function is expecting
            # The hexdigest() function is for making the value in hexadecimal form
            hash_function = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

            #The check is for 4 leading zeros in this case as it any hash start with 4 leading zeros is considers a golden nuance
            #Since this is not a realtime blockchain the value is kept easier to compute for any system
            if hash_function[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof
    #Hash Function to get convert the existing blocks into their respective hashes
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    #Check if each block in the blockchain has the correct proof of work
    #Check if Previous Hash of each block is equal to the hash of previous block
    #Thereby making sure we have a valid blockchain
    def is_chain_valid(self, chain):
        previous_block=chain[0]
        block_index=1
        while block_index<= len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_function = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_function[:4]!='0000':
                return False
            previous_block = block
            block_index+=1
            return True
