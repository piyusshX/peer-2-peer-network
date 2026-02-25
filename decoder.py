def handle_int(str): # 1100e -> 1234 
    i = 0 
    while(str[i] != 'e'):
        i = i + 1
    return int(str[0:i]), (i+2) # i+2 -> bcz i denotes no of int and 2 for i and e

def handle_str(length, str): # (4, temp....)
    return str[0:length]

def handle_list(str): # l 4:spam i42e e
    temp = []
    skip_count = 0
    while(str[0] != 'e'):
        val, skip = type_checker(str) # spam 6 | 42 4
        temp.append(val)
        str = str[skip:]
        skip_count = skip_count + skip
    return temp, (skip_count + 2) # same logic as int for skip_count + 2


def handle_dict(str):
    temp = []
    skip_count = 0
    while(str[0] != 'e'):
        val, skip = type_checker(str)
        temp.append(val)
        str = str[skip:]
        skip_count = skip_count + skip
    length = len(temp)
    i = 0
    new_dict = {}
    while(length != 0):
        new_dict[temp[i]] = temp[i+1]
        length = length - 2
        i = i + 2
    return new_dict, (skip_count + 2)


def type_checker(str):
    match str[0]:
        case 'i':
            return handle_int(str[1:])
        case 'l':
            return handle_list(str[1:])
        case 'd':
            return handle_dict(str[1:])
        case _:
            i = 0
            while(str[i] != ':'): 
                i = i + 1
            length = int(str[0:i])
            return handle_str(length, str[i+1:]), (i + length + 1) # String , Skip_Length
        

def main(encoded_string): 
    decoded_dict = type_checker(encoded_string) # Tuple of 2 elements is returned (dict, skip_length)
    print(decoded_dict[0]) 
    # return decoded_dict[0]

mydict = "d8:greeting5:hello5:counti42e5:itemsl5:apple6:bananae6:nestedd5:itemsl5:apple6:bananae6:numberi99eee"
main(mydict)
