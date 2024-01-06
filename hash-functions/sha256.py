import hashlib
import sys
import itertools
import string
from bitarray import bitarray


def main():
    alphabet = string.ascii_lowercase + string.ascii_uppercase

    hashes_12bit = []
    collided_words = {}
    change_probabilities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
    changes = 0

    for length in range(1, 4):
        combinations = itertools.product(alphabet, repeat=length)

        prev = 'a'

        for word in combinations:
            h = get_sha256(''.join(word))

            # Sprawdzanie kolizji pierwszych 12 bitów
            b = bitarray()
            b.frombytes(b''.fromhex(h))
            b = b[:12]

            if b not in hashes_12bit:
                hashes_12bit.append(b)
            else:
                collided_words[word] = 1

            # Sprawdzanie kryterium SAC
            if is_one_bit_changed(prev, ''.join(word)):
                prev_hash = get_sha256(prev)

                c_bits = changed_bits(prev_hash, h)
                for i in range(len(change_probabilities)):
                    change_probabilities[i] += c_bits[i]

                changes += 1

            prev = ''.join(word)

    if len(collided_words.keys()) > 0:
        print(f'Funkcja skrotu SHA256: znaleziono {len(collided_words.keys())} kolizji na pierwszych 12 bitach.')
    else:
        print(f'Funkcja skrotu SHA256: nie znaleziono kolizji na pierwszych 12 bitach.')

    for i in range(len(change_probabilities)):
        change_probabilities[i] = round(change_probabilities[i] / changes, 3)
    print(f'Prawdopodobienstwo zmiany kazdego bitu w skrocie, przy zmianie pojedynczego bitu na wejsciu:\n{change_probabilities}')


def get_sha256(s):
    h = hashlib.new('sha256')
    h.update(s.encode("UTF-8"))
    return h.hexdigest()


# Sprawdzanie czy zmieniony został tylko 1 bit
def is_one_bit_changed(a, b):
    abits = bitarray()
    bbits = bitarray()
    abits.frombytes(a.encode('utf-8'))
    bbits.frombytes(b.encode('utf-8'))

    bits_changed = 0

    for i in range(len(abits)):
        if abits[i] != bbits[i]:
            bits_changed += 1
            if bits_changed > 1:
                return False

    if bits_changed == 0:
        return False
    else:
        return True


# Zwraca tablicę zmienionych bitów (0 = bit niezmieniony, 1 = bit zmieniony)
def changed_bits(a, b):
    abits = bitarray()
    bbits = bitarray()
    abits.frombytes(b''.fromhex(a))
    bbits.frombytes(b''.fromhex(b))

    bits_changed = []

    for i in range(len(abits)):
        if abits[i] != bbits[i]:
            bits_changed.append(1)
        else:
            bits_changed.append(0)

    return bits_changed


if __name__ == "__main__":
    main(sys.argv[1:])
