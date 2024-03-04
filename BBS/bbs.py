from bitarray import bitarray
import secrets
import math
import sys


def main(argv):
    rng = secrets.SystemRandom()

    # Generowanie p i q
    p = 0
    while not is_prime(p) or p % 4 != 3:
        p = rng.randrange(10007, 99997)
    q = 0
    while not is_prime(q) or q % 4 != 3:
        q = rng.randrange(10007, 99997)

    # Obliczanie N
    N = p * q

    # Generowanie ciągu bitów
    random_string = bitarray()

    # Wartość pierwotna generatora
    x = N
    while not is_prime(x) or math.gcd(N, x) != 1:
        x = rng.randrange(3, N)

    x = pow(x, 2) % N

    # Wartości kolejnych bitów
    for i in range(int(argv[0])):
        x = pow(x, 2) % N
        random_string.append(x & 1)

    print(random_string.tobytes().hex())

    testFips(random_string)


# Testy statystyczne FIPS140-2
def testFips(s):
    single_bits_range = [9725, 10275]
    single_bits = [0, 0]
    series_ranges = [[2315, 2685], [1114, 1386], [527, 723], [240, 384], [103, 209], [103, 209]]
    series_0 = {}
    series_1 = {}
    long_serie = False
    poker_range = [2.16, 46.17]
    poker_values = {}

    if s[0] == 0:
        last = 1
    else:
        last = 0
    serie = 0
    for b in s:
        # Pojedyncze bity
        if b == 0:
            single_bits[0] += 1
        else:
            single_bits[1] += 1

        # Serie
        if b != last:
            if last == 0:
                if serie not in series_0.keys():
                    series_0[serie] = 1
                else:
                    series_0[serie] += 1
            else:
                if serie not in series_1.keys():
                    series_1[serie] = 1
                else:
                    series_1[serie] += 1

            serie = 1
        else:
            serie += 1
            if serie >= 26:
                long_serie = True
        last = b

    # Pokerowy
    s = s.tobytes().hex()
    for h in s:
        if ord(h) not in poker_values.keys():
            poker_values[ord(h)] = 1
        else:
            poker_values[ord(h)] += 1

    X = 0
    for key in poker_values.keys():
        X += pow(poker_values[key], 2)

    X = X * (16 / 5000) - 5000

    # Sprawdzanie wyników
    if single_bits_range[0] <= single_bits[0] <= single_bits_range[1] and single_bits_range[0] <= single_bits[1] <= single_bits_range[1]:
        print(f'Test pojedynczych bitów: OK (0: {single_bits[0]}, 1: {single_bits[1]})')
    else:
        print(f'Test pojedynczych bitów: NOK (0: {single_bits[0]}, 1: {single_bits[1]})')

    for i in range(1, 7):
        if series_ranges[i-1][0] <= series_0[i] <= series_ranges[i-1][1] and series_ranges[i-1][0] <= series_1[i] <= series_ranges[i-1][1]:
            print(f'Test serii {i}: OK (0: {series_0[i]}, 1: {series_1[i]})')
        else:
            print(f'Test serii {i}: NOK (0: {series_0[i]}, 1: {series_1[i]})')

    if not long_serie:
        print(f'Test długiej serii: OK')
    else:
        print(f'Test długiej serii: NOK')

    if poker_range[0] < X < poker_range[1]:
        print(f'Test pokerowy: OK (X={X})')
    else:
        print(f'Test pokerowy: NOK (X={X})')


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
    main(sys.argv[1:])
