# HTDF sdk

the sdk of HTDF

require python3.6+

# Install

```
pip3 install htdfsdk --upgrade
```


# Example

## Create address

```python
from htdfsdk import Address, HtdfPrivateKey
privkey = HtdfPrivateKey('')
print(privkey.private_key)
print(privkey.address)
# privkey2 = HtdfPrivateKey(privkey.private_key)
# pk3 = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
# addr3 = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')

```




## Normal HTDF Transaction

```python

from pprint import pprint
from htdfsdk import HtdfRPC, HtdfTxBuilder, htdf_to_satoshi, Address, HtdfPrivateKey

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

    # mempool =  htdfrpc.get_mempool_trasactions()
    # pprint(mempool)

    # memtx = htdfrpc.get_mempool_transaction(transaction_hash=tx_hash)
    # pprint(memtx)

    tx = htdfrpc.get_tranaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    # tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
    # pprint(tx)
            
```


## Contract Transaction


```python

import json
from pprint import pprint
from htdfsdk import Address, HtdfRPC, HtdfPrivateKey, HtdfTxBuilder, htdf_to_satoshi
from htdfsdk import HtdfContract
from htdfsdk import to_checksum_address, remove_0x_prefix

def test_hrc20_name():

    with open('./AJC_sol_AJCToken.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    contract_address = Address('htdf1k78exwfuta66m3sxgfjd6zuw8m7zykfmas0nrf')
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)

    name  =hc.call( hc.functions.name() )
    print(name)
    assert name == "AJC chain"
    pass


def test_hrc20_totalSupply():
    with open('./AJC_sol_AJCToken.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    contract_address = Address('htdf1k78exwfuta66m3sxgfjd6zuw8m7zykfmas0nrf')
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

    contract_address = Address('htdf1k78exwfuta66m3sxgfjd6zuw8m7zykfmas0nrf')
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)

    hc = HtdfContract(rpc=htdfrpc, address=contract_address, abi=abi)

    totalSupply = hc.call(hc.functions.decimals())
    print(totalSupply)
    assert totalSupply == int(18)
    pass


def test_hrc20_transfer():
    with open('./AJC_sol_AJCToken.abi', 'r') as abifile:
        # abi = abifile.readlines()
        abijson = abifile.read()
        # print(abijson)
        abi = json.loads(abijson)

    contract_address = Address('htdf1k78exwfuta66m3sxgfjd6zuw8m7zykfmas0nrf')
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

```


## TODO

- non-htdfservice transaction(eg. delegate undelegate )
- continuously optimize
- contract event support(HTDF v1.4.0)
- websocket support(HTDF v1.4.0)




## More details 

[https://github.com/youngqqcn/htdfsdk](https://github.com/youngqqcn/htdfsdk)
