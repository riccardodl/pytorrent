from bitfield import Bitfield
from handshake import Handshake
from message import Message
import socket


class Client(object):
    BUFFER_SIZE = 1024

    def __init__(self, peer, info_hash, peer_id):
        raw_bitfield, s = __perform_handshake__(peer, info_hash, peer_id)
        self.bitfield = __receive_bitfield__(raw_bitfield)
        self.peer_id = peer_id
        self.info_hash = info_hash
        self.socket = s
        self.peer = peer
        self.choked = True

    def send_unchoke(self):
        message = Message(Message.UNCHOKE,None)
        self.socket_connection.send(message.serialize())


def __perform_handshake__(peer, info_hash, peer_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.settimeout(3.0)
    addr =(str(peer.ip),peer.port)
    s.connect(addr)
    print(info_hash, peer_id)

    handshake = Handshake(info_hash, peer_id)
    s.send(handshake.serialize())
    response = s.recv(Client.BUFFER_SIZE)
    print(response)
    handshake_resp = handshake.receive(response)
    if handshake_resp.info_hash != handshake.info_hash:
        raise ConnectionError("info hash mismatch")
    return handshake_resp.peer_id, s

def __receive_bitfield__(data):
    id, payload = Message.receive(data)
    if id != "Bitfield":
        raise ConnectionError(format("expected bitfield, got {}",id))
    return Bitfield(payload)

