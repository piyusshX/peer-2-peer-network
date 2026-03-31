# message parsing based on protocol
# cheat sheet: 0 choked, 1 unchoked, 5 bitfield: peers inventory of pieces, 7 block data stream, 2 peer hi gareeb nikla lmao
import struct

def recv_exact(s, n): # we were getting choked mid transfer and not receiving full 16kb so now we will, surely
    data = b''
    while len(data) < n:
        chunk = s.recv(n - len(data))
        if not chunk:
            raise Exception("Connection closed")
        data += chunk
    return data

def check_peer_response(s):
    try:
        while True:
            try:
                length_bytes = s.recv(4)
            except TimeoutError:
                return 400, 0

            length = struct.unpack(">I", length_bytes)[0]

            if length == 0:
                print("keep-alive")
                continue
            else:
                msg = recv_exact(s, length)
                msg_id = msg[0]
                payload = msg[1:]

                print(f"Received msg: {msg_id}")
                if msg_id == 7:
                    return 7, payload
                elif msg_id == 5:
                    print("got bitfield")
                    peer_bitfield = payload
                    msg = struct.pack(">I", 1) + bytes([2])
                    s.send(msg)
                    print("Sent interested")
                elif msg_id == 0:
                    print("choked")
                elif msg_id == 1:
                    print("unchoked")
                    return 1, payload
                
    except Exception as e:
        print(e)
        return 0, 0

