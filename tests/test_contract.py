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


myweb3 = Web3(provider=HTTPProvider(endpoint_uri=URI('https://rinkeby.infura.io/v3/314aa8d6c0f4433b8f5c43c3c7e5c1e4')))


def getOwner():
    address = to_checksum_address("0x7174f4cE494f1577e4baeF5b22C7Bb23d1199845")

    with open('./htdf_faucet_sol_HtdfFaucet.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

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


hrc20_contract_address = ['htdf1k78exwfuta66m3sxgfjd6zuw8m7zykfmas0nrf']




def test_hrc20_name():

    with open('./AJC_sol_AJCToken.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    assert len(hrc20_contract_address) > 0
    contract_address = Address(hrc20_contract_address[0])
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)

    name  =hc.call( hc.functions.name() )
    print(name)
    assert name == "AJC chain"
    pass

def test_hrc20_symbol():
    with open('./AJC_sol_AJCToken.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    assert len(hrc20_contract_address) > 0
    contract_address = Address(hrc20_contract_address[0])
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)

    symbol = hc.call(hc.functions.symbol())
    print(symbol)
    assert symbol == "AJC"

    pass

def test_hrc20_totalSupply():
    with open('./AJC_sol_AJCToken.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    assert len(hrc20_contract_address) > 0
    contract_address = Address(hrc20_contract_address[0])
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)

    totalSupply = hc.call(hc.functions.totalSupply())
    print(totalSupply)
    assert totalSupply == int(199000000 * 10**18)
    pass

def test_hrc20_decimals():
    with open('./AJC_sol_AJCToken.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    assert len(hrc20_contract_address) > 0
    contract_address = Address(hrc20_contract_address[0])
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)

    totalSupply = hc.call(hc.functions.decimals())
    print(totalSupply)
    assert totalSupply == int(18)
    pass




def test_hrc20_balanceOf():
    with open('./AJC_sol_AJCToken.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    assert len(hrc20_contract_address) > 0
    contract_address = Address(hrc20_contract_address[0])
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    cfnBalanceOf = hc.functions.balanceOf(_owner= to_checksum_address( from_addr.hex_address))
    balance = hc.call(cfn=cfnBalanceOf )
    print(type(balance))
    print(balance)
    assert balance == int(199000000 * 10**18)
    pass

def test_hrc20_transfer():
    with open('./AJC_sol_AJCToken.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    assert len(hrc20_contract_address) > 0
    contract_address = Address(hrc20_contract_address[0])
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)


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
        to_address=contract_address,
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

    tx = htdfrpc.get_tranaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    cfnBalanceOf = hc.functions.balanceOf(_owner=to_checksum_address(new_to_addr.hex_address))
    balance = hc.call(cfn=cfnBalanceOf)
    print(balance)

    pass





def test_hrc20_approve_transferFrom():
    with open('./AJC_sol_AJCToken.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    # ownerAddress
    assert len(hrc20_contract_address) > 0
    contract_address = Address(hrc20_contract_address[0])
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)


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
        to_address=contract_address,
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

    tx = htdfrpc.get_tranaction_until_timeout(transaction_hash=tx_hash)
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

    tx = htdfrpc.get_tranaction_until_timeout(transaction_hash=tx_hash)
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
        to_address=contract_address,
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

    tx = htdfrpc.get_tranaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    cfnBalanceOf = hc.functions.balanceOf(_owner=to_checksum_address(new_to_addr.hex_address))
    balance = hc.call(cfn=cfnBalanceOf)
    print(balance)


    pass



def main():
    # getOwner()
    # test_htdf_contract()
    # test_contract_htdf_faucet_deposit()
    # test_contract_htdf_faucet_getOneHtdf()
    # test_contract_htdf_faucet_setOnceAmount()

    # test_hrc20_name()
    # test_hrc20_symbol()
    # test_hrc20_decimals()
    # test_hrc20_totalSupply()
    # test_hrc20_balanceOf()
    # test_hrc20_transfer()

    test_hrc20_approve_transferFrom()


    pass


if __name__ == '__main__':
    main()
    pass
