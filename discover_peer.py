import requests
from decoder import type_checker
from info_hash import calculate_info_hash

def discover_peer(torr_str):
    decoded_dict = type_checker(torr_str) # decoding the torrent file/string
    decoded_dict = decoded_dict[0] # decoded dict
    announce_url = decoded_dict['announce'] # getting the announce url
    info_hash = calculate_info_hash(decoded_dict)
    left = decoded_dict['info'][b'length'] # getting the length of the file to be downloaded
    # Parameters
    params = {
        'info_hash' : info_hash,
        'peer_id' : 12345678901234567890,
        'port': 6881,
        'uploaded': 0,
        'downloaded': 0,
        'left': left,
        'compact': 1,
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