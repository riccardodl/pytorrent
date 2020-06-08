from bitfield import Bitfield
from handshake import Handshake
from message import Message
import socket


class Client(object):


    def __init__(self, peer, info_hash, peer_id):
        raw_bitfield = __perform_handshake__(peer, info_hash, peer_id)
        self.bitfield = __receive_bitfield__(raw_bitfield)
        self.peer_id = peer_id
        self.info_hash = info_hash
        self.peer = peer
        self.choked = True

    def send_unchoke(self):
        message = Message(Message.UNCHOKE,None)
        self.socket_connection.send(message.serialize())


def __perform_handshake__(peer, info_hash, peer_id):
    peer.connect()
    handshake = Handshake(info_hash, peer_id)
    peer.send(handshake.serialize())
    test_rcv = peer.receive()
    handshake_resp = handshake.deserialize(test_rcv)
    if handshake_resp.info_hash != handshake.info_hash:
        raise ConnectionError("info hash mismatch")
    return handshake_resp.peer_id

def __receive_bitfield__(data):
    id, payload = Message.receive(data)
    if id != "Bitfield":
        raise ConnectionError(format("expected bitfield, got {}",id))
    return Bitfield(payload)


