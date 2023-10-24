"""
@author Ras Dwivedi
@date 21/10/2023

This file deploys the contract in contract.sol and updates the contract address and abi
"""
# Dependencies
import datetime
from web3 import Web3
from web3.middleware import geth_poa_middleware
# import logging
import json
import solcx
import os
import datetime
from config import RPCaddress
from eth_account import Account
import logging

logger = logging.getLogger(__name__)
# constants
FILES_TO_COMPILE = ["contract.sol"]
# connect to node
w3 = Web3(Web3.HTTPProvider(RPCaddress))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check if connected
if w3.is_connected():
    logger.info("Connected to Quorum node")
else:
    logger.error("Not connected to Quorum node, exiting")
    exit(0)

# OWNER_ACCOUNT = w3.eth.account.privateKeyToAccount("0x12126974647d010ab7999fda600004e4fe0550000075343f1508f8c100000000")
# w3.eth.defaultAccount = OWNER_ACCOUNT
w3.eth.defaultAccount = w3.eth.accounts[0]
print(w3.eth.defaultAccount)
print(w3.eth.accounts)


# in case of multiple files, you can add more files
def get_compiled_contracts():
    """
    This function returns a dictionary of all the compiled contracts, their ABI and bytecode.
    It uses the solcx library to compile the contracts specified in the FILES_TO_COMPILE variable.
    The returned dictionary has the
    contract name as the key and a dictionary containing the ABI and bytecode as the value.
    Additionally, it saves the contracts to the local storage using the save_contract function.
    :return: A dictionary with contract name as the key and a dictionary containing the ABI and bytecode as the value.
    """
    solc_version = "0.5.16"  # Replace with the desired Solidity version
    solcx.install_solc(solc_version)
    solcx.set_solc_version(solc_version)
    _compiled_contracts = solcx.compile_files(FILES_TO_COMPILE,
                                              output_values=["abi", "bin"])

    # save abi in contract abi
    for key in _compiled_contracts:
        abi = _compiled_contracts.get(key).get('abi')
        bin = _compiled_contracts.get(key).get('bin')
    # print(abi)
    f = open("./contract-abi.json", "w")
    f.write(json.dumps(abi))
    f.close()
    f = open("./contract-byte-code.json", "w")
    f.write(str(bin))
    f.close()
    # in case of multiple files, need to update this code
    # returning the abi and the bytecode
    return abi, bin


def deploy_contract(abi, bytecode):
    """
    This function deploys a contract to the Ethereum network.
    It takes in the ABI and bytecode of the contract and uses them to create a contract instance.
    It estimates the gas required for the deployment and builds the deployment transaction.
    The deployment transaction is signed by the owner account and sent to the Ethereum network.
    The function returns the address of the deployed contract.
    :param abi: The ABI of the contract
    :param bytecode: The bytecode of the contract
    :return: The address of the deployed contract.
    """
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    gas_estimate = contract.constructor().estimate_gas()
    print("gas estimate is ", gas_estimate)
    transaction = contract.constructor().build_transaction({
        'from': w3.eth.defaultAccount,
        'chainId': 1337,
        'gas': gas_estimate,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(w3.eth.defaultAccount)
    })
    # print(f"nonce received was {w3.eth.getTransactionCount(OWNER_ACCOUNT.address)}")

    # signed_transaction = w3.eth.account.sign_transaction(transaction, w3.eth.defaultAccount.privateKey)

    # Send the signed transaction
    # tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    tx_hash = w3.eth.send_transaction(transaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Check if the contract was deployed successfully
    contract_address = tx_receipt['contractAddress']
    if contract_address is None:
        raise Exception("Contract deployment failed")

    # Write the contract address to a JSON file
    with open("./contract-address.json", "w") as f:
        f.write(json.dumps({'address': contract_address}))

    return contract_address

    # signed_transaction = w3.eth.account.signTransaction(transaction, w3.eth.defaultAccount.privateKey)
    #
    # # Send the signed transaction
    # tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # contract_address = tx_receipt['contractAddress']
    # if contract_address is None:
    #     raise Exception("contract deployment failed")
    # f = open("./contract-address.json", "w")
    # f.write(json.dumps({'address': contract_address}))
    # f.close()
    # return contract_address


def main():
    """
    The main function
    """
    # os.system('rm logs.log')
    start_time = st = datetime.datetime.now()
    print("Compiling contracts")
    abi, bin = get_compiled_contracts()
    print("Contracts compiled")
    # f=open('../build/contract_address/addresses.txt')
    # contract_addresses = json.loads(f.read())
    contract_address = deploy_contract(abi, bin)
    print("Contracts deployed")
    print(contract_address)
    # logger.info(contract_addresses)
    # print(json.dumps(contract_addresses))
    # f = open('../build/contract_address/addresses.txt', 'w')
    # f.write(json.dumps(contract_addresses))
    # f.close()
    end_time = datetime.datetime.now()
    # print("instantiating")
    # instantiate(contract_addresses, compiled_contracts)
    print("total execution time: ", end_time - start_time)
    print("last mined block after instantiation was ", w3.eth.block_number)


if __name__ == "__main__":
    main()