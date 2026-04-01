# track pieces
import math
import struct
import hashlib
from protocol import check_peer_response, recv_exact

global peer_bitfield

def download_one_block(s, index=0, begin=0, length=16384): # the one block is real
    # now we are talking, with the peer ofc
    # print(f"\nStart talking to peer\n")
    
    payload = struct.pack(">III", index, begin, length)
    msg = struct.pack(">I", 13) + bytes([6]) + payload

    s.send(msg)

    while True:
        try:
            length_bytes = recv_exact(s, 4)
        except TimeoutError:
            return None

        length = struct.unpack(">I", length_bytes)[0]

        if length == 0:
            print("keep-alive")
            continue
        else:
            msg = recv_exact(s, length)
            msg_id = msg[0]
            payload = msg[1:]

            # print(f"Received msg: {msg_id}")
            if msg_id == 7:
                if len(payload) < 8:
                    print("Invalid block payload")
                    return None

                resp_index = struct.unpack(">I", payload[0:4])[0]
                resp_begin = struct.unpack(">I", payload[4:8])[0]
                if index != resp_index or begin != resp_begin:
                    print("Got wrong block, ignoring")
                    continue
                block = payload[8:]
                # print(len(block))
                return block
            
            elif msg_id == 5:
                print("got bitfield")
                peer_bitfield = payload

            # elif msg_id == 0:
            #     print("got choked")

            # elif msg_id == 1:
            #     print("got unchoked")


def download_from_peer(s, piece_index, piece_length, pieces_hash):
    piece_data = b''
    i = 1
    # print(f"piece length: {piece_length}")
    for begin in range(0, piece_length, 16384):
        # print(f"Downloading block {i}")
        length = min(16384, piece_length - begin)
        block = download_one_block(s, piece_index, begin=begin, length=length)
        if block is None:
            print("Block failed!", end='')
            break
        piece_data += block
        # print(f"Block  {i} downloaded of length {length}")
        print(f"{i}/{math.ceil(piece_length/16384)} blocks downloaded", end='\r', flush=True)
        i+=1
    print(f"\n")
    # verification of ONE PIECE
    hash = hashlib.sha1(piece_data).digest()
    torr_hash = pieces_hash[0:20]

    # print(f"hash of downloaded piece: \n{hash}")   
    # print(torr_hash)
    if hash == torr_hash:
        # print(f"hash matched")
        return piece_data
    else:
        print(f"piece {piece_index} is wrong")
        raise Exception("piece is wrong")