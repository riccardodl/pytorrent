from peer import get_peers
import queue
from client import Client

class WorkPiece(object):
    def __init__(self,index,length,hash):
        self.index = index
        self.length = length
        self.hash = hash

def download(torrent, peers):
    work_queue = queue.Queue(maxsize=len(torrent.piece_hashes))
    done_pieces = queue.Queue(maxsize=len(torrent.piece_hashes))
    for index, hash in enumerate(torrent.piece_hashes):
        length = get_piece_length(torrent)
        work_queue.put(WorkPiece(index,length,hash))

    for peer in peers:
        try:
            start_worker(peer, torrent, work_queue, done_pieces)
        except Exception as e:
            print("Something went wrong with this client - {}".format(e))

    done_pieces_count = 0
    downloaded_file = []
    while done_pieces_count < len(torrent.piece_hashes):
        #Take a work unit from the queue
        #Take a client that has it and get it
        #Remove the element from the work queue
        #Add the data to the downloaded file (in memory) (at the correct position!)
        res = done_pieces.pop()
        begin, end = get_bounds(res.index)

        downloaded_file[begin:end] = res.buf[:]

        done_pieces_count+=1


def get_piece_length(torrent):
    return 0 # todo

def get_bounds(index):
    return 0, 1 #TODO

# Make a client for each peer
def start_worker(peer, torrent, work_queue, done_pieces):
    client = Client(peer, torrent.info_hash, torrent.peer_id)
    client.send_unchoke()
    client.send_interested()

    for pc in range(work_queue):
        if not client.bitfield.has_piece(pc):
            work_queue.put(pc)
        try:
            dl = attempt_download(pc)
            if check_integrity(dl):
                done_pieces.put(dl)
            else:
                print("Corrupted piece, putting back into todo")
                work_queue.put(pc)
        except Exception as e:
            work_queue.put(pc)
