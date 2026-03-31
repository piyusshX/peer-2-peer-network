# track pieces
import struct
import hashlib
from protocol import check_peer_response

def download_one_block(s, index=0, begin=0, length=16384): # the one block is real
    # now we are talking, with the peer ofc
    # print(f"\nStart talking to peer\n")
    
    payload = struct.pack(">III", index, begin, length)
    msg = struct.pack(">I", 13) + bytes([6]) + payload

    s.send(msg)

    while True:
        peer_resp, payload = check_peer_response(s)
        if peer_resp == 7:
            break

        if peer_resp == 0:
            return None

        if peer_resp == 400: # 1 for being unchoeked, 400 for facing timeout
            return None
        
        else:
            continue

    if peer_resp == 7:
        if len(payload) < 8:
            print("Invalid piece payload")
            return None

        resp_index = struct.unpack(">I", payload[0:4])[0]
        resp_begin = struct.unpack(">I", payload[4:8])[0]
        if not (index == resp_index or begin == resp_begin):
            print("Got wrong block, ignoring")
            return None
        
        block = payload[8:]
        # print(len(block))
        return block

def download_from_peer(s, piece_index, piece_length, pieces_hash):
    piece_data = b''
    i = 0
    for begin in range(0, piece_length, 16384):
        print(f"Downloading block {i}")
        length = min(16384, piece_length - begin)
        block = download_one_block(s, piece_index, begin=begin, length=length)
        i+=1
        if block is None:
            print("Block failed!")
            break
        piece_data += block

    # verification of ONE PIECE
    # hash = hashlib.sha1(piece_data).digest()
    # print(f"hash of downloaded piece: \n{hash}")   
    # torr_hash = pieces_hash[0:20]
    # print(torr_hash)
    # print(hash == torr_hash)
