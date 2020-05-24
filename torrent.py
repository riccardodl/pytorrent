import hashlib
import bencoding
import requests
import json
class Torrent(object):
    def __init__(self, data):
        self.data = data
        self.info_hash = self.sha1_hash()
        self.piece_length = data[b'info'][b'piece length']
        self.length = data[b'info'][b'length']
        self.name = data[b'info'][b'name']
        self.announce = data[b'announce']
        self.piece_hashes = self.get_pieces()

    def get_pieces(self):
        info_string = self.data[b'info'][b'pieces']
        total_length = len(info_string)
        piece_length = 20
        if total_length%piece_length != 0:
            raise ValueError("Pieces length is unexpected value {0}",total_length)
        piece_hashes = [info_string[i:i + piece_length] for i in range(0, total_length, piece_length)]
        return piece_hashes

    def sha1_hash(self):
        #info_hash = hashlib.sha1(bencoding.bencode(self.decodedDict[b"info"])).hexdigest()
        info_hash = hashlib.sha1(self.data[b'info']).hexdigest()
        print(info_hash)
        return info_hash
