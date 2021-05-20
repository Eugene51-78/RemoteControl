import socket,  random, time
import AESCipher
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))

key = get_random_bytes(16) # Генерируем ключ шифрования
print(str(key))
print(type(str(key)))
aes = AESCipher.AESCipher(str(key))
address = None

while address == None:
    rand = random.randint(0, 10)
    message, address = server_socket.recvfrom(1024)
    message = message.upper()
    server_socket.sendto(message, address)
    print(address)

public_key = None
while public_key == None:
    public_key = server_socket.recv(1024)
    print(public_key)
public_key = RSA.importKey(public_key)
# Осталось закодировать AES и отправить
cipher = PKCS1_OAEP.new(public_key)
encrypted_AES_key = cipher.encrypt(key)
print(encrypted_AES_key)
server_socket.sendto(encrypted_AES_key, address)
#server_socket.sendto(str(key).encode(), address)

while True:
    #data = rsa.decrypt(server_socket.recv(1316), privat_key)
    res = server_socket.recv(8192)
    #print(res)
    print(len(res))
    print("до :", time.time() * 1000)
    dec = aes.decrypt(enc=res)
    print("после: ", time.time() * 1000)