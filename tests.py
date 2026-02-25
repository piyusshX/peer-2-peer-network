from b_decoder import main as decode, load, save
from bencoding import main as bencode
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
    print("Results of test 1: Input vs re-encoded data")
    if show_in_terminal: # print in terminal
        print(source)
        print(re_encoded_data)
    if source == re_encoded_data:
        print("Matched! Test Successful.")
    else:
        print("Mismatch! Human is dead!")
    
    # re-decode the re_encoded_data
    status, *rest = decode(re_encoded_data)
    if status != 0:
        return 1, f"Error while re_decoding: \n {rest[-1]}"
    re_decoded_data = rest[0]
    # optional: save the re_decoded data
    # status = save(stem+'_re_decoded', parent, re_decoded_data)
    # if status != 0:
    #     print(f"Failed to save the re_decoded file as {stem+'_re_decoded'}.bin. Continueing to verify...", flush=True)
    
    print("Results of test 2: decoded input vs re-decoded input")
    if show_in_terminal: # print in terminal
        print(decoded_data)
        print(re_decoded_data)
    if decoded_data == re_decoded_data:
        print("Matched! Test Successful.")
    else:
        print("Mismatch! Human is dead!")

    return 0, f"tests completed!"

# def test_encoder_first(input):
#     # load a dict from a .bin file
#     status, *rest = load(input)
#     if status == 0:
#         stem, parent, source = rest[0], rest[1], rest[2]
#     else:
#         return 1, f"Error while loading: \n {rest[-1]}"
    
#     # b-encode the dict
#     status, *rest = bencode(source)
#     if status == 1:
#         return 1, print(rest[-1])
#     b_encoded_data = rest[0]
#     # optional: save the b-encoded file
#     # status = save(stem+'_re_encoded', parent, re_encoded_data)
#     # if status != 0:
#     #     print(f"Failed to save the b_encoded file as {stem+'_re_encoded'}.bin. Continueing to verify...", flush=True)


#     # re-decode the b-encoded data
#     status, *rest = decode(b_encoded_data)
#     if status != 0:
#         return 1, f"Error while decoding: \n {rest[-1]}"
#     re_decoded_data = rest[0]
#     # optional: save the decoded data
#     # status = save(stem, parent, decoded_data)
#     # if status != 0:
#     #     print(f"Failed to save the decoded file as {stem}.bin. Continueing to verify...", flush=True)
    

#     # match and verify
#     print("Input vs re-decoded data")
#     print(source)
#     print(re_decoded_data)
#     if source == re_decoded_data:
#         return 0, "Matched! Test Successful."
#     else:
#          return 1, "Mismatch! Human is dead!"


if __name__ == "__main__":
    try:
        show_in_terminal = True # Recommended False for bigger files, else the terminal will be cluttered
        status, *rest = test_decoder_first('c:/Projects/torrent/peer-2-peer-network/examples/exampleString.torrent', show_in_terminal)
        print(f"{rest[-1]}")

        # status, *rest = test_encoder_first("c:/Projects/torrent/peer-2-peer-network/examples/exampleString.bin")
        # print(f"test 2 results:\n{rest[-1]}")
    except:
        print("Some exception occured")
