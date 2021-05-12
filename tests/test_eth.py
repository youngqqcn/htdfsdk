#coding:utf8
#author: yqq
#date: 2021/5/12 下午4:55
#descriptions:

import json
from eth_typing import URI
from htdfsdk import to_checksum_address

from htdfsdk.web3 import Web3, HTTPProvider

myweb3 = Web3(provider=HTTPProvider(endpoint_uri=URI('https://rinkeby.infura.io/v3/314aa8d6c0f4433b8f5c43c3c7e5c1e4')))

def parse_truffe_compile_outputs(json_path: str):
    with open(json_path, 'r') as infile:
        compile_outputs = json.loads(infile.read())
        abi = compile_outputs['abi']
        bytecode = compile_outputs['bytecode']
        bytecode = bytecode.replace('0x', '')
        return abi, bytecode

ABI, BYTECODES = parse_truffe_compile_outputs('./HtdfFaucet.json')

def getOwner():
    address = to_checksum_address("0x7174f4cE494f1577e4baeF5b22C7Bb23d1199845")

    contract = myweb3.eth.contract(address=address, abi=ABI)
    owner = contract.functions.owner().call()
    print(owner)

    transaction = contract.functions.owner().buildTransaction({
        # 'value': 0,
        # 'gas': 150000,
        # 'gasPrice': 100,
        'nonce': 10
    })
    print(transaction)

    pass



def main():
    getOwner()
    pass


if __name__ == '__main__':
    main()
    pass
