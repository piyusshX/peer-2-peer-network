# This files combines our modules and does the deed. read 01Please_read_this.txt to know how much it does. 
# We may add a gui main that replaces this, this main works in terminal

import os
import requests
import socket
import struct
from decoder import main as decode, load_and_decode
from encoder import main as bencode
from info_hash import calculate_info_hash
from tracker import contact_tracker, get_peer_list
from peer import contact_peer
from protocol import check_peer_response
from piece_manager import download_from_peer

peer_id = b'-PC0001-' + os.urandom(12)
torr_file = 'c:/Projects/torrent/peer-2-peer-network/examples/1134459.torrent'


if __name__=="__main__":
    try:
        # step 1: decode the .torrent file and store it in memory as a dict
        torr_dict = load_and_decode(torr_file) # global torrent file data
        pieces = torr_dict[b'info'][b'pieces'] # piece hashes
        piece_length = torr_dict[b'info'][b'piece length']
        num_pieces = len(pieces) // 20
        print(f"{num_pieces} pieces hashes found in file") # but last piece may be smaller

        # step 2: contact tracker with my peer id and get peer list from tracker
        info_hash, tracker_response = contact_tracker(peer_id, torr_dict)

        ipv4_peer_bytes = tracker_response[b'peers']
        seeders = tracker_response[b'complete']
        leechers = tracker_response[b'incomplete']
        downloaded = tracker_response[b'downloaded']
        peer_list = get_peer_list(ipv4_peer_bytes)
        print(f"seeders: {seeders}, leechers: {leechers}, downloaded: {downloaded}", flush=True)
        print(f"peers found: {len(peer_list)}", flush=True)

        # step 3: contact a peer and do a handshake
        s = contact_peer(my_peer_id=peer_id, peer_list=peer_list, info_hash=info_hash)
        # here s is the peer that has unchoked us and we can start downloading from it

        # step 4: download from peer
        download_from_peer(s, 0, piece_length, pieces)



    except Exception as e:
        print(e)
