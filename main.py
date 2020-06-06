import string
from bencode_parser import *
from torrent import *
import random
from peer import get_peers
import client

if __name__ == '__main__':
    peer_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

    file = open('debian-10.3.0-amd64-netinst.iso.torrent', 'rb').read()
    torrent = Torrent(decode(file))
    url = torrent.build_tracker_url(peer_id, 80)
    response = torrent.retrieve_response(url)
    peers = get_peers(response)
    [print("ip: {}, port: {}".format(p.ip,p.port)) for p in peers]
    worker = client.new_client(peers[0],peer_id,torrent.info_hash)

