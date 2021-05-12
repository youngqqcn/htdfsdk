# coding:utf8
# author: yqq
# date: 2020/12/17 下午5:41
# descriptions: test web3
import json
import time
from pprint import pprint

from eth_typing import URI
from htdfsdk import to_checksum_address, remove_0x_prefix

from htdfsdk import Address, HtdfRPC, HtdfPrivateKey, HtdfTxBuilder, htdf_to_satoshi
from htdfsdk import HtdfContract
from htdfsdk.web3 import Web3, HTTPProvider
from htdfsdk.web3.auto import w3


def parse_truffe_compile_outputs(json_path: str):
    with open(json_path, 'r') as infile:
        compile_outputs = json.loads(infile.read())
        abi = compile_outputs['abi']
        bytecode = compile_outputs['bytecode']
        bytecode = bytecode.replace('0x', '')
        return abi, bytecode


ABI, BYTECODES = parse_truffe_compile_outputs('./HtdfFaucet.json')

g_contract_address = []


def test_deploy_contract():
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)
    htdfcontract = HtdfContract(rpc=htdfrpc, address=None, abi=ABI, bytecode=BYTECODES)
    data = htdfcontract.constructor_data()
    # data = htdfcontract.contract_factory.constructor(amount=8899).data_in_transaction
    # data = htdfcontract.constructor.data_in_transaction()
    print(data)

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfTxBuilder(
        from_address=from_addr,
        to_address=None,
        amount_satoshi=0,
        sequence=from_acc.sequence,
        account_number=from_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=2000000,
        data=data,
        memo='test_deploy_contract'
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)
    log = tx['logs'][0]['log']
    conaddr = log[log.find("contract address:"): log.find(", output:")]
    contract_address = conaddr.replace('contract address:', '').strip()
    contract_address = Address.hexaddr_to_bech32(contract_address)

    print(contract_address)
    g_contract_address.append(contract_address)

    pass


def test_htdf_faucet_basic():
    address = g_contract_address[0]
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)

    htdfcontract = HtdfContract(rpc=htdfrpc, address=Address(address), abi=ABI)

    tx = htdfcontract.functions.owner().buildTransaction_htdf()
    print(tx)

    tx = htdfcontract.functions.setOnceAmount(amount=3 * 10 ** 8).buildTransaction_htdf()
    print(tx)

    cfnOwner = htdfcontract.functions.owner()
    calltx = htdfcontract.call(cfn=cfnOwner)
    print(calltx)

    cfnOnceAmount = htdfcontract.functions.onceAmount()
    calltx = htdfcontract.call(cfn=cfnOnceAmount)
    print(calltx)

    pass


def test_contract_htdf_faucet_deposit():
    contract_address = g_contract_address[0]
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=Address(contract_address), abi=ABI)

    deposit_tx = hc.functions.deposit().buildTransaction_htdf()
    data = remove_0x_prefix(deposit_tx['data'])

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfTxBuilder(
        from_address=from_addr,
        to_address=Address(contract_address),
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

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    # tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    # pprint(tx)
    pass


def test_contract_htdf_faucet_getOneHtdf():
    contract_address = g_contract_address[0]
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=Address(contract_address), abi=ABI)

    deposit_tx = hc.functions.getOneHtdf().buildTransaction_htdf()
    data = remove_0x_prefix(deposit_tx['data'])

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfTxBuilder(
        from_address=from_addr,
        to_address=Address(contract_address),
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

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    # tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    # pprint(tx)

    pass


def test_contract_htdf_faucet_setOnceAmount():
    contract_address = g_contract_address[0]
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=Address(contract_address), abi=ABI)

    deposit_tx = hc.functions.setOnceAmount(amount=int(3.5 * 10 ** 8)).buildTransaction_htdf()
    data = remove_0x_prefix(deposit_tx['data'])

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    # from_addr = Address('htdf1jrh6kxrcr0fd8gfgdwna8yyr9tkt99ggmz9ja2')
    # private_key = HtdfPrivateKey('485de9a2ee4ed834272389617da915da9176bd5281ec5d261256e15be0c375f2')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfTxBuilder(
        from_address=from_addr,
        to_address=Address(contract_address),
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

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    # tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    # pprint(tx)

    cfnOnceAmount = hc.functions.onceAmount()
    once_amount = hc.call(cfn=cfnOnceAmount)
    print("the latest onceAmount is ", once_amount)

    pass



def main():
    test_deploy_contract()
    test_htdf_faucet_basic()
    test_contract_htdf_faucet_deposit()
    test_contract_htdf_faucet_getOneHtdf()
    test_contract_htdf_faucet_setOnceAmount()

    pass


if __name__ == '__main__':
    main()
    pass
