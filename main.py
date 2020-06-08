import string
from bencode_parser import *
from torrent import *
import random
from peer import get_peers
from client import Client
from p2p import download

if __name__ == '__main__':
    peer_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)).encode("utf-8")

    file = open('debian-10.3.0-amd64-netinst.iso.torrent', 'rb').read()
    torrent = Torrent(decode(file))
    url = torrent.build_tracker_url(peer_id, 80)
    response = torrent.retrieve_response(url)
    peers = get_peers(response)
    [print("ip: {}, port: {}".format(p.ip,p.port)) for p in peers]

    #This will go into p2p
    worker = Client(peers[0],torrent.info_hash,peer_id)
    worker.send_unchoke()
    # then send interested, then start download pieces, then put them together
    #download(torrent)
    #remove peers if they don't respond


