# coding:utf8
# author: yqq
# date: 2020/12/18 10:44
# descriptions:  contract wrapper for htdf contract transactions
import itertools
import json
from typing import Optional, Any

from eth_abi.exceptions import DecodingError
from eth_typing import HexStr
from eth_utils import to_checksum_address, remove_0x_prefix, decode_hex

from htdfsdk import Address, HtdfRPC
from htdfsdk.web3 import Web3
from htdfsdk.web3._utils.abi import get_abi_output_types, map_abi_data
from htdfsdk.web3._utils.contracts import prepare_transaction, find_matching_fn_abi
from htdfsdk.web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from htdfsdk.web3.contract import Contract, ContractFunction, ACCEPTABLE_EMPTY_STRINGS
from htdfsdk.web3.exceptions import BadFunctionCallOutput
from htdfsdk.web3.types import TxParams


class HtdfContract:

    def __init__(self, rpc: HtdfRPC, address: [Address, None], **kwargs: Any):
        assert address is None or isinstance(address, Address)
        self.rpc = rpc
        self.web3 = Web3()
        self.contract_factory = Contract.factory(web3=self.web3, **kwargs)
        if address is not None :
            self.address = address
            self.chksum_addr = to_checksum_address(value=address.hex_address)
            self.contract = self.contract_factory(self.chksum_addr)
            self.functions = self.contract.functions
        pass

    def constructor_data(self, *args: Any, **kwargs: Any) -> HexStr:
        data = self.contract_factory.constructor(*args, **kwargs).data_in_transaction
        return remove_0x_prefix( data )


    def call(self, cfn: ContractFunction) -> Any:
        """
        refactor ContractFunction.call() to this function
        :param cfn:
        :return:
        """
        call_transaction: TxParams = {}
        if 'data' in call_transaction:
            raise ValueError("Cannot set data in call transaction")

        if self.chksum_addr:
            call_transaction.setdefault('to', self.chksum_addr)
        # if self.web3.eth.defaultAccount is not empty:
        # type ignored b/c check prevents an empty defaultAccount
        # call_transaction.setdefault('from', self.web3.eth.defaultAccount)  # type: ignore

        pre_tx = prepare_transaction(
            self.chksum_addr,
            self.web3,
            fn_identifier=cfn.function_identifier,
            contract_abi=cfn.contract_abi,
            fn_abi=cfn.abi,
            transaction=call_transaction,
            fn_args=cfn.args,
            fn_kwargs=cfn.kwargs,
        )

        data = remove_0x_prefix(pre_tx['data'])

        ret_data = self.rpc.contract_call(contract_address=self.address.bech32_address(), hex_data=data)
        # print('ret_data is {}'.format(ret_data))

        ret_data_bytes = decode_hex(ret_data)

        if cfn.abi is None:
            fn_abi = find_matching_fn_abi(cfn.contract_abi, self.web3.codec, cfn.function_identifier, args, kwargs)

        output_types = get_abi_output_types(cfn.abi)

        try:
            output_data = self.web3.codec.decode_abi(output_types, ret_data_bytes)
        except DecodingError as e:
            # Provide a more helpful error message than the one provided by
            # eth-abi-utils
            is_missing_code_error = (
                    ret_data_bytes in ACCEPTABLE_EMPTY_STRINGS)
            # and self.web3.eth.getCode(address) in ACCEPTABLE_EMPTY_STRINGS)
            if is_missing_code_error:
                msg = (
                    "Could not transact with/call contract function, is contract "
                    "deployed correctly and chain synced?"
                )
            else:
                msg = (
                    "Could not decode contract function call {} return data {} for "
                    "output_types {}".format(
                        cfn.function_identifier,
                        ret_data_bytes,
                        output_types
                    )
                )
            raise BadFunctionCallOutput(msg) from e

        normalizers = tuple()
        _normalizers = itertools.chain(
            BASE_RETURN_NORMALIZERS,
            normalizers,
        )
        normalized_data = map_abi_data(_normalizers, output_types, output_data)

        if len(normalized_data) == 1:
            return normalized_data[0]
        else:
            return normalized_data

        # return call_transaction

    def __str__(self):
        pass
