from b_decoder import main as decode, load, save
from bencoding import main as bencode
from pathlib import Path

def test_decoder_first(input):
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
    # optional: save the decoded data
    # status = save(stem, parent, decoded_data)
    # if status != 0:
    #     print(f"Failed to save the decoded file as {stem}.bin. Continueing to verify...", flush=True)
    
    # re-encode the decoded data
    status, *rest = bencode(decoded_data)
    if status == 1:
        return 1, print(rest[-1])
    re_encoded_data = rest[0]
    # optional: save the re-encoded file
    # status = save(stem+'_re_encoded', parent, re_encoded_data)
    # if status != 0:
    #     print(f"Failed to save the re_encoded file as {stem+'_re_encoded'}.bin. Continueing to verify...", flush=True)


    # match and verify
    print("Input vs re-encoded data")
    print(source)
    print(re_encoded_data)
    if source == re_encoded_data:
        return 0, "Matched! Test Successful."
    else:
         return 1, "Mismatch! Human is dead!"


if __name__ == "__main__":
    try:
        status, *rest = test_decoder_first('c:/Projects/torrent/peer-2-peer-network/examples/exampleString.torrent')
        print(f"\n{rest[-1]}")
    except:
        print("Some exception occured")
