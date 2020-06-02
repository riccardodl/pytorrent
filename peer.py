from bencode_parser import *
import ipaddress

class Peer(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

def get_peers(bencode):
    ip_port = []
    peer_len = 6
    ip_len = 4
    content = decode(bencode)
    assert content
    peers = content[b'peers']
    assert len(peers) % peer_len == 0

    for i in range(0, len(peers), peer_len):
        ip = ipaddress.IPv4Address(peers[i: i + ip_len])
        port = int.from_bytes(peers[i + ip_len:i + peer_len], "big")
        assert port <= 65535
        ip_port.append(Peer(ip,port))
    return ip_port