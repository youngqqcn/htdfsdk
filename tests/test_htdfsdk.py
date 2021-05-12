import pytest
from pprint import pprint

from htdfsdk import HtdfRPC, HtdfTxBuilder, htdf_to_satoshi, Address, HtdfPrivateKey
from htdfsdk.htdfsdk import ValidatorAddress, HtdfDelegateTxBuilder, HtdfWithdrawDelegateRewardsTxBuilder, \
    HtdfSetUndelegateStatusTxBuilder, HtdfUndelegateTxBuilder, HtdfEditValidatorInfoTxBuilder


def test_PrivateKey():
    privkey = HtdfPrivateKey('')
    privkey2 = HtdfPrivateKey(privkey.private_key)
    print(privkey.private_key)
    print(privkey.address)
    assert  privkey == privkey2

    pk3 = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    addr3 = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    assert  pk3.address == addr3


def test_Address():
    bech32_address = 'htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml'
    addr1 = Address(address=bech32_address)
    hexaddr =  addr1.hex_address
    hex_address = Address.bech32_to_hexaddr(bech32_address=bech32_address)
    assert hex_address == '338300688033C44D2064413D08969956ABA7211C'
    assert hexaddr == '338300688033C44D2064413D08969956ABA7211C'

    bech32_address2 = addr1.hexaddr_to_bech32(hex_address='338300688033C44D2064413D08969956ABA7211C')
    assert bech32_address == bech32_address2


def test_htdf_normal_transfer():

    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    to_addr = Address('htdf1jrh6kxrcr0fd8gfgdwna8yyr9tkt99ggmz9ja2')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfTxBuilder(
        from_address=from_addr,
        to_address=to_addr,
        amount_satoshi=htdf_to_satoshi(20.1215),
        sequence=from_acc.sequence,
        account_number=from_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=30000,
        data='',
        memo='htdfsdk test'
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))

    mempool =  htdfrpc.get_mempool_trasactions()
    pprint(mempool)

    memtx = htdfrpc.get_mempool_transaction(transaction_hash=tx_hash)
    pprint(memtx)

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    pprint(tx)


# @pytest.fixture(params=[])
def test_get_upgrade_info():
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)
    tx = htdfrpc.get_upgrade_info()
    pprint(tx)


def test_contract_call():
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)
    data = '8da5cb5b'
    contract_address = 'htdf1qnvztdxxr0l70sqqa33zah4e4sq4wk4nhwalsz'
    rsp = htdfrpc.contract_call(contract_address=contract_address, hex_data=data)
    print(rsp)

    pass




# get validators
# hscli query staking validators
#
# convert validator address to bech32
# hscli bech32 v2b htdfvaloper1gu23408yyv6lk6vqjkykecmulnj0xsmhqr47hs
#
#
# export validator private key
# hscli accounts export htdf1gu23408yyv6lk6vqjkykecmulnj0xsmh26d8qm 12345678

def test_delegate_tx():
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    to_addr = ValidatorAddress('htdfvaloper1gu23408yyv6lk6vqjkykecmulnj0xsmhqr47hs')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfDelegateTxBuilder(
        delegator_address=from_addr,
        validator_address= to_addr,
        amount_satoshi=htdf_to_satoshi(2000),
        sequence=from_acc.sequence,
        account_number=from_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=30000,
        memo=''
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))

    mempool = htdfrpc.get_mempool_trasactions()
    pprint(mempool)

    memtx = htdfrpc.get_mempool_transaction(transaction_hash=tx_hash)
    pprint(memtx)

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    pprint(tx)



def test_withdraw_delegate_rewards_tx():
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    to_addr = ValidatorAddress('htdfvaloper1gu23408yyv6lk6vqjkykecmulnj0xsmhqr47hs')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfWithdrawDelegateRewardsTxBuilder(
        delegator_address=from_addr,
        validator_address= to_addr,
        # amount_satoshi=htdf_to_satoshi(2000),
        sequence=from_acc.sequence,
        account_number=from_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=30000,
        memo=''
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))

    mempool = htdfrpc.get_mempool_trasactions()
    pprint(mempool)

    memtx = htdfrpc.get_mempool_transaction(transaction_hash=tx_hash)
    pprint(memtx)

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    pprint(tx)


def test_set_undelegate_status_tx():
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)

    delegate_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    to_addr = ValidatorAddress('htdfvaloper1gu23408yyv6lk6vqjkykecmulnj0xsmhqr47hs')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')

    validator_privkey = HtdfPrivateKey('e9f1679dd20996cc7d157cd632318a4b469f526accccca920552fa7cf084f65c')
    validator_acc = htdfrpc.get_account_info(address=validator_privkey.address.address)

    delegate_acc = htdfrpc.get_account_info(address=delegate_addr.address)
    signed_tx = HtdfSetUndelegateStatusTxBuilder(
        delegator_address=delegate_addr,
        validator_address= to_addr,
        status=True,
        sequence=validator_acc.sequence,
        account_number=validator_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=30000,
        memo=''
    ).build_and_sign(private_key=validator_privkey)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))

    mempool = htdfrpc.get_mempool_trasactions()
    pprint(mempool)

    memtx = htdfrpc.get_mempool_transaction(transaction_hash=tx_hash)
    pprint(memtx)

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    pprint(tx)




def test_undelegate_tx():
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)

    from_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    to_addr = ValidatorAddress('htdfvaloper1gu23408yyv6lk6vqjkykecmulnj0xsmhqr47hs')
    private_key = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
    from_acc = htdfrpc.get_account_info(address=from_addr.address)
    signed_tx = HtdfUndelegateTxBuilder(
        delegator_address=from_addr,
        validator_address= to_addr,
        amount_satoshi=htdf_to_satoshi(2000),
        sequence=from_acc.sequence,
        account_number=from_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=30000,
        memo=''
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))

    mempool = htdfrpc.get_mempool_trasactions()
    pprint(mempool)

    memtx = htdfrpc.get_mempool_transaction(transaction_hash=tx_hash)
    pprint(memtx)

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    pprint(tx)





def test_edit_validator_info_tx():

    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)

    # delegate_addr = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')
    val_addr = ValidatorAddress('htdfvaloper1gu23408yyv6lk6vqjkykecmulnj0xsmhqr47hs')

    validator_privkey = HtdfPrivateKey('e9f1679dd20996cc7d157cd632318a4b469f526accccca920552fa7cf084f65c')
    validator_acc = htdfrpc.get_account_info(address=validator_privkey.address.address)

    signed_tx = HtdfEditValidatorInfoTxBuilder(
        validator_address= val_addr,
        sequence=validator_acc.sequence,
        account_number=validator_acc.account_number,
        chain_id=htdfrpc.chain_id,
        gas_price=100,
        gas_wanted=30000,
        memo='',
        details="This is yqq test node",
        identity='yqq000001',
        moniker='yqq',
        website='www.yqq.good',
        min_self_delegation='2',
        commission_rate='0.101',
    ).build_and_sign(private_key=validator_privkey)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))

    mempool = htdfrpc.get_mempool_trasactions()
    pprint(mempool)

    memtx = htdfrpc.get_mempool_transaction(transaction_hash=tx_hash)
    pprint(memtx)

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    pprint(tx)



def main():
    # test_contract_call()
    # test_delegate_tx()
    # test_withdraw_delegate_rewards_tx()
    # test_set_undelegate_status_tx()
    # test_undelegate_tx()

    test_edit_validator_info_tx()

    pass


if __name__ == '__main__':
    main()
    pass


