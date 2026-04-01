# This file cotacts tracker to get peer ip addresses, renamed from test2.py and discover_peer.py
import os
import requests
from info_hash import calculate_info_hash
from decoder import main as decode, load_and_decode

def contact_tracker(peer_id, torr_dict, length):
    info_hash = calculate_info_hash(torr_dict)
    announce_url = torr_dict[b'announce'] # getting the announce url
    # Parameters
    params = {
        'info_hash' : info_hash,
        'peer_id' : peer_id, # 20 byte peer id
        'port': 6881,
        'uploaded': 0,
        'downloaded': 0,
        'left': length,
        'compact': 1,
    }

    response = requests.get(announce_url, params=params)
    if response.status_code != 200:
        print(f"Error \n {response}")
        return
    status, *rest = decode(response._content)
    if status == 0:
        return info_hash, rest[0]
    else:
        print("error decoding response content")
        return {}

def get_peer_list(peers_bytes):
    peers = []
    
    for i in range(0, len(peers_bytes), 6):
        ip_bytes = peers_bytes[i:i+4]
        port_bytes = peers_bytes[i+4:i+6]
        
        ip = ".".join(str(b) for b in ip_bytes)
        port = int.from_bytes(port_bytes, 'big')
        peer = ip + ":" + str(port)
        peers.append(peer)
    return peers

if __name__ == "__main__":
    # IMPORTANT
    # b'peers' returns all ipv4 peers, b'peers6' returns ipv6 peers
    # we dont support ipv6 peers

    peer_id = b'-PC0001-' + os.urandom(12)
    torr_file = 'c:/Projects/torrent/peer-2-peer-network/examples/2033398.torrent'

    torr_dict = load_and_decode(torr_file) # global torrent file data

    tracker_resp = contact_tracker(peer_id, torr_dict)
    print(tracker_resp)
    peer_list = get_peer_list(peers_bytes=tracker_resp[b'peers'])
    print(peer_list)