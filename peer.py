from bencode_parser import *
import ipaddress
import socket

class Peer(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.alive = False
        self.socket = None
        self.__data = b''

    def connect(self):
        try:
            self.socket = socket.create_connection((str(self.ip),self.port), timeout=3)
            #self.socket.setblocking(True)
            self.alive = True
        except Exception as e:
            print("Something went wrong while connecting to peer {} - {}".format(self.ip,e))

    def send(self, msg):
        try:
            self.socket.send(msg)
        except:
            self.alive = False
            print("Failed to send message, marking connection ad dead")

    def receive(self,buf_len = -1):
        BUFFER_SIZE = 1024
        while True:
            try:
                buffer = self.socket.recv(BUFFER_SIZE)
                if len(buffer) <= 0:
                    break
                self.__data += buffer
                #socket.error ???
            except Exception as e:
                print("receive failed - {}".format(e))
                break

        if buf_len == -1:
            data = self.__data
            self.__data = []
            return data
        elif len(self.__data) >= buf_len:
            data = self.__data[:buf_len]
            self.__data = self.__data[buf_len:]
            return data
        else:
            raise BufferError("You are trying to read more bytes than the peer has sent.")

def get_peers(bencode):
    peers_list = []
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
        peers_list.append(Peer(ip,port))
    return peers_list