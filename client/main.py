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
from downloader import create_empty_file, save_piece, download_and_save
from progress_manager import load_progress, show_progress

peer_id = b'-PC0001-' + os.urandom(12)
torr_file = 'c:/Projects/torrent/peer-2-peer-network/examples/2092471.torrent'


if __name__=="__main__":
    try:
        # step 1: decode the .torrent file and store it in memory as a dict
        torr_dict = load_and_decode(torr_file) # global torrent file data
        pieces = torr_dict[b'info'][b'pieces'] # piece hashes
        piece_length = torr_dict[b'info'][b'piece length']
        name = torr_dict[b'info'][b'name'].decode() # name of the file/folder we are going to geet
        num_pieces = len(pieces) // 20

        print(f"target: {name}")
        print(f"{num_pieces} pieces hashes found in file") # but last piece may be smaller
        # calculating total size
        if b'length' in torr_dict[b'info']: # single file torrent
            length = torr_dict[b'info'][b'length']
        else: # multi file torrent
            length = sum(file[b'length'] for file in torr_dict[b'info'][b'files'])
        print(f"total file size: ~{int(length / (1024*1024))} Mib") # length in mb

        # step 2: contact tracker with my peer id and get peer list from tracker
        info_hash, tracker_response = contact_tracker(peer_id, torr_dict, length)

        ipv4_peer_bytes = tracker_response[b'peers']
        seeders = tracker_response[b'complete']
        leechers = tracker_response[b'incomplete']
        downloaded = tracker_response[b'downloaded']
        peer_list = get_peer_list(ipv4_peer_bytes)
        print(f"seeders: {seeders}, leechers: {leechers}, downloaded: {downloaded}", flush=True)
        print(f"peers found: {len(peer_list)}", flush=True)

        # step 3: contact the peers and download pieces
        # create_empty_file("output.file", total_size=length)
        download_and_save(num_pieces, peer_list, peer_id, info_hash, piece_length, pieces, name)

        # step 4: retry missing pieces:
        total, downloaded_pieces = load_progress(name)
        if total == 0:
            total = num_pieces
        missing = set(range(num_pieces)) - downloaded_pieces
        print(f"missing pieces:{missing}")
        show_progress(downloaded_pieces, num_pieces)

    except Exception as e:
        print(e)
