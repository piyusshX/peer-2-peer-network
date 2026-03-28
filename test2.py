import requests
from b_decoder import main as decode, load, save
from bencoding import main as bencode
from info_hash import main as calculate_info_hash
from pathlib import Path

def test_decoder_first(input, show_in_terminal=False):
    # load a .torrent file
    status, *rest = load(input)
    if status == 0:
        stem, parent, source = rest[0], rest[1], rest[2]
    else:
        return 1, f"Error while loading: \n {rest[-1]}"
    
    # decode the torrent file
    status, *rest = decode(source)
    if status != 0:
        return 1, f"Error while decoding: \n {rest[-1]}"
    decoded_data = rest[0]
    # status = save(stem, parent, decoded_data)
    # if status != 0:
    #     print(f"Failed to save the decoded file as {stem}.bin. Continueing to verify...", flush=True)
    # print(decoded_data)
    info_hash = calculate_info_hash(decoded_data)
    announce_url = decoded_data[b'announce'] # getting the announce url
    # Parameters
    params = {
        'info_hash' : info_hash,
        'peer_id' : '2626277',
        'port': 6881,
        'uploaded': 1,
        'downloaded': 1,
        'left': 57479,
        'compact': 1,
        'event': 'started'
    }

    response = requests.get(announce_url, params=params)
    print(response) # <Response [400]>
    decoded_res = decode(response)
    print(decoded_res)

    return 0, f"tests completed!"


if __name__ == "__main__":
    try:
        show_in_terminal = True # Recommended False for bigger files, else the terminal will be cluttered
        status, *rest = test_decoder_first('C:/Users/91626/Desktop/p2p_project/example.torrent', show_in_terminal)
        print(f"{rest[-1]}")

        # status, *rest = test_encoder_first("c:/Projects/torrent/peer-2-peer-network/examples/exampleString.bin")
        # print(f"test 2 results:\n{rest[-1]}")
    except:
        print("Some exception occured")

        