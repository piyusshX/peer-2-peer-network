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
    # print(f'\nconnected to {peer}')
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
    response = s.recv(68)
    # print(f"Handshake successful!") # peer found
    recv_pstrlen = response[0]
    recv_pstr = response[1:20]
    recv_reserved = response[20:28]
    recv_info_hash = response[28:48]
    recv_peer_id = response[48:68]
    if pstr != recv_pstr:
        raise Exception("Not bittorrent peer")
    if recv_info_hash != info_hash:
        raise Exception(f"info hash mismatch \n{recv_info_hash} \n{info_hash}")
    # print(f"connected to swarm \npeer: {recv_peer_id}") # communication started

    # try to get unchoked from peer
    unchoked = False

    while True:
        length = struct.unpack(">I", recv_exact(s, 4))[0]

        if length == 0:
            continue

        msg = recv_exact(s, length)
        msg_id = msg[0]

        if msg_id == 5:
            # print(f"\nBITFIELD")
            bitfield = msg[1:]
        elif msg_id == 1:
            # print(f"\nUNCHOKED")
            unchoked = True
            break
        elif msg_id == 7:
            print("you got 7 for some reason here")

    if not unchoked:
        print(f"Failed to connect \nchecking next peer")
        raise Exception("Failed to connect")
    else:
        return s, bitfield # now we are unchoked and we can talk to peer


