from time import sleep
import socket, rsa
(public_key, privat_key) = rsa.newkeys(512)
sock_lc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock_streamer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_streamer.bind(('0.0.0.0', 5660))

server_address = '0.0.0.0'
server_port = 31337

server = (server_address, server_port)
sock.bind(server)
sock.listen(1)

streamer = None
while True:
    print('wait connection')
    conn, addr = sock.accept()
    print("conn is ", conn)
    print('socket accepted!')
    data, streamer = sock_streamer.recvfrom(1024)
    print("Streamer is ", streamer)
    if streamer:
        break

sock_streamer.sendto(data, streamer)
sock_streamer.close()

server_lc = ('127.0.0.1', 5646)
sock_lc.sendto(str(public_key.n).encode(), ('127.0.0.1', 5647))
print(public_key)
sock_lc.close()
sock_lc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_lc.bind(server_lc)
while True:
    data = rsa.decrypt(sock_lc.recv(1024), privat_key)
    print(data.decode())
    sleep(0.0005)