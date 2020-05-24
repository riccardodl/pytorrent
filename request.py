import hashlib
import requests
import torrent
from requests.models import PreparedRequest


class Request(object):
    def __init__(self, torrent_data):
        self.torrent = torrent_data.Torrent

    def build_tracker_url(self,peer_id, port):
        parameters = {
            "info_hash": self.torrent.info_hash,
            "peer_id": peer_id,
            "port": port,
            "uploaded": 0,
            "downloaded": 0,
            "compact": 1,
            "left": self.torrent.length,
        }

        req = PreparedRequest()
        req.prepare_url(self.torrent.announce, parameters)
        return req.url


    def retrieve_peers(self, url):
        r = requests.get(url)
        return r
