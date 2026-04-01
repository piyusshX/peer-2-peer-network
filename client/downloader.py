# the greatest loop of all time that combines pieces to download the file
import os
from peer import contact_peer
from piece_manager import download_from_peer
from progress_manager import save_progress, load_progress, show_progress

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
    total, downloaded_pieces = load_progress(name)

    if total == 0:
        total = num_pieces

    working_peers = []

    # MAIN LOOP: until all pieces done
    while len(downloaded_pieces) < num_pieces:

        progress_made = False

        # 1. TRY WORKING PEERS FIRST
        for peer, s, bitfield in working_peers[:]:
            try:
                print(f"\nUsing working peer {peer}")

                for piece_index in range(num_pieces):
                    if piece_index in downloaded_pieces:
                        continue

                    if bitfield and not peer_has_piece(bitfield, piece_index):
                        continue

                    print(f"Downloading piece {piece_index} from working peer")

                    piece_data = download_from_peer(s, piece_index, piece_length, pieces)

                    if piece_data is None:
                        continue

                    save_piece(piece_index, piece_data, name)
                    downloaded_pieces.add(piece_index)
                    save_progress(name, num_pieces, downloaded_pieces)

                    print(f"Piece {piece_index} saved")
                    show_progress(downloaded_pieces, num_pieces)

                    progress_made = True

                # keep using this peer
            except Exception:
                print(f"Peer {peer} failed, removing")
                try:
                    s.close()
                except:
                    pass
                working_peers.remove((peer, s, bitfield))

        # 2. IF NO PROGRESS → FIND NEW PEERS
        if not progress_made:
            print("\nSearching for new working peers...")

            for i, peer in enumerate(peer_list):
                try:
                    print(f"Trying peer {i+1}/{total_peers}", end='\r', flush=True)

                    s, bitfield = contact_peer(
                        my_peer_id=peer_id,
                        peer=peer,
                        info_hash=info_hash
                    )

                    print(f"\nConnected to {peer}")

                    # try downloading ONE piece to validate peer
                    for piece_index in range(num_pieces):
                        if piece_index in downloaded_pieces:
                            continue

                        if bitfield and not peer_has_piece(bitfield, piece_index):
                            continue

                        piece_data = download_from_peer(s, piece_index, piece_length, pieces)

                        if piece_data is None:
                            continue

                        # ✅ success → promote to working peer
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

                except Exception:
                    continue

        # ❌ If still no progress → exit
        if not progress_made:
            print("\nNo progress possible. Stopping.")
            break

    # cleanup
    for _, s, _ in working_peers:
        try:
            s.close()
        except:
            pass