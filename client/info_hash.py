import hashlib
from encoder import encode_dict

def calculate_info_hash(torr_dict):
    if b'info' not in torr_dict:
        raise ValueError("Info dictionary is not present in torrent!")
    
    info = torr_dict[b'info'] # extracing info dict from torrent dict
    encoded_info = encode_dict(info) # Re-encoding info dict to calculate info hash

    info_hash = hashlib.sha1(encoded_info).digest() # Sha1 hash
    return info_hash


def main(torr_dict):
    return calculate_info_hash(torr_dict)