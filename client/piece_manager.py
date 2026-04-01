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
    total_blocks = math.ceil(piece_length / 16384)

    for i, begin in enumerate(range(0, piece_length, 16384), start=1):
        length = min(16384, piece_length - begin)

        block = download_one_block(s, piece_index, begin=begin, length=length)

        if block is None:
            print(f"\nBlock failed!\n")
            return None

        piece_data += block
        print(f"{i}/{total_blocks} blocks downloaded", end='\r', flush=True)

    print("")

    # Ensure full piece received
    if len(piece_data) != piece_length:
        print("Incomplete piece")
        return None

    # Verify hash
    hash_val = hashlib.sha1(piece_data).digest()
    torr_hash = pieces_hash[piece_index*20:(piece_index+1)*20]

    if hash_val == torr_hash:
        return piece_data
    else:
        print(f"piece {piece_index} is wrong")
        return None