import enum

from abci_pb.v0_22_8 import types_pb2 as types_v0_22_8
from abci_pb.v0_31_5.github.com.tendermint.tendermint.abci.types import \
    types_pb2 as types_v0_31_5

CodeTypeOk = 0


class TmVersion(enum.Enum):
    """Supported Tendermint versions enum"""
    v0_31_5 = 'v0.31.5'
    v0_22_8 = 'v0.22.8'


class ABCI(object):
    def __init__(self, tm_version=None):
        # types: (TmVersion) -> None
        self.types = {
            TmVersion.v0_22_8: types_v0_22_8,
            TmVersion.v0_31_5: types_v0_31_5,
        }.get(tm_version)

        if self.types is None:
            raise Exception(
                "Unsupported tendermint version, "
                "Please specify tendermint version"
                "Hint: import TmVersion")
