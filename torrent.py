import hashlib
import bencoding
import message
import urllib.parse


class Torrent(object):
    def __init__(self, data):
        self.data = data
        self.info_hash = self.get_info_hash()
        self.piece_length = data[b'info'][b'piece length']
        self.length = data[b'info'][b'length']
        self.name = data[b'info'][b'name']
        self.announce = data[b'announce']
        self.piece_hashes = self.get_pieces()

    def get_pieces(self):
        info_string = self.data[b'info'][b'pieces']
        total_length = len(info_string)
        piece_length = 20
        if total_length % piece_length != 0:
            raise ValueError("Pieces length is unexpected value {0}", total_length)
        piece_hashes = [info_string[i:i + piece_length] for i in range(0, total_length, piece_length)]
        return piece_hashes

    def get_info_hash(self):
        info = bencoding.bencode(self.data[b'info'])
        info_hash = hashlib.sha1(info).hexdigest()
        print(info_hash)
        return info_hash

    def build_tracker_url(self, peer_id, port):
        # Every 2 characters of the infohash need to be spaced by a "%" inbetween
        hash = self.info_hash
        hack = ''.join("%" + i + hash[n + 1] for n, i in enumerate(hash) if n % 2 == 0)
        parameters = {
            "info_hash": hack,
            "peer_id": peer_id,
            "port": str(port),
            "uploaded": str(0),
            "downloaded": str(0),
            "compact": str(1),
            "left": str(self.length),
        }

        headers = urllib.parse.urlencode(parameters, safe="%")
        return self.announce.decode("utf-8") + "?" + headers
        # req = PreparedRequest()
        # req.prepare_url(self.torrent.announce, parameters)
        # return req.url

    def retrieve_response(self, url):
        # works = "http://bttracker.debian.org:6969/announce?info_hash=%5a%80%62%c0%76%fa%85%e8%05%64%51%c0%d9" \
        #        "%aa%04%34%9a%e2%79%09&peer_id=ABCDEFGHIJKLMNOPQRST&port=80" \
        #        "&uploaded=0&downloaded=0&compact=1&left=351272960"
        # r2 = requests.get(works)
        # hashtest = "5a8062c076fa85e8056451c0d9aa04349ae27909"
        # doesntwork = "http://bttracker.debian.org:6969/announce?info_hash=5a8062c076fa85e8056451c0d9aa04349ae27909" \
        #             "&peer_id=ABCDEFGHIJKLMNOPQRST&port=80" \
        #             "&uploaded=0&downloaded=0&compact=1&left=351272960"

        r = message.get(url)
        return r.content
