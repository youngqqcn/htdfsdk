import sys
import warnings

import pkg_resources

from eth_account import (
    Account  # noqa: E402,
)
from htdfsdk.web3.main import (
    Web3  # noqa: E402,
)
from htdfsdk.web3.providers.eth_tester import (  # noqa: E402
    EthereumTesterProvider,
)
from htdfsdk.web3.providers.ipc import (  # noqa: E402
    IPCProvider,
)
from htdfsdk.web3.providers.rpc import (  # noqa: E402
    HTTPProvider,
)
from htdfsdk.web3.providers.websocket import (  # noqa: E402
    WebsocketProvider,
)

if (3, 5) <= sys.version_info < (3, 6):
    warnings.warn(
        "Support for Python 3.5 will be removed in web3.py v5",
        category=DeprecationWarning,
        stacklevel=2)

if sys.version_info < (3, 5):
    raise EnvironmentError(
        "Python 3.5 or above is required. "
        "Note that support for Python 3.5 will be removed in web3.py v5")


__version__ =  '0.0.1' #pkg_resources.get_distribution("web3").version

__all__ = [
    "__version__",
    "Web3",
    "HTTPProvider",
    "IPCProvider",
    "WebsocketProvider",
    # "TestRPCProvider",
    "EthereumTesterProvider",
    "Account",
]
