from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode
import sys
import math
import numpy

def main(argv):
    file = argv[0]
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    print(f'Szyfrowanie "{file}"...')
    print(f"Klucz: {b64encode(key).decode('UTF-8')}")
    print(f"IV: {b64encode(iv).decode('UTF-8')}")
    encrypted = cbc_encrypt(file, key, iv)
    print(encrypted)


def cbc_encrypt(file, key, iv):
    content = bytearray(file.encode('UTF-8'))
    encrypted_content = []

    # Podziel zawartość na bloki 16 bajtowe
    plain_blocks = numpy.array_split(content, math.ceil(len(content)/16))

    # Zaszyfruj pierwszy blok
    block_ct = cbc_encrypt_block(plain_blocks[0], iv, key)
    encrypted_content.append(block_ct)

    # Zaszyfruj resztę bloków
    for block in plain_blocks[1:]:
        block_ct = cbc_encrypt_block(block, block_ct, key)
        encrypted_content.append(block_ct)

    return b''.join(encrypted_content)

def cbc_encrypt_block(block, top_buffer, key):

    # Obiekt szyfrowania ECB
    cipher = AES.new(key, AES.MODE_ECB)

    # XOR IV z pierwszym blokiem
    xored = int.from_bytes(top_buffer, sys.byteorder) ^ int.from_bytes(block, sys.byteorder)

    # Szyfrowanie wyniku XOR
    return cipher.encrypt(xored.to_bytes(len(top_buffer), sys.byteorder))

if __name__ == "__main__":
    main(sys.argv[1:])