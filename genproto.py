"""
NOTE: This code is adapted from the google protobuf Python library. Specifically
from the setup.py file
"""

import os
import subprocess
import sys
from distutils.spawn import find_executable


if 'PROTOC' in os.environ and os.path.exists(os.environ['PROTOC']):
    protoc = os.environ['PROTOC']
elif os.path.exists("../src/protoc"):
    protoc = "../src/protoc"
elif os.path.exists("../src/protoc.exe"):
    protoc = "../src/protoc.exe"
elif os.path.exists("../vsprojects/Debug/protoc.exe"):
    protoc = "../vsprojects/Debug/protoc.exe"
elif os.path.exists("../vsprojects/Release/protoc.exe"):
    protoc = "../vsprojects/Release/protoc.exe"
else:
    protoc = find_executable("protoc")


# def generate_proto(source, version, require=True):
def generate_proto(source, require=True):
    """Invokes the Protocol Compiler to generate a _pb2.py from the given
    .proto file.  Does nothing if the output already exists and is newer than
    the input."""

    if not require and not os.path.exists(source):
        return

    output = source.replace(".proto", "_pb2.py").replace("./protobuf/", "")

    if (not os.path.exists(output)
        or (os.path.exists(source)
            and os.path.getmtime(source) > os.path.getmtime(output))):
        print("Generating %s..." % output)

        if not os.path.exists(source):
            sys.stderr.write("Can't find required file: %s\n" % source)
            sys.exit(-1)

        if protoc is None:
            sys.stderr.write(
                "protoc is not installed\n")
            sys.exit(-1)

        protoc_command = [protoc, "-I./protobuf/", "--python_out=.", source]
        if subprocess.call(protoc_command) != 0:
            sys.exit(-1)


COMMON = [
    "github.com/gogo/protobuf/gogoproto/gogo.proto"
]

GEN_MAP = {
    # Version to file list mapping
    'v0_22_8': [
        'github.com/tendermint/tmlibs/common/types.proto',
        'types.proto',
    ],
    'v0_31_5': [
        "github.com/tendermint/tendermint/crypto/merkle/merkle.proto",
        "github.com/tendermint/tendermint/libs/common/types.proto",
        "github.com/tendermint/tendermint/abci/types/types.proto",
    ]
}

if __name__ == '__main__':
    # Build all the protobuf files and put into the 'github' directory
    for fn in COMMON:
        generate_proto("./protobuf/abci_pb/{fn}".format(fn=fn))
    for ver, file_names in GEN_MAP.items():
        for fn in file_names:
            generate_proto("./protobuf/abci_pb/{ver}/{fn}".format(ver=ver, fn=fn))
