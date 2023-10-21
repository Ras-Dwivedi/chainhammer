#!/usr/bin/env python3
"""
@summary: submit many contract.set(arg) transactions to the example contract

@version: v52 (22/January/2019)
@since:   17/April/2018
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

# extend sys.path for imports:
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

################
## Dependencies:

# standard library:
import sys, time, random, json
from threading import Thread
from queue import Queue
from pprint import pprint
import random

# pypi:
import requests # pip3 install requests
import web3
from web3 import Web3, HTTPProvider # pip3 install web3
from web3.utils.abi import filter_by_name, abi_to_signature
from web3.utils.encoding import pad_hex

# chainhammer:
from hammer.config import RPCaddress, ROUTE, PRIVATE_FOR, EXAMPLE_ABI
from hammer.config import PARITY_UNLOCK_EACH_TRANSACTION
from hammer.config import GAS_FOR_SET_CALL
from hammer.config import FILE_LAST_EXPERIMENT, EMPTY_BLOCKS_AT_END
from hammer.deploy import loadFromDisk
from hammer.clienttools import web3connection, unlockAccount


##########################
## smart contract related:


def initialize_fromAddress():
    """
    initialise contract object from address, stored in disk file by deploy.py
    """
    contractAddress, abi = loadFromDisk()
    myContract = w3.eth.contract(address=contractAddress,
                                 abi=abi)
    return myContract
    


def contract_method_ID(methodname, abi):
    """
    build the 4 byte ID, from abi & methodname
    """
    method_abi = filter_by_name(methodname, abi)
    
    assert(len(method_abi)==1)
    method_abi = method_abi[0]
    method_signature = abi_to_signature(method_abi) 
    method_signature_hash_bytes = w3.sha3(text=method_signature) 
    method_signature_hash_hex = w3.toHex(method_signature_hash_bytes)
    method_signature_hash_4bytes = method_signature_hash_hex[0:10]
    return method_signature_hash_4bytes

def argument_encoding(contract_method_ID,arg ):
    """
    concatenate method ID + padded parameter
    """
    arg_hex = w3.toHex(arg)
    arg_hex_padded = pad_hex ( arg_hex, bit_size=256)
    data = contract_method_ID + arg_hex_padded [2:]
    return data
  
    
def fetch_function_value_from_contract(contract_address, abi):
    
    method_ID = contract_method_ID("getDRCInfo", abi) 
    data = argument_encoding(method_ID,1)

    # myContract = web3.eth.contract(address=contract_address,abi=abi) 
    # myvalue = myContract.functions.getDRCInfo(1).call()
    # print(myvalue)   
    print(data, w3.eth.accounts[0],contract_address)
    txParameters = {
        'from': w3.eth.accounts[0], 
        'to': contract_address,
        'data': data
    } 

    call_function = w3.eth.call(txParameters) 
    print(call_function)
    return call_function



if __name__ == '__main__':
    

    global w3, NODENAME, NODETYPE, NODEVERSION, CONSENSUS, NETWORKID, CHAINNAME, CHAINID
    w3, chainInfos = web3connection(RPCaddress=RPCaddress, account=None)
    NODENAME, NODETYPE, NODEVERSION, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos
    
    w3.eth.defaultAccount = w3.eth.accounts[0] # set first account as sender
    contract = initialize_fromAddress()
    txs = fetch_function_value_from_contract('0x342B9eaFC75f7765240D7193f28157DFAbc55Db7', contract.abi)
    sys.stdout.flush() # so that the log files are updated.

    