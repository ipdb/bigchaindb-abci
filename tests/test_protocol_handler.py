from io import BytesIO

from abci.application import BaseApplication, CodeTypeOk
from abci.encoding import read_messages
from abci.server import ProtocolHandler
from abci import types_v0_31_5


class ExampleApp(BaseApplication):

    def __init__(self):
        self.abci = types_v0_31_5
        self.validators = []

    def info(self, req):
        v = req.version
        r = self.abci.ResponseInfo(
            version=v, data="hello",
            last_block_height=0, last_block_app_hash=b'0x12')
        return r

    def init_chain(self, req):
        self.validators = req.validators
        return self.abci.ResponseInitChain()

    def check_tx(self, tx):
        return self.abci.ResponseCheckTx(code=CodeTypeOk, data=tx, log="bueno")

    def deliver_tx(self, tx):
        return self.abci.ResponseDeliverTx(code=CodeTypeOk, data=tx,
                                           log="bueno")

    def query(self, req):
        d = req.data
        return self.abci.ResponseQuery(code=CodeTypeOk, value=d)

    def begin_block(self, req):
        return self.abci.ResponseBeginBlock()

    def end_block(self, req):
        return self.abci.ResponseEndBlock(validator_updates=self.validators)

    def commit(self):
        return self.abci.ResponseCommit(data=b'0x1234')

    def set_option(self, req):
        k = req.key
        v = req.value
        return self.abci.ResponseSetOption(code=CodeTypeOk, log=f'{k}={v}')


def test_handler():
    app = ExampleApp()
    p = ProtocolHandler(app)
    types = app.abci

    def _deserialze(raw: bytes):
        resp = next(read_messages(BytesIO(raw), types.Response))
        return resp

    # Echo
    req = types.Request(echo=types.RequestEcho(message='hello'))
    raw = p.process('echo', req)
    resp = _deserialze(raw)
    assert resp.echo.message == 'hello'

    # Flush
    req = types.Request(flush=types.RequestFlush())
    raw = p.process('flush', req)
    resp = _deserialze(raw)
    assert isinstance(resp.flush, types.ResponseFlush)

    # Info
    req = types.Request(info=types.RequestInfo(version='16'))
    raw = p.process('info', req)
    resp = _deserialze(raw)
    assert resp.info.version == '16'
    assert resp.info.data == 'hello'
    assert resp.info.last_block_height == 0
    assert resp.info.last_block_app_hash == b'0x12'

    # init_chain
    val_a = types.ValidatorUpdate(
        power=10,
        pub_key=types.PubKey(type='amino_encoded', data=b'a_pub_key'))
    val_b = types.ValidatorUpdate(
        power=10, pub_key=types.PubKey(type='amino_encoded', data=b'b_pub_key'))

    v = [val_a, val_b]
    req = types.Request(init_chain=types.RequestInitChain(validators=v))
    raw = p.process('init_chain', req)
    resp = _deserialze(raw)
    assert isinstance(resp.init_chain, types.ResponseInitChain)

    # check_tx
    req = types.Request(check_tx=types.RequestCheckTx(tx=b'helloworld'))
    raw = p.process('check_tx', req)
    resp = _deserialze(raw)
    assert resp.check_tx.code == CodeTypeOk
    assert resp.check_tx.data == b'helloworld'
    assert resp.check_tx.log == 'bueno'

    # deliver_tx
    req = types.Request(deliver_tx=types.RequestDeliverTx(tx=b'helloworld'))
    raw = p.process('deliver_tx', req)
    resp = _deserialze(raw)
    assert resp.deliver_tx.code == CodeTypeOk
    assert resp.deliver_tx.data == b'helloworld'
    assert resp.deliver_tx.log == 'bueno'

    # query
    req = types.Request(query=types.RequestQuery(path='/dave', data=b'0x12'))
    raw = p.process('query', req)
    resp = _deserialze(raw)
    assert resp.query.code == CodeTypeOk
    assert resp.query.value == b'0x12'

    # begin_block
    req = types.Request(begin_block=types.RequestBeginBlock(hash=b'0x12'))
    raw = p.process('begin_block', req)
    resp = _deserialze(raw)
    assert isinstance(resp.begin_block, types.ResponseBeginBlock)

    # end_block
    req = types.Request(end_block=types.RequestEndBlock(height=10))
    raw = p.process('end_block', req)
    resp = _deserialze(raw)
    assert resp.end_block.validator_updates
    assert len(resp.end_block.validator_updates) == 2
    assert resp.end_block.validator_updates[0].pub_key.data == b'a_pub_key'
    assert resp.end_block.validator_updates[1].pub_key.data == b'b_pub_key'

    # Commit
    req = types.Request(commit=types.RequestCommit())
    raw = p.process('commit', req)
    resp = _deserialze(raw)
    assert resp.commit.data == b'0x1234'

    # No match
    raw = p.process('whatever', None)
    resp = _deserialze(raw)
    assert resp.exception.error == "ABCI request not found"

    # set_option
    req = types.Request(set_option=types.RequestSetOption(key='name',
                                                          value='dave'))
    raw = p.process('set_option', req)
    resp = _deserialze(raw)
    assert resp.set_option.code == CodeTypeOk
    assert resp.set_option.log == 'name=dave'
