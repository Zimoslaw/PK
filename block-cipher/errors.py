from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

text = 'Lorem ipsum dolor sit amet'

modes = [AES.MODE_ECB, AES.MODE_CBC, AES.MODE_OFB, AES.MODE_CFB, AES.MODE_CTR] # Tryby pracy szyfrów blokowych
mode_labels = {
    1: 'ECB',
    2: 'CBC',
    3: 'CFB',
    5: 'OFB',
    6: 'CTR'
}

print(f'Wiadomość oryginalna:\n{text}')

for mode in modes:
    key = get_random_bytes(16)  # Klucz szyfrowania

    cipher = AES.new(key, mode)

    # Szyfrowanie
    cryptext = cipher.encrypt(pad(text.encode("UTF-8"), AES.block_size))

    # Wyzeruj 8 bajt
    ct = bytearray(cryptext)
    ct[8] = 0

    if mode in (AES.MODE_CBC, AES.MODE_OFB, AES.MODE_CFB):
        iv = cipher.iv
        cipher = AES.new(key, mode, iv)
    elif mode == AES.MODE_CTR:
        nonce = cipher.nonce
        cipher = AES.new(key, mode, nonce=nonce)
    else:
        cipher = AES.new(key, mode)

    # Deszyfrowanie
    decrypted = unpad(cipher.decrypt(ct), AES.block_size)

    print(f'{mode_labels[mode]}:\n{decrypted}')