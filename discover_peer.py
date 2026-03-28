import requests
from decoder import type_checker
from info_hash import calculate_info_hash

def discover_peer(torr_str, peer_id, port, left):
    decoded_dict = type_checker(torr_str) # decoding the torrent file/string
    decoded_dict = decoded_dict[0] # decoded dict
    announce_url = decoded_dict['announce'] # getting the announce url
    info_hash = calculate_info_hash(decoded_dict)
    # Parameters
    params = {
        'info_hash' : info_hash,
        'peer_id' : peer_id,
        'port': port,
        'uploaded': 1,
        'downloaded': 1,
        'left': left,
        'compact': 1,
        'event': 'started'
    }
    response = requests.get(announce_url, params=params)
    decoded_res = type_checker(response)
    peers = parse_peers(decoded_res['peers'])
    return peers


def parse_peers(peers_bytes):
    peers = []
    
    for i in range(0, len(peers_bytes), 6):
        ip_bytes = peers_bytes[i:i+4]
        port_bytes = peers_bytes[i+4:i+6]
        
        ip = ".".join(str(b) for b in ip_bytes)
        port = int.from_bytes(port_bytes, 'big')
        peer = ip + ":" + str(port)
        peers.append(peer)
    return peers

def main(torr_str):
    return discover_peer(torr_str)