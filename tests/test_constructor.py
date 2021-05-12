#coding:utf8
#author: yqq
#date: 2021/5/12 下午4:57
#descriptions:
import json
from pprint import pprint


from htdfsdk import Address, HtdfRPC, HtdfPrivateKey, HtdfTxBuilder, htdf_to_satoshi
from htdfsdk import HtdfContract


def parse_truffe_compile_outputs(json_path: str):
    with open(json_path, 'r') as infile:
        compile_outputs = json.loads(infile.read())
        abi = compile_outputs['abi']
        bytecode = compile_outputs['bytecode']
        bytecode = bytecode.replace('0x', '')
        return abi, bytecode

def test_deploy_contract():
    abi, bytecodes = parse_truffe_compile_outputs('./Constructor.json')
    htdfrpc = HtdfRPC(chaid_id='testchain', rpc_host='127.0.0.1', rpc_port=1317)
    htdfcontract = HtdfContract(rpc=htdfrpc, address=None, abi=abi, bytecode=bytecodes)
    data = htdfcontract.constructor_data(amount=8899)
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
        gas_wanted=200000,
        data=data,
        memo='test_deploy_contract'
    ).build_and_sign(private_key=private_key)

    tx_hash = htdfrpc.broadcast_tx(tx_hex=signed_tx)
    print('tx_hash: {}'.format(tx_hash))
    # self.assertTrue( len(tx_hash) == 64)

    tx = htdfrpc.get_transaction_until_timeout(transaction_hash=tx_hash)
    pprint(tx)

    pass




def main():
    test_deploy_contract()
    pass


if __name__ == '__main__':
    main()
    pass
