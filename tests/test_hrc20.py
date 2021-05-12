#coding:utf8
#author: yqq
#date: 2020/12/17 下午5:41
#descriptions: test web3
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

ABI, BYTECODES = parse_truffe_compile_outputs('./AJCToken.json')

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
    g_contract_address.append( contract_address)

    pass





def test_hrc20_name():
    contract_address = g_contract_address[0]
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)


    hc = HtdfContract(rpc=htdfrpc, address=Address(contract_address), abi=ABI)

    name  =hc.call( hc.functions.name() )
    print(name)
    assert name == "AJC chain"
    pass

def test_hrc20_symbol():
    contract_address = g_contract_address[0]
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)


    hc = HtdfContract(rpc=htdfrpc, address=Address(contract_address), abi=ABI)

    symbol = hc.call(hc.functions.symbol())
    print(symbol)
    assert symbol == "AJC"

    pass

def test_hrc20_totalSupply():
    contract_address = g_contract_address[0]
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)


    hc = HtdfContract(rpc=htdfrpc, address=Address(contract_address), abi=ABI)

    totalSupply = hc.call(hc.functions.totalSupply())
    print(totalSupply)
    assert totalSupply == int(199000000 * 10**18)
    pass

def test_hrc20_decimals():
    contract_address = g_contract_address[0]
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)


    hc = HtdfContract(rpc=htdfrpc, address=Address(contract_address), abi=ABI)

    totalSupply = hc.call(hc.functions.decimals())
    print(totalSupply)
    assert totalSupply == int(18)
    pass



def test_hrc20_balanceOf():
    contract_address = g_contract_address[0]
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)


    hc = HtdfContract(rpc=htdfrpc, address=Address(contract_address), abi=ABI)

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    cfnBalanceOf = hc.functions.balanceOf(_owner= to_checksum_address( from_addr.hex_address))
    balance = hc.call(cfn=cfnBalanceOf )
    print(type(balance))
    print(balance)
    assert balance == int(199000000 * 10**18)
    pass

def test_hrc20_transfer():
    contract_address = g_contract_address[0]
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=Address(contract_address), abi=ABI)


    new_to_addr = HtdfPrivateKey('').address

    transfer_tx = hc.functions.transfer(
        _to=to_checksum_address(new_to_addr.hex_address),
        _value=(10001*10**18)).\
        buildTransaction_htdf()

    data = remove_0x_prefix(transfer_tx['data'])

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
        memo='test_hrc20_transfer'
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))
    # self.assertTrue( len(tx_hash) == 64)

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    cfnBalanceOf = hc.functions.balanceOf(_owner=to_checksum_address(new_to_addr.hex_address))
    balance = hc.call(cfn=cfnBalanceOf)
    print(balance)

    pass



def test_hrc20_approve_transferFrom():

    # ownerAddress
    contract_address = g_contract_address[0]
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=Address(contract_address), abi=ABI)


    #
    new_to_priv_key = HtdfPrivateKey('')
    new_to_addr = new_to_priv_key.address


    approve_tx = hc.functions.approve(
        _spender=to_checksum_address(new_to_addr.hex_address),
        _value=(10002*10**18)).\
        buildTransaction_htdf()

    data = remove_0x_prefix(approve_tx['data'])

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfTxBuilder(
        from_address=from_addr,
        to_address=Address( contract_address),
        amount_satoshi=0,
        sequence=from_acc.sequence,
        account_number=from_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=200000,
        data=data,
        memo='test_hrc20_approve'
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))
    # self.assertTrue( len(tx_hash) == 64)

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)



    # transfer some htdf  for fee
    signed_tx = HtdfTxBuilder(
        from_address=from_addr,
        to_address=new_to_addr,
        amount_satoshi=200000*100,
        sequence=from_acc.sequence + 1,
        account_number=from_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=200000,
        data='',
        memo='some htdf for fee'
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))
    # self.assertTrue( len(tx_hash) == 64)

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)



    # cfnBalanceOf = hc.functions.balanceOf(_owner=to_checksum_address(new_to_addr.hex_address))
    # balance = hc.call(cfn=cfnBalanceOf)
    # print(balance)
    time.sleep(8)

    transferFrom_tx = hc.functions.transferFrom(
        _from=to_checksum_address( from_addr.hex_address),
        _to= to_checksum_address(new_to_addr.hex_address),
        _value = (10002*10**18)
    ).buildTransaction_htdf()
    data = remove_0x_prefix(transferFrom_tx['data'])


    to_acc_new = htdfrpc.get_account_info(address=new_to_addr.address)
    signed_tx = HtdfTxBuilder(
        from_address=new_to_addr,
        to_address=Address(contract_address),
        amount_satoshi=0,
        sequence=to_acc_new.sequence,
        account_number=to_acc_new.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=200000,
        data=data,
        memo='test_hrc20_transferFrom'
    ).build_and_sign(private_key=new_to_priv_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))
    # self.assertTrue( len(tx_hash) == 64)

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    cfnBalanceOf = hc.functions.balanceOf(_owner=to_checksum_address(new_to_addr.hex_address))
    balance = hc.call(cfn=cfnBalanceOf)
    print(balance)

    pass



def main():
    test_deploy_contract()
    test_hrc20_name()
    test_hrc20_symbol()
    test_hrc20_totalSupply()
    test_hrc20_decimals()
    test_hrc20_balanceOf()

    test_hrc20_transfer()
    test_hrc20_approve_transferFrom()

    pass


if __name__ == '__main__':
    main()
    pass
