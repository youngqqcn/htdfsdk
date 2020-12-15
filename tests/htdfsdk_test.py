import unittest

from htdfsdk import HtdfRPC, HtdfTxBuilder, htdf_to_satoshi, Address


class MyTestCase(unittest.TestCase):

    def test_htdf_address(self):
        bech32_address = 'htdf1xwpsq6yqx0zy6grygy7s395e2646wggufqndml'
        addr1 = Address(address=bech32_address)
        hexaddr =  addr1.hex_address
        hex_address = Address.bech32_to_hexaddr(bech32_address=bech32_address)
        self.assertEqual(hex_address, '338300688033C44D2064413D08969956ABA7211C')
        self.assertEqual(hexaddr, '338300688033C44D2064413D08969956ABA7211C')

        bech32_address2 = addr1.hexaddr_to_bech32(hex_address='338300688033C44D2064413D08969956ABA7211C')
        self.assertEqual(bech32_address, bech32_address2)



    def test_htdf_normal_transfer(self):

        def transfer():
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
            return tx_hash

        # self.assertRaises(None, transfer, )
        tx_hash = transfer()
        self.assertTrue( len(tx_hash) == 64)


if __name__ == '__main__':
    unittest.main()
