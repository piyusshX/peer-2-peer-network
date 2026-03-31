# This file cotacts peers to do the handshake probably
import socket
from protocol import check_peer_response

def contact_peer(my_peer_id, peer_list, info_hash):
    for peer in peer_list:
        ip, port = peer.split(":")
        port = int(port)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        try: # try to connect to peer
            s.connect((ip, port))
            print(f'connected to {peer}')
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
            print(f"Handshake successful!") # peer found
            recv_pstrlen = response[0]
            recv_pstr = response[1:20]
            recv_reserved = response[20:28]
            recv_info_hash = response[28:48]
            recv_peer_id = response[48:68]
            if pstr != recv_pstr:
                raise Exception("Not bittorrent peer")
            if recv_info_hash != info_hash:
                raise Exception(f"info hash mismatch \n{recv_info_hash} \n{info_hash}")
            print(f"connected to swarm \npeer: {recv_peer_id}") # communication started

            # try to get unchoked from peer
            peer_resp, payload = check_peer_response(s)

            got_unchoked = peer_resp

            if not got_unchoked:
                print("Still choked")
                print(f"checking next peer \n\n")
                continue
            else:
                break  # we got the first peer that unchoked us
        except Exception as e:
            print("Failed:", e)
            s.close()

    return s # now we are unchoked and we can talk to peer
