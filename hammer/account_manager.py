"""
@author Ras Dwivedi
@date 21/10/2023

This file deploys the contract in contract.sol and updates the contract address and abi
"""
# Dependencies
import datetime
from web3 import Web3
# import logging
import datetime
from config import RPCaddress
from eth_account import Account
import logging
logger = logging.getLogger(__name__)
#constants
FILES_TO_COMPILE = ["contract.sol"]
# connect to node
w3 = Web3(Web3.HTTPProvider(RPCaddress))
# w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check if connected
if w3.isConnected():
    logger.info("Connected to Quorum node")
else:
    logger.error("Not connected to Quorum node, exiting")
    exit(0)
    
OWNER_ACCOUNT = w3.eth.account.privateKeyToAccount("0x12126974647d010ab7999fda600004e4fe0550000075343f1508f8c100000000")
w3.eth.defaultAccount = OWNER_ACCOUNT
