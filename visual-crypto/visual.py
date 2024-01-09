import sys
import secrets
from PIL import Image


def main(argv):
    rng = secrets.SystemRandom()
    code_matrix_w = [
        [(0, 0, 0, 255), (255, 255, 255, 255)], [(255, 255, 255, 255), (0, 0, 0, 255)]
    ]
    code_matrix_b = [
        [[(255, 255, 255, 255), (0, 0, 0, 255)], [(0, 0, 0, 255), (255, 255, 255, 255)]],
        [[(0, 0, 0, 255), (255, 255, 255, 255)], [(255, 255, 255, 255), (0, 0, 0, 255)]]
    ]

    img = Image.open(argv[0])
    pixels = img.load()

    part1 = Image.new('RGBA', (img.width * 2, img.height), 'white')
    p1_pixels = part1.load()
    part2 = Image.new('RGBA', (img.width * 2, img.height), 'white')
    p2_pixels = part2.load()

    for y in range(img.height):
        for x in range(img.width):
            matrix = rng.randrange(0, 2)

            # Czarne piksele
            if pixels[x, y] == 0 or pixels[x, y] == (0, 0, 0) or pixels[x, y] == (0, 0, 0, 255):
                p1_pixels[x * 2, y] = code_matrix_b[matrix][0][0]
                p1_pixels[x * 2 + 1, y] = code_matrix_b[matrix][0][1]
                p2_pixels[x * 2, y] = code_matrix_b[matrix][1][0]
                p2_pixels[x * 2 + 1, y] = code_matrix_b[matrix][1][1]
            # Białe (lub inne) piksele
            else:
                p1_pixels[x * 2, y] = code_matrix_w[matrix][0]
                p1_pixels[x * 2 + 1, y] = code_matrix_w[matrix][1]
                p2_pixels[x * 2, y] = code_matrix_w[matrix][0]
                p2_pixels[x * 2 + 1, y] = code_matrix_w[matrix][1]

    part1.save('part1.png')
    part2.save('part2.png')


if __name__ == "__main__":
    main(sys.argv[1:])
