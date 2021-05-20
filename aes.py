from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import string, random

from hybrid_rsa_aes import HybridCipher

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    #print("Random string of length", length, "is:", rand_string)
    return rand_string

rsa_private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048, backend=default_backend()
)
rsa_public_key = rsa_private_key.public_key()
a = rsa_public_key.public_numbers().public_key(default_backend())
data = generate_random_string(1000)
encrypt_message = HybridCipher().encrypt(rsa_public_key=a, data=data)
print("encrypt_message is ", encrypt_message)

decrypt_message = HybridCipher().decrypt(rsa_private_key=rsa_private_key, cipher_text=encrypt_message)
# мне надо передать приватный ключ на Orange Pi
print(decrypt_message)