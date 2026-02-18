def encode_string(str):
    return f"{len(str)}:{str}"

def encode_int(num):
    return f"i{num}e"

def encode_list(lst):
    temp = ""
    for item in lst:
        temp_str = type_checker(item)
        temp = temp + temp_str

    return f"l{temp}e"

def encode_dict(my_dict):
    temp = ""
    for key in my_dict:
        temp_str = encode_string(key)
        temp = temp + temp_str
        val = my_dict[key]
        temp_str = type_checker(val)
        temp = temp + temp_str

    return f"d{temp}e"

def type_checker(val):
    match val:
            case str():
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
    return encode_dict(torrDict)
    

# torrent_dict = {
#     "announce": "http://tracker.example.com:8080/announce",
#     "creation date": 1700000000,
#     "created by": "MiniTorrent 1.0",
#     "info": {
#         "length": 12345,
#         "name": "example.txt",
#         "piece length": 262144,
#         "pieces": "aaaaaaaaaaaaaaaaaaaa"
#     }
# }


# main(torrent_dict)