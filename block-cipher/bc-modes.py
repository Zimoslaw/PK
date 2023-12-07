from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import time

files = ['plik1.wav', 'plik2.txt', 'plik3.tif'] # Pliki do szyfrowania

modes = [AES.MODE_ECB, AES.MODE_CBC, AES.MODE_OFB, AES.MODE_CFB, AES.MODE_CTR] # Tryby pracy szyfrów blokowych
mode_labels = {
    1: 'ECB',
    2: 'CBC',
    3: 'CFB',
    5: 'OFB',
    6: 'CTR'
}

for file in files:
    encrypt_times = {}  # Czasy szyfrowania
    decrypt_times = {}  # Czasy deszyfrowania

    for i in range(0, 10):
        content = open(file, 'rb')
        text = content.read()

        for mode in modes:
            key = get_random_bytes(16)  # Klucz szyfrowania

            cipher = AES.new(key, mode)

            # Odliczanie czasu
            start = time.time()

            # Szyfrowanie
            cryptext = cipher.encrypt(pad(text, AES.block_size))

            # Koniec odliczania
            stop = time.time()

            elapsed = stop - start
            if i == 0:
                encrypt_times[file + ',' + mode_labels[mode]] = elapsed
            else:
                encrypt_times[file + ',' + mode_labels[mode]] += elapsed

            if mode in (AES.MODE_CBC, AES.MODE_OFB, AES.MODE_CFB):
                iv = cipher.iv
                cipher = AES.new(key, mode, iv)
            elif mode == AES.MODE_CTR:
                nonce = cipher.nonce
                cipher = AES.new(key, mode, nonce=nonce)
            else:
                cipher = AES.new(key, mode)

            # Odliczanie czasu
            start = time.time()

            # Deszyfrowanie
            cipher.decrypt(cryptext)

            # Koniec odliczania
            stop = time.time()

            elapsed = stop - start
            if i == 0:
                decrypt_times[file + ',' + mode_labels[mode]] = elapsed
            else:
                decrypt_times[file + ',' + mode_labels[mode]] += elapsed
    print(file, ':')
    print(encrypt_times)
    print(decrypt_times)