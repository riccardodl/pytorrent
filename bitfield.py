class Bitfield(object):
    def __init__(self, bitfield):
        self.bitfield = bitfield


    def has_piece(self, index):
        byte_index = index / 8
        bit_offset = index % 8
        return (self.bitfield[byte_index] >> (7 - bit_offset)) & 1 != 0

    def set_piece(self, index):
        byte_index = index / 8
        bit_offset = index % 8
        self.bitfield[byte_index] |= 1 << (7 - bit_offset)
