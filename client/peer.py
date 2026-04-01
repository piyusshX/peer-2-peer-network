# This file cotacts peers to do the handshake probably
import socket, struct
from protocol import check_peer_response, recv_exact

global bitfield

def contact_peer(my_peer_id, peer, info_hash):
    ip, port = peer.split(":")
    port = int(port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5)

    s.connect((ip, port))

    pstrlen = b'\x13'
    pstr = b'BitTorrent protocol'
    reserved = b'\x00' * 8

    handshake = (
        pstrlen +
        pstr +
        reserved +
        info_hash +
        my_peer_id
    )

    s.send(handshake)

    # ensure full handshake read
    response = recv_exact(s, 68)

    recv_pstr = response[1:20]
    recv_info_hash = response[28:48]

    if recv_pstr != pstr:
        raise Exception("Not bittorrent peer")

    if recv_info_hash != info_hash:
        raise Exception("info hash mismatch")

    # send INTERESTED immediately
    s.send(struct.pack(">I", 1) + bytes([2]))

    bitfield = None
    unchoked = False

    # bounded loop (prevents hanging)
    for _ in range(10):
        try:
            length = struct.unpack(">I", recv_exact(s, 4))[0]
        except:
            break

        if length == 0:
            continue

        msg = recv_exact(s, length)
        msg_id = msg[0]

        if msg_id == 5:
            bitfield = msg[1:]

        elif msg_id == 1:
            unchoked = True
            break

        elif msg_id == 0:
            # choked
            continue

    if not unchoked:
        s.close()
        raise Exception("Failed to unchoke")

    return s, bitfield