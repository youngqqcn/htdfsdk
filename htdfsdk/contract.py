# coding:utf8
# author: yqq
# date: 2020/12/18 10:44
# descriptions:  contract wrapper for htdf contract transactions
import json
from typing import Optional, Any

from eth_utils import to_checksum_address

from htdfsdk import Address
from web3 import Web3
from web3.contract import Contract


class HtdfContract:

    def __init__(self, address: Address, **kwargs: Any):
        self.web3 = Web3()
        chksum_addr = to_checksum_address(value=address.hex_address)
        contract_factory = Contract.factory(web3=self.web3, **kwargs )
        # self.web3_contract = Contract(address=chksum_addr)
        self.contract = contract_factory(chksum_addr)
        pass


    def __str__(self):
        pass


