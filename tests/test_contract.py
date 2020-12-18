#coding:utf8
#author: yqq
#date: 2020/12/17 下午5:41
#descriptions: test web3
import json
from pprint import pprint

from eth_typing import URI
from htdfsdk import to_checksum_address, remove_0x_prefix

from htdfsdk import Address, HtdfRPC, HtdfPrivateKey, HtdfTxBuilder, htdf_to_satoshi
from htdfsdk import HtdfContract
from htdfsdk.web3 import Web3, HTTPProvider
from htdfsdk.web3.auto import w3


myweb3 = Web3(provider=HTTPProvider(endpoint_uri=URI('https://rinkeby.infura.io/v3/314aa8d6c0f4433b8f5c43c3c7e5c1e4')))


def getOwner():
    address = to_checksum_address("0x7174f4cE494f1577e4baeF5b22C7Bb23d1199845")

    with open('./htdf_faucet_sol_HtdfFaucet.abi', 'r') as abifile:
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

    with open('./htdf_faucet_sol_HtdfFaucet.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    # 获取ownerAddress
    address = Address("htdf1wc4489xl37za6k8kk8y2tsce8aftdycxxk0saa")
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    htdfcontract = HtdfContract(rpc=htdfrpc, address=address, abi=abi)

    tx = htdfcontract.functions.owner().buildTransaction_htdf()
    print(tx)

    tx = htdfcontract.functions.setOnceAmount(amount=3*10**8).buildTransaction_htdf()
    print(tx)


    cfnOwner  =  htdfcontract.functions.owner()
    calltx = htdfcontract.call(cfn=cfnOwner)
    print(calltx)

    cfnOnceAmount = htdfcontract.functions.onceAmount()
    calltx = htdfcontract.call(cfn=cfnOnceAmount)
    print(calltx)

    pass




def test_contract_htdf_faucet_deposit():

    with open('./htdf_faucet_sol_HtdfFaucet.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    # 获取ownerAddress
    # contract = myweb3.eth.contract(address=address, abi=abi)
    # owner = contract.functions.owner().call()
    contract_address = Address("htdf1wc4489xl37za6k8kk8y2tsce8aftdycxxk0saa")
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)


    deposit_tx = hc.functions.deposit().buildTransaction_htdf()
    data = remove_0x_prefix(deposit_tx['data'])

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfTxBuilder(
        from_address=from_addr,
        to_address=contract_address,
        amount_satoshi=htdf_to_satoshi(20.12181447),
        sequence=from_acc.sequence,
        account_number=from_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=200000,
        data=data,
        memo='htdf_faucet.deposit()'
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))
    # self.assertTrue( len(tx_hash) == 64)

    tx = htdfrpc.get_tranaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    # tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    # pprint(tx)

    pass




def test_contract_htdf_faucet_getOneHtdf():

    with open('./htdf_faucet_sol_HtdfFaucet.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    # 获取ownerAddress
    # contract = myweb3.eth.contract(address=address, abi=abi)
    # owner = contract.functions.owner().call()
    contract_address = Address("htdf1wc4489xl37za6k8kk8y2tsce8aftdycxxk0saa")
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)


    deposit_tx = hc.functions.getOneHtdf().buildTransaction_htdf()
    data = remove_0x_prefix(deposit_tx['data'])

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfTxBuilder(
        from_address=from_addr,
        to_address=contract_address,
        amount_satoshi=0,
        sequence=from_acc.sequence,
        account_number=from_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=200000,
        data=data,
        memo='htdf_faucet.deposit()'
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))
    # self.assertTrue( len(tx_hash) == 64)

    tx = htdfrpc.get_tranaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    # tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    # pprint(tx)

    pass



def test_contract_htdf_faucet_setOnceAmount():

    with open('./htdf_faucet_sol_HtdfFaucet.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    # 获取ownerAddress
    # contract = myweb3.eth.contract(address=address, abi=abi)
    # owner = contract.functions.owner().call()
    contract_address = Address("htdf1wc4489xl37za6k8kk8y2tsce8aftdycxxk0saa")
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)


    deposit_tx = hc.functions.setOnceAmount(amount=int(3.5 * 10**8)).buildTransaction_htdf()
    data = remove_0x_prefix(deposit_tx['data'])

    # from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    # private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    from_addr = Address('htdf1jrh6kxrcr0fd8gfgdwna8yyr9tkt99ggmz9ja2')
    private_key = HtdfPrivateKey('485de9a2ee4ed834272389617da915da9176bd5281ec5d261256e15be0c375f2')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfTxBuilder(
        from_address=from_addr,
        to_address=contract_address,
        amount_satoshi=0,
        sequence=from_acc.sequence,
        account_number=from_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=200000,
        data=data,
        memo='htdf_faucet.deposit()'
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))
    # self.assertTrue( len(tx_hash) == 64)

    tx = htdfrpc.get_tranaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    # tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    # pprint(tx)

    cfnOnceAmount = hc.functions.onceAmount()
    once_amount = hc.call(cfn=cfnOnceAmount)
    print("the latest onceAmount is ", once_amount)

    pass


def main():
    # getOwner()
    test_htdf_contract()
    # test_contract_htdf_faucet_deposit()
    # test_contract_htdf_faucet_getOneHtdf()
    # test_contract_htdf_faucet_setOnceAmount()

    pass


if __name__ == '__main__':
    main()
    pass
