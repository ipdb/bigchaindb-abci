# NOTE: May be use abstract class for clear interface
from abci import CodeTypeOk


class BaseApplication(object):
    """
    Base ABCI Application. Extend this and override what's needed for your app
    """
    def __init__(self, abci_types):
        # types: (Module) -> None
        self.abci = abci_types

    def init_chain(self, req):
        # types: (RequestInitChain) -> ResponseInitChain
        """
        Called only once - usually at genesis or when blockheight == 0.
        See info()
        """
        return self.abci.ResponseInitChain()

    def info(self, req):
        # types (RequestInfo) -> ResponseInfo
        """
        Called by ABCI when the app first starts. A stateful application
        should alway return the last blockhash and blockheight to prevent Tendermint
        from replaying the transaction log from the beginning.  This values are used
        to help Tendermint determine how to synch the node.
        If blockheight == 0, Tendermint will call init_chain()
        """
        r = self.abci.ResponseInfo()
        r.last_block_height = 0
        r.last_block_app_hash = b''
        return r

    def set_option(self, req):
        # types: (RequestSetOption) -> ResponseSetOption
        """Can be used to set key value pairs in storage.  Not always used"""
        return self.abci.ResponseSetOption()

    def deliver_tx(self, tx):
        # types: (bytes) -> ResponseDeliverTx
        """
        Process the tx and apply state changes.
        This is called via the consensus connection.
        A non-zero response code implies an error and will reject the tx
        """
        return self.abci.ResponseDeliverTx(code=CodeTypeOk)

    def check_tx(self, tx):
        # types: (bytes) -> ResponseCheckTx
        """
        Use to validate incoming transactions.  If the returned resp.code is 0 (OK),
        the tx will be added to Tendermint's mempool for consideration in a block.
        A non-zero response code implies an error and will reject the tx
        """
        return self.abci.ResponseCheckTx(code=CodeTypeOk)

    def query(self, req):
        # types: (RequestQuery) -> ResponseQuery
        """
        This is commonly used to query the state of the application.
        A non-zero 'code' in the response is used to indicate and error.
        """
        return self.abci.ResponseQuery(code=CodeTypeOk)

    def begin_block(self, req):
        # types: (RequestBeginBlock) -> ResponseBeginBlock
        """
        Called during the consensus process.  The overall flow is:
        begin_block()
         for each tx:
           deliver_tx(tx)
        end_block()
        commit()
        """
        return self.abci.ResponseBeginBlock()

    def end_block(self, req):
        # types: (ResponseEndBlock) -> ResponseEndBlock
        """Called at the end of processing. If this is a stateful application
        you can use the height from here to record the last_block_height"""
        return self.abci.ResponseEndBlock()

    def commit(self):
        # types: () -> ResponseCommit
        """
        Called after the end of a block.  Normally this should return the results
        of the computation, such as the root hash of a merkletree.  The returned
        data is used as part of the consensus process.
        """
        return self.abci.ResponseCommit()
