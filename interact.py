from web3 import Web3
from dotenv import load_dotenv
import os
import json

# Now Change the Greeting Value


def update_greet(newValue, w3, contract_instance):
    # Ensure New Variable is a String
    if type(newValue) != str:
        print("Invalid Type")
        return
    else:
        # Get Private Key
        private_key = os.getenv('private_key')
        wallet = "0x1f472D2550744f20C13Ac525fa365Ad88317078A"
        nonce = w3.eth.getTransactionCount(wallet)

        # Build Transaction for changing variable greets
        greet_transaction = contract_instance.functions.changeGreet(newValue).buildTransaction(
            {
                "gasPrice": w3.eth.gas_price,
                "chainId": 42,
                "from": wallet,
                "nonce": nonce,
            }
        )
        # Sign the Transaction
        signed_transaction = w3.eth.account.sign_transaction(
            greet_transaction, private_key=private_key)

        transaction_hash = w3.eth.send_raw_transaction(
            signed_transaction.rawTransaction)

        transaction_recipt = w3.eth.wait_for_transaction_receipt(
            transaction_hash)


def main():
    # Load Infura ID
    load_dotenv()
    infura_id = os.getenv('INFURA_ID')

    with open('FirstDeploy.json', 'r') as file:
        compiled_sol = json.load(file)

    # Get the ABI
    abi = compiled_sol['contracts']['FirstDeploy.sol']['FirstDeploy']['abi']

    # Connect Using Infura ID
    w3 = Web3(Web3.HTTPProvider(infura_id))

    # Get the Contract Instance Using
    contract_instance = w3.eth.contract(
        address='0x15EA2F65225267906465c30D9FA84e8ADD7dF2C9', abi=abi)

    # Print the Original Greeting Value
    print(contract_instance.functions.getGreet().call())

    # Update the state of greet variable
    update_greet("Hello, but change it", w3, contract_instance)

    # Print the Updated Greeting Value
    print(contract_instance.functions.getGreet().call())


if __name__ == "__main__":
    main()
