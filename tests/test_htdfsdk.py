import pytest
import time
from pprint import pprint

from htdfsdk import HtdfRPC, HtdfTxBuilder, htdf_to_satoshi, Address, HtdfPrivateKey


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
    # self.assertTrue( len(tx_hash) == 64)

    mempool =  htdfrpc.get_mempool_trasactions()
    pprint(mempool)

    memtx = htdfrpc.get_mempool_transaction(transaction_hash=tx_hash)
    pprint(memtx)

    tx = htdfrpc.get_tranaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    pprint(tx)

