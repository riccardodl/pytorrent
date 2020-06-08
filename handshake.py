from struct import pack, unpack


class Handshake(object):
    PSTR = b"BitTorrent protocol"

    def __init__(self, info_hash, peer_id):
        self.ext_flags = bytearray(8)
        self.info_hash = info_hash
        self.peer_id = peer_id

    def serialize(self):
        buf = pack(">b 19s 8s 20s 20s",
                   len(self.PSTR),
                   self.PSTR,
                   self.ext_flags,
                   self.info_hash,
                   self.peer_id)
        return buf

    @classmethod
    def deserialize(cls, data):
        len_pstr, pstr, ext_flags, info_hash, peer_id = unpack(">b 19s 8s 20s 20s", data)
        if len_pstr != len(cls.PSTR) or pstr != cls.PSTR:
            raise ValueError("incorrect or malformed pstr")
        return Handshake(info_hash, peer_id)
