from enum import Enum
from struct import pack, unpack

class MessageCodes(Enum):
    CHOKE = 0
    UNCHOKE = 1
    INTERESTED = 2
    NOT_INTERESTED = 3
    HAVE = 4
    BITFIELD = 5
    REQUEST = 6
    PIECE = 7
    CANCEL = 8

class Message(object):

    def __init__(self, id, message):
        self.id = id
        self.message = message

    def serialize(self):
        msg_len = len(self.payload) + 1
        len = msg_len.to_bytes(4, "big")
        return pack(">b 4s 1s {}s".format(len(self.message)),
                    len,
                    self.id,
                    self.message)

    @classmethod
    def deserialize(cls, data):
        msg_len, msg_id, msg_payload = unpack("> 4s 1s {}s".format(len(data)-5), data)
        if msg_len == 0:
            return None
        return Message(msg_id, msg_payload)

