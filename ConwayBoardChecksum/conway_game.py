import numpy as np
import pygame
import base64
import lzma


def text_to_binary(text):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string


def create_grid(binary_string):
    binary_list = [int(bit) for bit in binary_string]
    size = int(np.ceil(np.sqrt(len(binary_list))))
    padded_list = binary_list + [0] * (size**2 - len(binary_list))
    grid = np.array(padded_list).reshape(size, size)
    return grid


def draw_grid(surface, grid, cell_size, grid_color):
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            color = (255, 255, 255) if grid[row, col] == 1 else (0, 0, 0)
            pygame.draw.rect(surface, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    for i in range(rows + 1):
        pygame.draw.line(surface, grid_color, (0, i * cell_size), (cols * cell_size, i * cell_size))
    for j in range(cols + 1):
        pygame.draw.line(surface, grid_color, (j * cell_size, 0), (j * cell_size, rows * cell_size))


def update(grid):
    new_grid = grid.copy()
    size = len(grid)
    for i in range(size):
        for j in range(size):
            neighbors_sum = (
                grid[i, (j-1) % size] + grid[i, (j+1) % size] +
                grid[(i-1) % size, j] + grid[(i+1) % size, j] +
                grid[(i-1) % size, (j-1) % size] + grid[(i-1) % size, (j+1) % size] +
                grid[(i+1) % size, (j-1) % size] + grid[(i+1) % size, (j+1) % size]
            )
            if grid[i, j] == 1 and (neighbors_sum < 2 or neighbors_sum > 3):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and neighbors_sum == 3:
                new_grid[i, j] = 1
    return new_grid


def compress_and_encode_lzma(binary_string):
    binary_bytes = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')
    compressed_data = lzma.compress(binary_bytes)
    base64_encoded = base64.b64encode(compressed_data)
    return base64_encoded.decode('utf-8')


def custom_hash(input_data):
    a = 0x01234567
    b = 0x89abcdef
    c = 0xfedcba98
    d = 0x76543210

    if isinstance(input_data, str):
        input_data = input_data.encode('utf-8')

    for i in range(0, len(input_data), 4):
        block = input_data[i:i+4]
        print(block)
        print("a before: " + hex(a))
        print("a moved by 5 to left: " + hex(a << 5))
        print("a moved by 2 to right: " + hex(a >> 2))
        print(int.from_bytes(block, 'big'))
        print(hex((a << 5) + int.from_bytes(block, 'big') + (a >> 2)))
        a ^= (a << 5) + int.from_bytes(block, 'big') + (a >> 2)
        print("a: " + hex(a))
        b ^= (b << 7) + int.from_bytes(block, 'big') - (b >> 3)
        print("b: " + hex(b))
        c ^= (c << 11) + int.from_bytes(block, 'big') * (c >> 5)
        print("c: " + hex(c))
        d ^= (d << 13) + int.from_bytes(block, 'big') // (d >> 7)
        print("d: " + hex(c))

    hash_value = (a << 96) | (b << 64) | (c << 32) | d
    mask = (1 << 256) - 1
    print("hash value: " + hex(hash_value))
    truncated_hash = ((hash_value & mask) + ((hash_value >> 128) & mask)) & mask
    hex_str = format(truncated_hash, '064x')
    mixed_case_hash = ''.join([c.upper() if i % 2 == 0 else c for i, c in enumerate(hex_str)])
    return mixed_case_hash


def save_hash_to_file(hash_value, filename):
    with open(filename, 'w') as file:
        file.write(hash_value)


def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def save_image(surface, filename):
    pygame.image.save(surface, filename)
