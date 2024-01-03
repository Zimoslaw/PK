import os
import secrets
import math
from multiprocessing import Process, Pipe


def main():
    A_pipe, B_pipe = Pipe()
    A = Process(target=user, args=(A_pipe,))
    B = Process(target=user, args=(B_pipe,))

    A.start()
    B.start()

    A.join()
    B.join()


def user(pipe):
    rng = secrets.SystemRandom()
    n = 1

    # Generowanie n
    while not is_prime(n):
        n = rng.randrange(1009, 9974)

    # Wyznaczenie g
    g = prime_root(n)

    # Wysyłanie, porównywanie i uzgodnienie pary n i g
    pipe.send([n, g])
    n2, g2 = pipe.recv()

    if n2 > n:
        n = n2
        g = g2

    # Klucz prywatny
    x = rng.randrange(100000, 9999999)

    X = pow(g, x, n)

    # Wysyłanie X i odbieranie Y
    pipe.send(X)
    Y = pipe.recv()
    pipe.close()

    # Klucz
    key = pow(Y, x, n)

    print(f'Proces nr {os.getpid()}, Klucz: {key}\n')


# Znajdowanie najwyższego pierwiastka pierwotnego modulo
def prime_root(modulo):
    coprime_set = {num for num in range(1, modulo) if math.gcd(num, modulo) == 1}
    for g in range(modulo-1, 1, -1):
        if coprime_set == {pow(g, powers, modulo) for powers in range(1, modulo)}:
            return g


# Sprawdzanie czy liczba jest pierwsza
def is_prime(n):
    if n == 1:
        return False
    if n == 3 or n == 5 or n == 7:
        return True
    if n % 2 == 0:
        return False
    for d in range(3, int(pow(n, 0.5)) + 1, 2):
        if n % d == 0:
            return False
    return True


if __name__ == "__main__":
    main()
