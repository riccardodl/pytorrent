class Requests(object):
    CHOKE = 0
    UNCHOKE = 1
    INTERESTED = 2
    NOT_INTERESTED = 3
    HAVE = 4
    BITFIELD = 5
    REQUEST = 6
    PIECE = 7
    CANCEL = 8

    def __init__(self, data):
        self.length = int.from_bytes(data[:4],"big")
        self.msg_id = int.from_bytes(data[5])
        self.payload = data[6:]