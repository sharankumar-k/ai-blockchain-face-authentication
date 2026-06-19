from web3 import Web3
import json

# -------------------------------
# Ganache & Contract details
# -------------------------------
GANACHE_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "YOUR_CONTRACT_ADDRESS"

# -------------------------------
# Web3 connection
# -------------------------------
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
assert w3.is_connected(), "Ganache is not running"

# -------------------------------
# Load ABI
# -------------------------------
with open("../blockchain/abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)

# Default Ganache account
ACCOUNT = w3.eth.accounts[0]

# -------------------------------
# Register face hash on blockchain (EMAIL + HASH)
# -------------------------------
def register_face_hash(email, face_hash):
    tx = contract.functions.registerFace(email, face_hash).transact({
        "from": ACCOUNT
    })
    w3.eth.wait_for_transaction_receipt(tx)

# -------------------------------
# Verify integrity using blockchain (EMAIL + HASH)
# -------------------------------
def verify_face_hash(email, face_hash):
    return contract.functions.verifyFace(email, face_hash).call({
        "from": ACCOUNT
    })

# -------------------------------
# Optional: Get stored hash (debug)
# -------------------------------
def get_blockchain_hash(email):
    return contract.functions.getHash(email).call()
