from typing import (
    NoReturn,
)

from htdfsdk.web3._utils.net import (
    listening,
    peer_count,
    peerCount,
    version,
)
from htdfsdk.web3.module import (
    ModuleV2,
)


class Net(ModuleV2):
    """
        https://github.com/ethereum/wiki/wiki/JSON-RPC
    """

    _listening = listening
    _peer_count = peer_count
    _peerCount = peerCount
    _version = version

    @property
    def listening(self) -> bool:
        return self._listening()

    @property
    def peer_count(self) -> int:
        return self._peer_count()

    @property
    def peerCount(self) -> int:
        return self._peerCount()

    @property
    def chainId(self) -> NoReturn:
        raise DeprecationWarning("This method has been deprecated in EIP 1474.")

    @property
    def version(self) -> str:
        return self._version()
