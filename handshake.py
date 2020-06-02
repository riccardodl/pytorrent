class Handshake(object):
    def __init__(self, info_hash, peer_id):
        self.pstr = b"BitTorrent protocol"
        self.ext_flags = bytearray(8)
        self.info_hash = str.encode(info_hash)
        self.peer_id = str.encode(peer_id)

def serialize(handshake):
    buf = "".join(str(len(handshake.pstr)).encode("utf-8") + handshake.pstr + handshake.ext_flags + handshake.info_hash + handshake.peer_id )
    return buf

def deserialize(data):
    info_hash = data[28:48]
    peer_id=data[48:]
    handshake = Handshake(info_hash,peer_id)
    return handshake
