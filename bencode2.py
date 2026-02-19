# Decoder for bencoded files

def decodeString(string, i=0):
    """
    Docstring for decodeString
    
    :param string: parent string from which string decoding is to be done
    :param i: index at which the digits denoting the length of string start 
    """
    # check if its a valid string format
    check = string[i].isdigit()
    if not check:
        return 1, i
    
    # calculate the length of string
    decodedStringLength = ""
    while(string[i].isdigit()):
        decodedStringLength+=string[i]
        i += 1
    if string[i] == ':': # check validity of format
        i += 1
    else:
        return 1, i
    decodedString = string[i:i+int(decodedStringLength)]
    updatedindex = i + int(decodedStringLength)

    return 0, decodedString, updatedindex

def decodeInt(string, i=0):
    """
    Docstring for decodeInt
    
    :param string: parent string from which integer decoding is to be done
    :param i: index at which the formatted integer starts
    :result format: status, decodedInteger, updatedIndex, erronousIndex
    """
    # check validity of format
    if string[i] != 'i':
        return 1, f"invalid format for int: missing 'i' at index {i}"
    i += 1
    num = ""

    # decipher the number
    if string[i] == '-':
        num += '-'
        i += 1
    while(string[i].isdigit()):
        num += string[i]
        i += 1

    # verify the fomatting
    if string[i] == 'e':
        updatedIndex = i+1
        return 0, num, updatedIndex
    else:
        erronousIndex = i+1
        return 1, f"missing end of int 'e' at {erronousIndex}"
    
def decodeList(string, i=0):
    """
    Docstring for decodeList
    
    :param string: parent string from which list is to be extracted
    :param i: index at which bencoded list begins
    """
    if string[i] != 'l':
        return 1, 'invalid list'
    i += 1
    list = []

    while string[i] != 'e':
        if string[i].isdigit() and int(string[i]) != 0:
            # the list element is a string
            status, *rest = decodeString(string, i)
            if status == 0:
                decodedString, updatedIndex = rest[0], rest[1]
                list.append(decodedString)
                i = updatedIndex
            else:
                return 1, 'invalid string format in list'
        else:
            match string[i]:
                case 'i':
                    # the list element is an integer
                    status, *rest = decodeInt(string, i)
                    if status == 0:
                        decodedInteger, updatedIndex = rest[0], rest[1]
                        list.append(decodedInteger)
                        i = updatedIndex
                    else:
                        return 1, 'invalid int format in list'
                case 'l':
                    # the list element is another list
                    status, *rest = decodeList(string, i)
                    if status == 0:
                        decodedList, updatedIndex = rest[0], rest[1]
                        list.append(decodedList)
                        i = updatedIndex
                    else:
                        return 1, 'invalid list format in list'
                case 'd':
                    # the list element is a dictionary
                    status, *rest = decodeDict(string, i)
                    if status == 0:
                        decodedDict, updatedIndex = rest[0], rest[1]
                        list.append(decodedDict)
                        i = updatedIndex
                    return 1, 'invalid dict format in list'
                case _:
                    # unexpected encounters
                    return 1, 'unexpected encounter in list'
    # encountering end of list 'e'
    updatedIndex = i + 1
    return 0, list, updatedIndex

def decodeDict(string, i=0):
    """
    Docstring for decodeDict
    
    :param string: parent string from which dict is to be decoded
    :param i: index at which dict starts
    """
    if string[i] != 'd':
        return 1, "invalid dictionary"
    
    dict = {}
    key = value = None
    i += 1

    # find all key value pairs in dict
    while string[i] != 'e':

        # finding the key
        status, *rest = decodeString(string, i)
        if status == 0:
            key, index = rest[0], rest[1]
        else:
            return 1, f'invalid key at index {i}'
        
        # finding the corresponding value
        i = index
        status, *rest = main(string, i)
        if status == 2: # here status 0 would indicate absence of trailing 'e' which denotes the end of dict, making the input invalid
            output, updatedIndex = rest[0], rest[1]
            value, i = output, updatedIndex
        elif status == 0:
            return 1, f'incomplete input: missing end of dict at index {i}'
        else:
            return 1, f'invalid value at index {i}'
        # adding the key value entry to the dictionary
        dict[key] = value
    
    # encountering end of dict 'e'
    updatedIndex = i + 1
    return 0, dict, updatedIndex

def main(string, i=0):
    """
    function for decoding the bencoded input in python string format'
    
    :param string: bencoded input to be decoded
    """
    if string:
        # check input type
        if string[i].isdigit():
            status, *rest = decodeString(string, i)
        else: 
            match string[i]:
                case 'i':
                    status, *rest = decodeInt(string, i)
                
                case 'l':
                    status, *rest = decodeList(string, i)
                
                case 'd':
                    status, *rest = decodeDict(string, i)

                case _:
                    return 1, "invalid input"

        if status == 0: # here 0 indicates success in decoding
            output, updatedIndex = rest[0], rest[1]
            # check for trailing characters
            if updatedIndex == len(string):
                return 0, output
            else:
                return 2, output, updatedIndex, "trailing garbage"
        else:
            return 1, f"error decoding string: {rest[-1]}"





if __name__=="__main__":
    string1 = "d5:helloi69e6:myListli70ei71ee6:mydictd5:firsti72e6:second2:hiee"
    string2 = "l2:hi3:supi69ee"
    status, *rest = main(string1)
    if status == 0:
        print(f'success!\n{rest[0]}')
    else:
        print(f'failure!\n{rest[-1]}')

    
    print(f"\nexecution complete!")