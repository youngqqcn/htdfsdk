# HTDF sdk

the sdk of HTDF

require python >= 3.6

# Install

```
pip install htdfsdk
```


# Example

## create address

```python
from htdfsdk import Address, HtdfPrivateKey
privkey = HtdfPrivateKey('')
print(privkey.private_key)
print(privkey.address)
# privkey2 = HtdfPrivateKey(privkey.private_key)
# pk3 = HtdfPrivateKey('279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8')
# addr3 = Address('htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml')

```




## normal htdf transaction

```python

from pprint import pprint
from htdfsdk import HtdfRPC, HtdfTxBuilder, htdf_to_satoshi, Address, HtdfPrivateKey

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

memtx = htdfrpc.get_mempool_transaction(transaction_hash=tx_hash)

tx = htdfrpc.get_tranaction_until_timeout(transaction_hash=tx_hash)
pprint(tx)

tx = htdfrpc.get_transaction(transaction_hash=tx_hash)
pprint(tx)
            
```
