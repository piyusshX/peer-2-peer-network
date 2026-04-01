# the greatest loop of all time that combines pieces to download the file
import os
from peer import contact_peer
from piece_manager import save_piece, peer_has_piece, download_with_multiple_peers, download_piece_pipelined
from progress_manager import save_progress, load_progress, show_progress

def create_empty_file(filename, total_size):
    with open(filename, "wb") as f:
        f.truncate(total_size)
        

def download_and_save(num_pieces, peer_list, peer_id, info_hash, piece_length, pieces, name, total_length):
    total, downloaded_pieces = load_progress(name)
    if total == 0:
        total = num_pieces

    working_peers = []

    while len(downloaded_pieces) < num_pieces:

        progress_made = False

        # ✅ 1. try existing working peers
        if working_peers:
            progress_made = download_with_multiple_peers(
                num_pieces,
                working_peers,
                piece_length,
                pieces,
                name,
                downloaded_pieces,
                total_length
            )

        # ✅ 2. if no progress → find new peer
        if not progress_made:
            for peer in peer_list:
                try:
                    s, bitfield = contact_peer(peer_id, peer, info_hash)

                    # try downloading ONE piece
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

                        # ✅ promote to working peer
                        working_peers.append((peer, s, bitfield))

                        save_piece(piece_index, piece_data, name)
                        downloaded_pieces.add(piece_index)
                        save_progress(name, num_pieces, downloaded_pieces)

                        print(f"Piece {piece_index} saved (new peer)")
                        show_progress(downloaded_pieces, num_pieces)

                        progress_made = True
                        break

                    if progress_made:
                        break
                    else:
                        s.close()

                except:
                    continue

        if not progress_made:
            print("No progress possible")
            break