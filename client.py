from bitfield import Bitfield
from handshake import Handshake
from message import Message, MessageCodes
import socket

# A client handles the state between us and a peer
class Client(object):
    def __init__(self, peer, info_hash, peer_id):
        self.__perform_handshake__(peer, info_hash, peer_id)
        self.bitfield = self.__receive_bitfield__(peer)
        self.peer_id = peer_id
        self.info_hash = info_hash
        self.peer = peer
        self.choked = True

    def send_unchoke(self):
        message = Message(MessageCodes.UNCHOKE, None)
        self.choked = False
        self.peer.send(message.serialize())

    def send_interested(self):
        message = Message(MessageCodes.INTERESTED, None)
        self.peer.send(message.serialize())


    def __perform_handshake__(self, peer, info_hash, peer_id):
        peer.connect()
        if peer.alive:
            handshake = Handshake(info_hash, peer_id)
            peer.send(handshake.serialize())
            handshake_resp = handshake.deserialize(peer.receive(Handshake.MSG_LEN))
            if handshake_resp.info_hash != handshake.info_hash:
                raise ConnectionError("info_hash mismatch")
        else:
            raise ConnectionAbortedError("No answer from this client...")

    def __receive_bitfield__(self, peer):
        data = peer.receive()
        msg = Message.deserialize(data)
        if msg.id != MessageCodes.BITFIELD:
            raise ConnectionError("expected BITFIELD, got {}".format(MessageCodes(msg.id).name))
        return Bitfield(msg.message)


