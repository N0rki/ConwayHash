import numpy as np
import pygame
import sys
import base64
import lzma
import time
import os


def text_to_binary(text):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string


def compress_and_encode_lzma(binary_string):
    # Convert binary string to bytes
    binary_bytes = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')

    # Compress the binary data using lzma
    compressed_data = lzma.compress(binary_bytes)

    # Encode the compressed data in base64
    base64_encoded = base64.b64encode(compressed_data)

    return base64_encoded.decode('utf-8')


def create_grid(binary_string):
    binary_list = [int(bit) for bit in binary_string]
    size = int(np.ceil(np.sqrt(len(binary_list))))
    padded_list = binary_list + [0] * (size**2 - len(binary_list))
    grid = np.array(padded_list).reshape(size, size)

    return grid


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


def save_representation_to_file(representation, binary_string, filename):
    with open(filename, 'a') as file:
        file.write(f"Representation: {representation}\n")
        file.write(f"Binary Representation: {binary_string}\n\n")


def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def custom_hash(input_data):
    # Initialize state variables
    a = 0x01234567
    b = 0x89abcdef
    c = 0xfedcba98
    d = 0x76543210

    # Ensure input_data is of type bytes
    if isinstance(input_data, str):
        input_data = input_data.encode('utf-8')

    # Process in 32-bit blocks
    for i in range(0, len(input_data), 4):
        block = input_data[i:i+4]

        # Mix the block with state variables
        a ^= (a << 5) + int.from_bytes(block, 'big') + (a >> 2)
        b ^= (b << 7) + int.from_bytes(block, 'big') - (b >> 3)
        c ^= (c << 11) + int.from_bytes(block, 'big') * (c >> 5)
        d ^= (d << 13) + int.from_bytes(block, 'big') // (d >> 7)

    # Combine the state variables and truncate to 256 bits with better balance
    hash_value = (a << 96) | (b << 64) | (c << 32) | d
    mask = (1 << 256) - 1
    truncated_hash = ((hash_value & mask) + ((hash_value >> 128) & mask)) & mask

    # Convert the truncated hash to a hexadecimal string with both lower and uppercase letters
    hex_str = format(truncated_hash, '064x')
    mixed_case_hash = ''.join([c.upper() if i % 2 == 0 else c for i, c in enumerate(hex_str)])

    return mixed_case_hash


def save_image(surface, filename):
    pygame.image.save(surface, filename)


def save_hash_to_file(hash_value, filename):
    with open(filename, 'w') as file:
        file.write(hash_value)


def main():
    pygame.init()

    text_file_path = 'TextFiles/TestFile.txt'
    text = read_text_from_file(text_file_path)

    binary_text = text_to_binary(text)
    grid = create_grid(binary_text)

    size = len(grid)
    cell_size = 2
    window_size = size * cell_size
    grid_color = (100, 100, 100)

    screen = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption("Conway's Game of Life")

    max_steps = 15

    start_time = time.time()

    for steps in range(max_steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        grid = update(grid)

        progress = (steps + 1) / max_steps * 100
        print(f"Progress: {progress:.2f}%")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")

    # Visualize the final state
    screen.fill((0, 0, 0))
    draw_grid(screen, grid, cell_size, grid_color)
    pygame.display.flip()

    # Save the final Conway board image
    image_directory = "ConwayBoardImages"
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    image_filename = os.path.join(
        image_directory,
        f"final_conway_board_{os.path.splitext(os.path.basename(text_file_path))[0]}_{time.strftime('%Y%m%d_%H%M%S')}.png"
    )
    save_image(screen, image_filename)

    print(f"Final Conway board image saved to {image_filename}")

    # Save the hash as a text file
    hash_directory = "ConwayBoardHashes"
    if not os.path.exists(hash_directory):
        os.makedirs(hash_directory)

    input_data = compress_and_encode_lzma(''.join(map(str, grid.flatten())))
    hashed_value = custom_hash(input_data)

    hash_filename = os.path.join(
        hash_directory,
        f"final_conway_hash_{os.path.splitext(os.path.basename(text_file_path))[0]}_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    )
    save_hash_to_file(hashed_value, hash_filename)

    print(f"Hash saved to {hash_filename}")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()
