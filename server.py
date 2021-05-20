import random, time
import socket, rsa
from time import sleep
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from hybrid_rsa_aes import HybridCipher

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))
#(public_key, privat_key) = rsa.newkeys(2048)
"""
rsa_private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048, backend=default_backend()
)
rsa_public_key = rsa_private_key.public_key()
a = rsa_public_key.public_numbers().public_key(default_backend())
print(a.public_numbers())
print('hello')
"""
address = None
while address == None:
    rand = random.randint(0, 10)
    message, address = server_socket.recvfrom(1024)
    message = message.upper()
    server_socket.sendto(message, address)
    print(address)
"""
print('sending key')
#server_socket.sendto(str(public_key.n).encode(), address)
server_socket.sendto(str(rsa_public_key.public_numbers()).encode(), address)
print(rsa_public_key)
i=0
"""
while True:
    #data = rsa.decrypt(server_socket.recv(1316), privat_key)
    res = server_socket.recv(1316)
    #print(res)
    print(time.time()*1000)
    print(len(res))
    #print(data)
    #rec_data = base64.b64decode(data)
    #print(type(rec_data))
    #data = data.decode("ascii")
    #encrypt_message = HybridCipher().encrypt(rsa_public_key=a, data=str(data))
    #res = HybridCipher().decrypt(rsa_private_key=rsa_private_key, cipher_text=encrypt_message)
    """
    if res:
        #print(data)
        i += 1
        print("\n ", i)
        res = None
    """