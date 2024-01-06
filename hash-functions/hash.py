import hashlib
import time
import sys


def main(argv):
    if len(argv) != 1:
        print('Nieprawidlowa liczba argumentow')
        exit()

    s = argv[0]

    functions = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']

    for f in functions:

        start = time.perf_counter_ns()

        h = get_hash(s, f)

        stop = time.perf_counter_ns()
        elapsed = stop - start

        print(f'{f},\t\twejscie: {len(s)}B, \t\t({elapsed}ns): {h}')


def get_hash(s, f):
    h = hashlib.new(f)
    h.update(s.encode("UTF-8"))
    return h.hexdigest()


if __name__ == "__main__":
    main(sys.argv[1:])
