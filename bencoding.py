def encode_string(bytes):
    return str(len(bytes)).encode() + b":" + bytes

def encode_int(num):
    return b"i" + str(num).encode() + b"e"

def encode_list(lst):
    temp = b""
    for item in lst:
        temp_str = type_checker(item)
        temp = temp + temp_str

    return b"l" + temp + b"e"

def encode_dict(my_dict):
    temp = b""
    sorted_key_list = sorted(my_dict)
    for key in sorted_key_list:
        temp_str = encode_string(key)
        temp = temp + temp_str
        val = my_dict[key]
        temp_str = type_checker(val)
        temp = temp + temp_str

    return b"d" + temp + b"e"

def type_checker(val):
    match val:
            case bytes():
                return encode_string(val)
            case int():
                return encode_int(val)
            case list():
                return encode_list(val)
            case dict():
                return encode_dict(val)
            case _:
                print("Unknown Data Type")
                return

def main(torrDict): 
    # print(encode_dict(torrDict))
    try:
        return 0, encode_dict(torrDict)
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()  # Shows full stack trace
        return 1, f"encoding failed: {e}"
    
# For Testing 
    
torrent_dict = {b'hello': 69, b'myList': [[70, 71],[72, 73]], b'mydict': {b'first': 72, b'second': 2}}


# main(torrent_dict)

if __name__ == "__main__":
    print(main(torrent_dict)[1])