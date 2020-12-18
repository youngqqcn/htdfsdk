import sys

if sys.version_info < (3, 6):
    raise EnvironmentError(
        "Python 3.6 or above is required. ")


# import web3

from htdfsdk.htdfsdk import (
    HtdfTxBuilder,
    HtdfRPC,
    Address,
    HtdfPrivateKey,
)

from htdfsdk.contract import (
    HtdfContract
)

from eth_utils import (
    to_checksum_address,
    remove_0x_prefix
)


from htdfsdk.utils import *

__all__ = [
    'utils',
    "HtdfRPC",
    "HtdfTxBuilder",
    "Address",
    "HtdfPrivateKey",
    # "web3"
    "HtdfContract",
    "to_checksum_address",
    "remove_0x_prefix",
]
