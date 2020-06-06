class Handshake(object):
    def __init__(self, info_hash, peer_id):
        self.pstr = b"BitTorrent protocol"
        self.ext_flags = bytearray(8)
        self.info_hash = str.encode(info_hash)
        self.peer_id = str.encode(peer_id)

    def serialize(self):
        buf = "".join(str(len(self.pstr)).encode("utf-8") + self.pstr + self.ext_flags + self.info_hash +
                      self.peer_id )
        return buf

    def receive(self,stream):
        data = stream.read()#TODO
        self.info_hash = data[28:48]
        self.peer_id=data[48:]
        return data
