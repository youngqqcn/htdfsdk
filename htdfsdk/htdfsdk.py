# coding:utf8
# author: yqq
# date: 2020/12/15 16:45
# descriptions:


from typing import Dict, List

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
import os

from .utils import htdf_to_satoshi
from .template import UNSIGNED_TX_TEMPLATE, BROADCAST_TX_TEMPLATE


class Account:
    address: str
    balance_satoshi: int
    account_number: int
    sequence: int


class Address:

    def __init__(self, address: [str, bytes]):
        self.__address = address
        if not Address.is_valid_address(self.__address):
            raise Exception("invalid address: {}".format(self.__address))
        self.__hex_address = Address.bech32_to_hexaddr(self.__address)
        pass

    @classmethod
    def bech32_to_hexaddr(cls, bech32_address: str) -> str:
        assert len(bech32_address) > 0

        hrp, data = bech32_decode(bech32_address)
        hexbytes = convertbits(data, 5, 8, pad=False)
        hexstraddr = ''.join(['%02x' % x for x in hexbytes])
        return hexstraddr.upper()

    @classmethod
    def hexaddr_to_bech32(cls, hex_address: str, hrp: str = 'htdf') -> str:
        assert len(hex_address) > 0 and (len(hex_address) & 1 == 0)
        hexaddr = hex_address[2:] if hex_address[:2] == '0x' else hex_address

        data = [int(x) for x in unhexlify(hexaddr)]
        addr = bech32_encode(hrp, convertbits(data, 8, 5))
        return addr

    @classmethod
    def is_valid_address(cls, address: str) -> bool:
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
    def address(self) -> str:
        """bech32 encoding address """
        return self.__address

    def bech32_address(self) -> str:
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

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.address == other.address


class HtdfPrivateKey:

    def __init__(self, private_key_hex: [str, bytes]):

        if len(private_key_hex) == 0:
            private_key_hex = self.create_random_private_key()
        else:
            assert len(unhexlify(private_key_hex)) == 32, 'invalid parameter: private_key_hex'

        self.__private_key_hex = private_key_hex
        sk = ecdsa.SigningKey.from_string(unhexlify(self.__private_key_hex), curve=ecdsa.SECP256k1)
        s = sk.get_verifying_key().to_string(encoding='compressed')
        self.__public_key_compressed = hexlify(s).decode('latin1')

        uck = sk.get_verifying_key().to_string(encoding='uncompressed')
        self.__public_key_uncompressed = hexlify(uck).decode('latin1')
        pass

    @classmethod
    def create_random_private_key(cls, salt: str = '') -> str:
        # reference : https://en.bitcoin.it/wiki/Private_key
        MAX_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140
        while True:
            randkey = hexlify(os.urandom(32))
            hash = hexlify(hashlib.sha256(randkey + salt.encode('utf8')).digest())
            if (1 << 32) < int(hash, 16) < MAX_P:
                return hash.decode('latin1')
        pass

    @property
    def private_key(self) -> str:
        return self.__private_key_hex

    @property
    def private_key_bytes(self) -> bytes:
        return unhexlify(self.__private_key_hex)

    def public_key(self, compressed: bool = True) -> str:
        return self.__public_key_compressed if compressed else self.__public_key_uncompressed

    @classmethod
    def pubkey_to_address(cls, public_key_compressed, hrp='htdf'):
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(unhexlify(public_key_compressed)).digest())
        r160data = ripemd160.digest()
        data = [r160data[i] for i in range(len(r160data))]
        address = bech32_encode(hrp, convertbits(data, 8, 5))
        return address

    @property
    def address(self) -> Address:
        return Address(self.bech32_address)

    @property
    def bech32_address(self) -> str:
        return self.pubkey_to_address(self.__public_key_compressed)

    @property
    def hex_address(self) -> str:
        return Address.bech32_to_hexaddr(self.bech32_address)

    def sign(self, hash: bytes) -> Tuple:
        pk = coincurve.PrivateKey(self.private_key_bytes)
        signature = pk.sign_recoverable(hash, hasher=None)
        # v = safe_ord(signature[64]) + 27
        r = signature[0:32]
        s = signature[32:64]
        return r, s

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.private_key == other.private_key

    def __str__(self):
        return self.__private_key_hex


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
            acc.balance_satoshi = htdf_to_satoshi(float(rsp['value']['coins'][0]['amount']))
        else:
            acc.balance_satoshi = 0
        return acc

    def get_balance(self, address: str) -> int:
        """ get account balance in satoshi"""
        acc = self.get_account_info(address=address)
        if acc:
            return acc.balance_satoshi
        return 0

    def get_block(self, block_number: int) -> [Dict, None]:
        """ get block details by block number"""

        url = 'http://{0}/block_detail/{1}'.format(self.node_ip_port.strip(), block_number)
        rsp = requests.get(url)
        if rsp.status_code != 200:
            return None
        tx = rsp.json()
        return tx

    def get_latest_block(self) -> [Dict, None]:
        """ get latest block details """

        url = 'http://{0}/blocks/latest'.format(self.node_ip_port.strip())
        rsp = requests.get(url)
        if rsp.status_code != 200:
            return None
        tx = rsp.json()
        return tx

    def get_mempool_transaction(self, transaction_hash: str) -> [Dict, None]:
        """
        search a tx in mempool by tx_hash, if it not in mempool return None .
        NOTE: a confirmed(successed or failed) transaction couldn't be found in mempool
        """
        req_url = 'http://{0}/mempool/txs/{1}'.format(self.node_ip_port.strip(), transaction_hash.strip())
        rsp = requests.get(url=req_url)
        if rsp.status_code == 400:
            return None
        tx = rsp.json()
        return tx

    def get_mempool_trasactions(self) -> [List[Dict], None]:
        """ get the frontly 101 transactions """
        # raise NotImplementedError
        req_url = 'http://{0}/mempool/txs'.format(self.node_ip_port.strip())
        rsp = requests.get(url=req_url)
        if rsp.status_code != 200:
            return None
        tx = rsp.json()
        return tx

    def get_mempool_transaction_count(self) -> [Dict, None]:
        """ get mempool transaction count """
        # raise NotImplementedError
        req_url = 'http://{0}/mempool/txscount'.format(self.node_ip_port.strip())
        rsp = requests.get(url=req_url)
        if rsp.status_code != 200:
            return None
        tx = rsp.json()
        return tx

    # @func_set_timeout(30)
    def get_tranaction_until_timeout(self, transaction_hash: str, timeout_secs: float = 15,
                                     interval_secs: float = 5) -> [Dict, None]:
        assert 0.0 < interval_secs < timeout_secs, 'interval_secs must less than timeout secs'
        start_time = time.time()
        while True:
            url = 'http://{0}/txs/{1}'.format(self.node_ip_port, transaction_hash.strip())
            rsp = requests.get(url)
            if rsp.status_code == 404:
                cur_time = time.time()
                if cur_time - start_time >= timeout_secs:
                    return None
                if timeout_secs - (cur_time - start_time) >= interval_secs:
                    time.sleep(interval_secs)
                else:
                    time.sleep(timeout_secs - (cur_time - start_time))
                continue
            tx = rsp.json()
            return tx
        pass

    def get_transaction(self, transaction_hash: str) -> [Dict, None]:
        """
        get transaction by hash
        :param transaction_hash:  tx hash
        :return: if found , return transaction details , else return None
        """

        url = 'http://{0}/txs/{1}'.format(self.node_ip_port.strip(), transaction_hash.strip())
        rsp = requests.get(url)
        if rsp.status_code == 404:
            return None
        tx = rsp.json()
        return tx

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

    def get_upgrade_info(self) -> Dict:
        """
        get upgrade info
        :return:
        """
        url = 'http://{0}/upgrade_info'.format(self.node_ip_port.strip())
        rsp = requests.get(url)
        if rsp.status_code != 200:
            raise Exception("get upgrade info error:{}".format(rsp.text))
        tx = rsp.json()
        return tx

    def __str__(self):
        pass


class HtdfTxBuilder(object):

    def __init__(self, from_address: Address, to_address: Address, amount_satoshi: int,
                 sequence: int, account_number: int, chain_id: str,
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

    def build_and_sign(self, private_key: HtdfPrivateKey) -> str:
        """
        build and sign transaction
        :param private_key:
        :return: signed transaction
        """

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

        r, s = private_key.sign(shadata)
        # logging.info('r:' + hexlify(r).decode(encoding='utf8'))
        # logging.info('s:' + hexlify(s).decode(encoding='utf8'))

        b64sig = base64.b64encode(r + s).decode(encoding='utf8')
        # logging.info("base64encode(signature) : {}".format(b64sig))

        # step 5 : format broadcast string
        pubkey = private_key.public_key()  # self.__privkey_to_pubkey(privkey=private_key)
        b64pubkey = base64.b64encode(unhexlify(pubkey)).decode(encoding='utf8')
        # logging.info("base64encode(public key) :" + b64pubkey)

        fmt_broadcast_str = BROADCAST_TX_TEMPLATE.replace(' ', '').replace('\n', '').replace('\t', '')
        fmt_broadcast_str = fmt_broadcast_str % (
            self.from_address, self.to_address, self.amount_satoshi,
            self.data, self.gas_price, self.gas_wanted, self.gas_wanted, self.gas_price, b64pubkey, b64sig, self.memo)
        # logging.info("broadcast str: {}".format(fmt_broadcast_str))

        broadcast_data = hexlify(bytes(fmt_broadcast_str, encoding='utf8')).decode(encoding='utf8')
        return broadcast_data

    def __str__(self):
        pass
