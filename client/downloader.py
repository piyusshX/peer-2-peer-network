# the greatest loop of all time that combines pieces to download the file
import os
from peer import contact_peer
from piece_manager import download_from_peer

def create_empty_file(filename, total_size):
    with open(filename, "wb") as f:
        f.truncate(total_size)

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

def download_and_save(num_pieces, peer_list, peer_id, info_hash, piece_length, pieces, name):
    total_peers = len(peer_list)
    for piece_index in range(num_pieces):
        print(f"\nDownloading piece {piece_index}")
        i = 0

        for peer in peer_list:
            i+=1
            try:
                # handshake + get unchoked
                print(f"Trying peer {i}/{total_peers}", end='\r', flush=True)
                s, bitfield = contact_peer(my_peer_id=peer_id, peer=peer, info_hash=info_hash)
                print(f"")

                # if not peer_has_piece(bitfield, piece_index):
                #     print(f"\npeer {i} does not have piece\n")
                #     continue

                # download a piece from peer
                piece_data = download_from_peer(s, piece_index, piece_length, pieces)

                if piece_data is None:
                    continue

                # piece hash is already verified
                save_piece(piece_index, piece_data, name)
                print(f"Piece {piece_index} saved")
                break

            except Exception as e:
                # print(f"Exception raised: {e}")
                continue
        else:
            print(f"\nNo peer offered piece {piece_index}")
            i = 0

        # # manual stopper
        # if piece_index == 10:
        #     print(f"stopping after piece {piece_index}")
        #     break
    
    return


