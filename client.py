from bitfield import Bitfield
from handshake import Handshake
from message import Message
import socket

# A client handles the state between us and a peer
class Client(object):
    def __init__(self, peer, info_hash, peer_id):
        self.__perform_handshake__(info_hash, peer_id)
        self.bitfield = self.__receive_bitfield__()
        self.peer_id = peer_id
        self.info_hash = info_hash
        self.peer = peer
        self.choked = True

    def send_unchoke(self):
        message = Message(Message.UNCHOKE,None)
        self.socket_connection.send(message.serialize())


    def __perform_handshake__(self, info_hash, peer_id):
        self.peer.connect()
        handshake = Handshake(info_hash, peer_id)
        self.peer.send(handshake.serialize())
        handshake_resp = handshake.deserialize(self.peer.receive())
        if handshake_resp.peer_id != handshake.peer_id:
            raise ConnectionError("peer_id mismatch")

    def __receive_bitfield__(self):
        data = self.peer.receive()
        id, payload = Message.receive(data)
        if id != "Bitfield":
            raise ConnectionError(format("expected bitfield, got {}", id))
        return Bitfield(payload)


