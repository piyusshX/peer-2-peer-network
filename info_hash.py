import hashlib
from decoder import type_checker
from bencoding import encode_dict

def main(torr_str):
    decoded_dict = type_checker(torr_str) # decoding the torrent file/string
    decoded_dict = decoded_dict[0] # decoded dict
    if 'info' not in decoded_dict:
        raise ValueError("Info dictionary is not present in torrent!")
    
    info = decoded_dict['info'] # extracing info dict from torrent dict
    encoded_info = encode_dict(info) # Re-encoding info dict to calculate info hash

    info_hash = hashlib.sha1(encoded_info).digest() # Sha1 hash
    return info_hash