from importlib.resources import path
from dotenv import load_dotenv
import os
from web3 import Web3
from solcx import compile_standard
import json


def deploy_contract(w3, private_key, infura_id):
    with open('FirstDeploy.sol', 'r') as file:
        contract_file = file.read()

    compiled_solidity = compile_standard({
        "language": "Solidity",
        "sources": {"FirstDeploy.sol": {"content": contract_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        }
    }, solc_version="0.8.12")

    with open('FirstDeploy.json', 'w') as file:
        json.dump(compiled_solidity, file)

    bytecode = compiled_solidity['contracts']['FirstDeploy.sol']['FirstDeploy']['evm']['bytecode']['object']
    abi = compiled_solidity['contracts']['FirstDeploy.sol']['FirstDeploy']['abi']
    deploy = w3.eth.contract(abi=abi, bytecode=bytecode)
    wallet = "0x1f472D2550744f20C13Ac525fa365Ad88317078A"
    nonce = w3.eth.getTransactionCount(wallet)

    transaction = deploy.constructor().buildTransaction(
        {
            'gasPrice': w3.eth.gas_price,
            'chainId': 42,
            "from": wallet,
            "nonce": nonce,

        }
    )

    signed_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=private_key)

    trans_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(trans_hash)
    print(transaction_receipt)


def main():
    load_dotenv()
    # Get INFURA ID
    infura_id = os.getenv('INFURA_ID')
    private_key = os.getenv('private_key')

    # HTTP Providor
    w3 = Web3(Web3.HTTPProvider(infura_id))

    deploy_contract(w3, private_key, infura_id)


if __name__ == "__main__":
    main()
