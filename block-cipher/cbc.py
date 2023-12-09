from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
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

    fd = open(file, "rb")
    content = fd.read()
    encrypted = cbc_encrypt(content, key, iv)
    fd.close()

    print(f'Szyfrowanie zakończone!')
    #print(encrypted)

    print(f'Odszyfrowywanie...')

    decrypted = cbc_decrypt(encrypted, key, iv)
    fd = open('new_' + file, '+bx')
    fd.write(decrypted)
    fd.close()

    print(f'Odszyfrowanie zakończone!')
    #print(decrypted.decode('UTF-8'))


def cbc_encrypt(file, key, iv):
    content = bytearray(file)
    content = pad(content, AES.block_size)
    encrypted_content = []

    # Podziel zawartość na bloki 16 bajtowe
    plain_blocks = numpy.array_split(content, math.ceil(len(content) / AES.block_size))

    # Zaszyfruj pierwszy blok
    block_ct = cbc_encrypt_block(plain_blocks[0], iv, key)
    encrypted_content.append(block_ct)

    # Zaszyfruj resztę bloków
    for block in plain_blocks[1:]:
        block_ct = cbc_encrypt_block(block, block_ct, key)
        encrypted_content.append(block_ct)

    return b''.join(encrypted_content)


def cbc_encrypt_block(block, top_register, key):
    # Obiekt szyfrowania ECB
    cipher = AES.new(key, AES.MODE_ECB)

    # XOR IV z pierwszym blokiem
    xored = int.from_bytes(top_register, sys.byteorder) ^ int.from_bytes(block, sys.byteorder)

    # Szyfrowanie wyniku XOR
    return cipher.encrypt(xored.to_bytes(len(top_register), sys.byteorder))


def cbc_decrypt(file, key, iv):
    content = bytearray(file)
    decrypted_content = []

    # Podziel zawartość na bloki 16 bajtowe
    crypt_blocks = numpy.array_split(content, math.ceil(len(content) / 16))

    # Odszyfruj pierwszy blok
    block_ct = cbc_decrypt_block(crypt_blocks[0], iv, key)
    decrypted_content.append(block_ct)

    # Odszyfruj resztę bloków
    for i in range(1, len(crypt_blocks)):
        block_ct = cbc_decrypt_block(crypt_blocks[i], b''.join(crypt_blocks[i - 1]), key)
        decrypted_content.append(block_ct)

    return unpad(b''.join(decrypted_content), AES.block_size)


def cbc_decrypt_block(block, top_register, key):
    cipher = AES.new(key, AES.MODE_ECB)

    decrypted = cipher.decrypt(b''.join(block))

    xored = int.from_bytes(top_register, sys.byteorder) ^ int.from_bytes(decrypted, sys.byteorder)

    return xored.to_bytes(len(top_register), sys.byteorder)


if __name__ == "__main__":
    main(sys.argv[1:])
