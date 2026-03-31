import hashlib
from bencoding import encode_dict


"String version is not useful I guess but keeping it since i wasted my time writing it."
# def calculate_info_hash_from_str(torr_str):
#     decoded_dict = type_checker(torr_str) # decoding the torrent file/string
#     decoded_dict = decoded_dict[0] # decoded dict
#     if b'info' not in decoded_dict:
#         raise ValueError("Info dictionary is not present in torrent!")
    
#     info = decoded_dict[b'info'] # extracing info dict from torrent dict
#     encoded_info = encode_dict(info) # Re-encoding info dict to calculate info hash

#     info_hash = hashlib.sha1(encoded_info).digest() # Sha1 hash
#     return info_hash

def calculate_info_hash(torr_dict):
    if b'info' not in torr_dict:
        raise ValueError("Info dictionary is not present in torrent!")
    
    info = torr_dict[b'info'] # extracing info dict from torrent dict
    encoded_info = encode_dict(info) # Re-encoding info dict to calculate info hash

    info_hash = hashlib.sha1(encoded_info).digest() # Sha1 hash
    return info_hash


def main(torr_dict):
    return calculate_info_hash(torr_dict)