# HTDF sdk

the sdk of HTDF

require python >= 3.6

# Install

```
pip install htdfsdk
```


# Example

```python

from htdfsdk import HtdfRPC, HtdfTxBuilder, htdf_to_satoshi, Address

htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='192.168.0.171', rpc_port=1317)
from_addr = 'htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml'
private_key = '279bdcd8dccec91f9e079894da33d6888c0f9ef466c0b200921a1bf1ea7d86e8'
from_acc = htdfrpc.get_account_info(address=from_addr)
signed_tx = HtdfTxBuilder(
    from_address=from_addr,
    to_address='htdf1jrh6kxrcr0fd8gfgdwna8yyr9tkt99ggmz9ja2',
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

            
```
