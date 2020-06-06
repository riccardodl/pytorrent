class Message(object):
    CHOKE = 0
    UNCHOKE = 1
    INTERESTED = 2
    NOT_INTERESTED = 3
    HAVE = 4
    BITFIELD = 5
    REQUEST = 6
    PIECE = 7
    CANCEL = 8

    def __init__(self, id, message):
        self.id = id
        self.message = message

    def serialize(self):
        msg_len = len(self.payload) + 1
        bytes_msg = bytearray()
        bytes_msg.append(msg_len.to_bytes(4,"big"))
        bytes_msg.append(self.id)
        bytes_msg.append(self.payload)
        return bytes_msg

    def receive(self, data):
        msg_len = int.from_bytes(data[:4],"big")
        if msg_len == 0:
            return None
        msg_id = int.from_bytes(data[4],"big")
        msg_payload = data[5:].decode("utf-8")
        return msg_id, msg_payload

