class Handshake(object):
    def __init__(self, info_hash, peer_id):
        self.pstr = b"BitTorrent protocol"
        self.ext_flags = bytearray(8)
        self.info_hash = str.encode(info_hash)
        self.peer_id = str.encode(peer_id)

    def serialize(self):
        buf = str(len(self.pstr)).encode("utf-8") + self.pstr + self.ext_flags + self.info_hash + self.peer_id
        return buf

    def receive(self, data):
        pstr = int(data[0])
        if pstr == 0:
            raise ValueError("pstr cannot be zero")
        info_hash = data[28:48]
        peer_id = data[48:]
        return Handshake(info_hash,peer_id)
