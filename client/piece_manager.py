# track pieces
import math, os
import struct
import hashlib
from protocol import check_peer_response, recv_exact
from progress_manager import show_progress, save_progress

global peer_bitfield

def save_piece(piece_index, piece_data, name):
    os.makedirs(f"output/{name}", exist_ok=True)
    filename = f"output/{name}/{piece_index}.bin"

    with open(filename, "wb") as f:
        f.write(piece_data)

def peer_has_piece(bitfield, piece_index):
    byte_index = piece_index // 8
    bit_index = 7 - (piece_index % 8)

    if byte_index >= len(bitfield):
        return False

    return (bitfield[byte_index] >> bit_index) & 1

def get_piece_length(piece_index, piece_length, total_length, num_pieces):
    if piece_index == num_pieces - 1:
        return total_length - piece_length * (num_pieces - 1)
    return piece_length

# def download_one_block(s, index=0, begin=0, length=16384): # the one block is real
#     # now we are talking, with the peer ofc
#     # print(f"\nStart talking to peer\n")
    
#     payload = struct.pack(">III", index, begin, length)
#     msg = struct.pack(">I", 13) + bytes([6]) + payload

#     s.send(msg)

#     while True:
#         try:
#             length_bytes = recv_exact(s, 4)
#         except TimeoutError:
#             return None

#         length = struct.unpack(">I", length_bytes)[0]

#         if length == 0:
#             print("keep-alive")
#             continue
#         else:
#             msg = recv_exact(s, length)
#             msg_id = msg[0]
#             payload = msg[1:]

#             # print(f"Received msg: {msg_id}")
#             if msg_id == 7:
#                 if len(payload) < 8:
#                     print("Invalid block payload")
#                     return None

#                 resp_index = struct.unpack(">I", payload[0:4])[0]
#                 resp_begin = struct.unpack(">I", payload[4:8])[0]
#                 if index != resp_index or begin != resp_begin:
#                     print("Got wrong block, ignoring")
#                     continue
#                 block = payload[8:]
#                 # print(len(block))
#                 return block
            
#             elif msg_id == 5:
#                 print("got bitfield")
#                 peer_bitfield = payload

#             # elif msg_id == 0:
#             #     print("got choked")

#             # elif msg_id == 1:
#             #     print("got unchoked")


# def download_from_peer(s, piece_index, piece_length, pieces_hash):
#     piece_data = b''
#     total_blocks = math.ceil(piece_length / 16384)

#     for i, begin in enumerate(range(0, piece_length, 16384), start=1):
#         length = min(16384, piece_length - begin)

#         block = download_one_block(s, piece_index, begin=begin, length=length)

#         if block is None:
#             print(f"\nBlock failed!\n")
#             return None

#         piece_data += block
#         print(f"{i}/{total_blocks} blocks downloaded", end='\r', flush=True)

#     print("")

#     # Ensure full piece received
#     if len(piece_data) != piece_length:
#         print("Incomplete piece")
#         return None

#     # Verify hash
#     hash_val = hashlib.sha1(piece_data).digest()
#     torr_hash = pieces_hash[piece_index*20:(piece_index+1)*20]

#     if hash_val == torr_hash:
#         return piece_data
#     else:
#         print(f"piece {piece_index} is wrong")
#         return None
    

def download_with_multiple_peers(num_pieces, working_peers, piece_length, pieces, name, downloaded_pieces, total_length):

    for peer, s, bitfield in working_peers:
        print(f"\nUsing peer {peer}")

        for piece_index in range(num_pieces):
            if piece_index in downloaded_pieces:
                continue

            if bitfield and not peer_has_piece(bitfield, piece_index):
                continue

            piece_data = download_piece_pipelined(
                s, piece_index, piece_length, pieces, total_length, num_pieces
            )

            if piece_data is None:
                continue

            save_piece(piece_index, piece_data, name)
            downloaded_pieces.add(piece_index)
            save_progress(name, num_pieces, downloaded_pieces)


            print(f"\nPiece {piece_index} saved") # hash is already verified
            show_progress(downloaded_pieces, num_pieces)

            return True  # progress made

    return False

def download_piece_pipelined(s, piece_index, piece_length, pieces_hash, total_length, num_pieces):
    p_length = get_piece_length(piece_index, piece_length, total_length, num_pieces)
    piece_length = p_length

    block_size = 16384
    total_blocks = (piece_length + block_size - 1) // block_size

    piece_data = [None] * total_blocks

    pipeline = 5  # number of requests in flight
    requested = 0
    received = 0


    # send initial pipeline
    for _ in range(min(pipeline, total_blocks)):
        begin = requested * block_size
        length = min(block_size, piece_length - begin)

        payload = struct.pack(">III", piece_index, begin, length)
        msg = struct.pack(">I", 13) + bytes([6]) + payload
        s.send(msg)

        requested += 1

    while received < total_blocks:
        try:
            length_prefix = recv_exact(s, 4)
        except:
            return None

        msg_len = struct.unpack(">I", length_prefix)[0]

        if msg_len == 0:
            continue

        msg = recv_exact(s, msg_len)
        msg_id = msg[0]
        payload = msg[1:]

        if msg_id == 7:
            index = struct.unpack(">I", payload[0:4])[0]
            begin = struct.unpack(">I", payload[4:8])[0]
            block = payload[8:]

            block_index = begin // block_size
            piece_data[block_index] = block
            received += 1

            print(f"{received}/{total_blocks} blocks", end='\r', flush=True)

            # send next request
            if requested < total_blocks:
                begin = requested * block_size
                length = min(block_size, piece_length - begin)

                payload = struct.pack(">III", piece_index, begin, length)
                msg = struct.pack(">I", 13) + bytes([6]) + payload
                s.send(msg)

                requested += 1

        elif msg_id == 0:
            print("Choked mid-piece")
            return None

        elif msg_id == 1:
            continue

    # assemble piece
    full_piece = b''.join(piece_data)

    # verify
    hash_val = hashlib.sha1(full_piece).digest()
    torr_hash = pieces_hash[piece_index*20:(piece_index+1)*20]

    if hash_val == torr_hash:
        return full_piece
    else:
        print(f"Piece {piece_index} failed hash")
        return None