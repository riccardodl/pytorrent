from peer import get_peers
from client import new_client

class WorkPiece(object):
    def __init__(self,index,length,hash):
        self.index = index
        self.length = length
        self.hash = hash

def get_piece_length(torrent):
    return 0 # todo

def start_worker(peer, torrent, work_queue, done_pieces):
    client = new_client(peer,torrent.peer_id, torrent.info_hash)
    client.send_unchoke()
    client.send_interested()


def get_bounds(index):

def download(torrent):
    work_queue = []
    done_pieces = []
    for index, hash in range(len(torrent.piece_hashes)):
        length = get_piece_length(torrent)
        work_queue.append(WorkPiece(index,length,hash))


    for peer in range(get_peers):
        start_worker(peer, torrent, work_queue, done_pieces)

    done_pieces_count = 0
    downloaded_file = []
    while done_pieces_count < len(torrent.piece_hashes):
        res = done_pieces.pop()
        begin, end = get_bounds(res.index)

        downloaded_file[begin:end] = res.buf[:]

        done_pieces_count+=1