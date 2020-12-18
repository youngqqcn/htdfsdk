#coding:utf8
#author: yqq
#date: 2020/12/17 下午5:41
#descriptions: test web3
import json

from eth_typing import URI
from eth_utils import to_checksum_address

from htdfsdk import Address
from htdfsdk.contract import HtdfContract
from web3 import Web3, HTTPProvider
from web3.auto import w3


myweb3 = Web3(provider=HTTPProvider(endpoint_uri=URI('https://rinkeby.infura.io/v3/314aa8d6c0f4433b8f5c43c3c7e5c1e4')))


def getOwner():
    address = to_checksum_address("0x7174f4cE494f1577e4baeF5b22C7Bb23d1199845")

    with open('./htdf_abi_faucet.json', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    # 获取ownerAddress
    contract = myweb3.eth.contract(address=address, abi=abi)
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



def test_htdf_contract():
    # address = to_checksum_address("0x7174f4cE494f1577e4baeF5b22C7Bb23d1199845")

    with open('./htdf_abi_faucet.json', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    # 获取ownerAddress
    # contract = myweb3.eth.contract(address=address, abi=abi)
    # owner = contract.functions.owner().call()
    address = Address("htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml")
    htdfcontract = HtdfContract(address=address, abi=abi)
    pass


def main():
    # getOwner()
    test_htdf_contract()

    pass


if __name__ == '__main__':
    main()
    pass
