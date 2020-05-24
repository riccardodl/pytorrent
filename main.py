from bencode_parser import *
from request import *
from torrent import *
import random

if __name__ == '__main__':
    # file = open('test.txt','r')
    file = open('debian-10.3.0-amd64-netinst.iso.torrent', 'rb').read()
    torrent = Torrent(decode(file))
    request = Request(torrent)
    peer_id = bytearray(random.getrandbits(8) for _ in range(20))
    url = request.build_tracker_url(peer_id, 80)
    print(url)
    request.retrieve_peers(url)
