from bencode_parser import *
from torrent import *
from peer import get_peers
from client import Client
from p2p import download
import random
import string

if __name__ == '__main__':
    file = open('debian-10.3.0-amd64-netinst.iso.torrent', 'rb').read()
    torrent = Torrent(decode(file))
    url = torrent.build_tracker_url(torrent.peer_id, 80)
    response = torrent.retrieve_response(url)
    peers = get_peers(response)

    #This will go into p2p
    #worker = Client(peers[3],torrent.info_hash,peer_id)
    #worker.send_unchoke()
    # then send interested, then start download pieces, then put them together
    download(torrent, peers)
    #remove peers if they don't respond


