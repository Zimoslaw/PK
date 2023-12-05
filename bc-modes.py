from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import time

files = ['sample0.txt'] # Pliki do szyfrowania

modes = [AES.MODE_ECB, AES.MODE_CBC, AES.MODE_OFB, AES.MODE_CFB, AES.MODE_CTR] # Tryby pracy szyfrów blokowych

key = get_random_bytes(16) # Klucz szyfrowania

encrypt_times = {} # Czasy szyfrowania
decrypt_times = {} # Czasy deszyfrowania

for file in files:

    content = open(file, 'r')
    text = content.read()
    
    for mode in modes:

        cipher = AES.new(key, mode)

        # Odliczanie czasu
        start = time.time()

        # Szyfrowanie
        cryptext = cipher.encrypt(pad(text.encode("UTF-8"), AES.block_size))

        # Koniec odliczania
        stop = time.time()

        elapsed = stop - start
        encrypt_times[file+str(mode)] = elapsed

        #print(f'Encrypting file {file} in mode {mode}, time: {encrypt_times[file+str(mode)]}')

        cipher = AES.new(key, mode)

        # Odliczanie czasu
        start = time.time()

        # Szyfrowanie
        cipher.decrypt(cryptext)

        # Koniec odliczania
        stop = time.time()

        elapsed = stop - start
        decrypt_times[file+str(mode)] = elapsed

        #print(f'Decrypting file {file} in mode {mode}, time: {decrypt_times[file+str(mode)]}')
        print(f'{file}: {mode}: {encrypt_times[file+str(mode)]}, {decrypt_times[file+str(mode)]}')