import math
import secrets
import sys


def main():
    rng = secrets.SystemRandom()
    m = 'Lorem ipsum dolor sit amet consectetur adipiscinge'
    p = 1
    q = 1

    # Generowanie p i q
    while not is_prime(p):
        p = rng.randrange(1009, 9974)

    while not is_prime(q):
        q = rng.randrange(1009, 9974)

    # Obliczanie n i phi
    n = p * q
    phi = (p - 1) * (q - 1)

    # Generowanie e
    e = 2
    while not is_prime(e) or math.gcd(phi, e) != 1:
        e = rng.randrange(3, phi)

    # Generowanie d
    d = pow(e, -1, phi)

    # Klucze
    public_key = [e, n]
    private_key = [d, n]

    print(f'Wiadomość:\n{m}\np = {p}\nq = {q}\nn = {n}\nphi = {phi}\ne = {e}\nd = {d}\n')

    # Szyfrowanie
    cryptext = encrypt(m, public_key)

    print(f'Wiadomość po szyfrowaniu:\n{cryptext}')

    # Deszyfrowanie
    decrypted = decrypt(cryptext, private_key)

    print(f'Wiadomość po odszyfrowaniu:\n{decrypted}')


def encrypt(m, key):
    ct = []
    for char in m:
        c = ord(char) ** key[0]
        c %= key[1]
        ct.append(c)

    return ct


def decrypt(c, key):
    msg = ''
    for char in c:
        m = char ** key[0]
        m %= key[1]
        msg += chr(m)

    return msg


# Sprawdzanie czy liczba jest pierwsza
def is_prime(n):
    if n == 1:
        return False
    if n == 3 or n == 5 or n == 7:
        return True
    if n % 2 == 0:
        return False
    for d in range(3, int(math.sqrt(n)) + 1, 2):
        if n % d == 0:
            return False
    return True


if __name__ == "__main__":
    main()
