#coding:utf8
#author: yqq
#date: 2020/12/15 16:45
#descriptions:


from typing import Dict

import json
import hashlib
import time
import ecdsa
import traceback
import coincurve
import base64
import requests
import logging
from typing import Tuple, Dict
from binascii import hexlify, unhexlify
from bech32 import bech32_decode, convertbits, bech32_encode
from func_timeout import func_set_timeout

from .utils import htdf_to_satoshi
from .template import UNSIGNED_TX_TEMPLATE, BROADCAST_TX_TEMPLATE


class Account:
    address : str
    balance_satoshi : int
    account_number : int
    sequence : int


class Address:

    def __init__(self, address: str):
        self.__address = address
        if not Address.is_valid_address(self.__address):
            raise Exception("invalid address: {}".format(self.__address))
        self.__hex_address = Address.bech32_to_hexaddr(self.__address)
        pass

    @classmethod
    def bech32_to_hexaddr(cls, bech32_address: str):
        assert len(bech32_address) > 0

        hrp, data = bech32_decode(bech32_address)
        hexbytes = convertbits(data, 5, 8, pad=False)
        hexstraddr = ''.join(['%02x' % x for x in hexbytes])
        return hexstraddr.upper()

    @classmethod
    def hexaddr_to_bech32(cls, hex_address: str, hrp: str = 'htdf'):
        assert len(hex_address) > 0 and (len(hex_address) & 1 == 0)
        hexaddr = hex_address[2:] if hex_address[:2] == '0x' else hex_address

        data = [int(x) for x in unhexlify(hexaddr)]
        addr = bech32_encode(hrp, convertbits(data, 8, 5))
        return addr


    @classmethod
    def is_valid_address(cls, address: str):
        """ check address validation"""
        if not (len(address) == 43 and address.islower()):
            return False

        prefix, data = bech32_decode(address)
        if prefix is None or data is None:
            return False

        if prefix == 'htdf' and len(data) == 32:
            return True
        return False

    @property
    def address(self):
        """bech32 encoding address """
        return  self.__address

    def bech32_address(self):
        """
        bech32 encoding address
        :return:
        """
        return self.__address

    # def checksum_hex_address(self):
    #     return

    @property
    def hex_address(self) -> str:
        """
        hex encoding address
        :return:
        """
        return self.__hex_address

    def __str__(self):
        """bech32 encoding address"""
        return self.__address



class HtdfRPC(object):

    def __init__(self, chaid_id: str, rpc_host: str, rpc_port: int):
        self.chain_id = chaid_id
        self.rpc_host = rpc_host
        self.rpc_port = rpc_port
        self.node_ip_port = '{}:{}'.format(self.rpc_host, self.rpc_port)
        pass

    def get_account_info(self, address: str) -> [Account, None]:
        """
        get account info
        :param address: address
        :return: account info
        """

        url = 'http://{0}/auth/accounts/{1}'.format(self.node_ip_port.strip(), address.strip())
        rsp = requests.get(url)

        if rsp.status_code != 200:
            if rsp.status_code == 204:
                return None
                # raise Exception('not found any account info ')
            raise Exception('get account info error: {}'.format(rsp.status_code))

        rsp = rsp.json()
        acc = Account()
        acc.address = address
        acc.account_number = int(rsp['value']['account_number'])
        acc.sequence = int(rsp['value']['sequence'])
        if rsp['value']['coins'] is not None:
            acc.balance_satoshi = htdf_to_satoshi( float(rsp['value']['coins'][0]['amount']))
        else:
            acc.balance_satoshi = 0
        return acc


    def get_balance(self, address: str) -> Dict :
        raise NotImplementedError

    def get_latest_block(self, block_num: int) -> Dict:
        raise NotImplementedError

    # @func_set_timeout(30)
    # def get_tranaction_async(self, tx_hash: str) -> Dict:
    #     while True:
    #         url = 'http://{0}/txs/{1}'.format(self.chain_id, tx_hash.strip())
    #         rsp = requests.get(url)
    #         if rsp.status_code == 404:
    #             time.sleep(3)
    #             continue
    #         tx = rsp.json()
    #         return tx
    #     pass

    def get_transaction(self, transaction_hash: str) -> [Dict, None]:
        """
        get transaction by hash
        :param transaction_hash:  tx hash
        :return: transaction details
        """

        url = 'http://{0}/txs/{1}'.format(self.node_ip_port.strip(), transaction_hash.strip())
        rsp = requests.get(url)
        if rsp.status_code == 404 :
            return None
        tx = rsp.json()
        return tx

    def get_block(self, block_num: int) -> Dict:
        raise NotImplementedError

    def broadcast_tx(self, tx_hex: str) -> str:
        """
        broadcast transaction
        :param tx_hex:  transaction is hex-string
        :return:  transaction hash
        """

        # check tx_hex
        unhexlify(tx_hex)

        post_data = {'tx': tx_hex}
        post_data = json.dumps(post_data)
        url = 'http://%s/hs/broadcast' % (self.node_ip_port)
        rsp = requests.post(url, post_data)

        if rsp.status_code != 200:
            raise Exception(rsp.text)

        rsp_json = rsp.json()
        if 'code' in rsp_json or 'raw_log' in rsp_json:
            raise Exception(rsp.text)

        txhash = str(rsp_json['txhash'])

        return txhash


    def __str__(self):
        pass




class HtdfTxBuilder(object):


    def __init__(self, from_address: str, to_address: str, amount_satoshi: int,
                   sequence: int, account_number: int,  chain_id: str,
                 gas_price: int = 100, gas_wanted: int = 30000, data: str = '', memo: str = ''):
        self.from_address = from_address
        self.to_address = to_address
        self.amount_satoshi = amount_satoshi
        self.data = data
        self.memo = memo
        self.sequence = sequence
        self.account_number = account_number
        self.chain_id = chain_id
        self.gas_price = gas_price
        self.gas_wanted = gas_wanted
        pass

    def __sign(self, rawhash, key):
        if coincurve and hasattr(coincurve, 'PrivateKey'):
            pk = coincurve.PrivateKey(key)
            signature = pk.sign_recoverable(rawhash, hasher=None)
            # v = safe_ord(signature[64]) + 27
            r = signature[0:32]
            s = signature[32:64]
            return r, s

    def __privkey_to_pubkey(self, privkey: str) -> str:
        sk = ecdsa.SigningKey.from_string(unhexlify(privkey), curve=ecdsa.SECP256k1)
        s = sk.get_verifying_key().to_string(encoding='compressed')
        return hexlify(s).decode('latin')

    def build_and_sign(self, private_key: str) -> str:
        # logging.info('account_number : {}, sequence: {} '.format(account_number, sequence))

        # step 3 : format raw transaction
        fmt_unsigned_txstr = UNSIGNED_TX_TEMPLATE.replace(' ', '').replace('\t', '').replace('\n', '')
        fmt_unsigned_txstr = fmt_unsigned_txstr % (
            self.account_number, self.chain_id, self.gas_price, self.gas_wanted, self.memo,
            self.amount_satoshi, self.data, self.from_address, self.gas_price, self.gas_wanted,
            self.to_address, self.sequence)

        # logging.info("formatted raw transaction str: {}".format(fmt_unsigned_txstr))

        # step 4 : make signature
        shadata = hashlib.sha256(fmt_unsigned_txstr.encode('utf-8')).digest()
        logging.info("sha256(fmt_unsigned_txstr): {}".format(hexlify(shadata)))

        r, s = self.__sign(shadata, unhexlify(private_key))
        # logging.info('r:' + hexlify(r).decode(encoding='utf8'))
        # logging.info('s:' + hexlify(s).decode(encoding='utf8'))

        b64sig = base64.b64encode(r + s).decode(encoding='utf8')
        # logging.info("base64encode(signature) : {}".format(b64sig))

        # step 5 : format broadcast string
        pubkey = self.__privkey_to_pubkey(privkey=private_key)
        b64pubkey = base64.b64encode(unhexlify(pubkey)).decode(encoding='utf8')
        # logging.info("base64encode(public key) :" + b64pubkey)

        fmt_broadcast_str = BROADCAST_TX_TEMPLATE .replace(' ', '').replace('\n', '').replace('\t', '')
        fmt_broadcast_str = fmt_broadcast_str % (
            self.from_address, self.to_address, self.amount_satoshi,
            self.data, self.gas_price, self.gas_wanted,  self.gas_wanted, self.gas_price, b64pubkey, b64sig, self.memo)
        # logging.info("broadcast str: {}".format(fmt_broadcast_str))

        broadcast_data = hexlify(bytes(fmt_broadcast_str, encoding='utf8')).decode(encoding='utf8')
        return broadcast_data


    def __str__(self):
        pass


