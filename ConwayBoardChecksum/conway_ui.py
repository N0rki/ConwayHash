import tkinter as tk
from tkinter import filedialog
import threading
import os
import pygame
import sys
import time
from .file_handler import convert_to_txt
from .conway_game import (
    text_to_binary, compress_and_encode_lzma, create_grid, update, draw_grid, save_image,
    custom_hash, save_hash_to_file, read_text_from_file
)

icondata = '''
R0lGODdhQABAAIUAAP////j4+Pf39/X19fT09PPz8/Ly8u7u7u3t7evr6+rq6unp6ejo6Ofn5+bm
5t/f397e3t3d3dnZ2dfX19bW1tXV1c3NzczMzMvLy8fHx8XFxcTExLa2tjs7Ozk5OSwsLCsrKyoq
KigoKCcnJyYmJiIiIiEhIR8fHxwcHBsbGxoaGhYWFhUVFRQUFBAQEA8PDw4ODg0NDQwMDAsLCwoK
CggICAcHBwYGBgUFBQQEBAMDAwAAAAAAAAAAAAAAAAAAACwAAAAAQABAAEAI/wBRvHjBYgMDBhE+
DFyRYmHDFwwdSoT4MCJBgwgrHEw40aLFFx9KlBiBAgYMFipMolSZ8mTLlS5ZyoTRQsOCBRAyVKhg
IcTMFhx2Xqhwc4GGnT1nwlz6sqnSlyFEkshw8wGIpzNhULgJYStOnTx9xhzLFCtZp2dN1iyawmxZ
mkF5ehA5AoRUqgusmgUq9GiFC36Tmgws9u3avFfJRh1ZMu3JxSTdtoTR1vFSyI1hHtZrGbJdxio9
iyxRmW9YyaHpfo481vTQqok1xxUMI/Bc0JbRvtVsM28HupnRmq5Qebfu43t7d4WtVLRIrzmRFkae
2y3mvXErhBy5enXwn3EB9/+Vjrrz6OLUTVu4zVo9++9wkbLvDtwkjO2sDffmLJu8Y9eEqRWeX8SV
Z1h4RCGGnX/G2VfafrFR12B8cqlWH4WvKWhSDDvsgMMEAAAwgAkd2sDhDiaWeGKKKK7oYoc3UBBi
AQmEOKKKOLbY4Q4K2EiijkCyKOSLQZ4YY4gE/HgDkSziIGOIMOQ4pJRMVgnjkwX0CECSOd4A4pY1
hmiklUVSaeYOXiKpJZdlArnDAkgqSeaUbdKZpog/0snimzOuKeeZes4p6JUhArBmmASEeWOdRsoA
o6NoDtrmnQBEyeiZHyKJqJ+ANvoojCfuYGmgOWaKZ6lfLkqnqYlq6uOOY57/eeSWeRqZaq1d3trp
jlqqSuSsbNop6Q2QLtklpKLuiqauQAKLa7Nftnrqsq5CqSypHj4ZLJnGXtrhqLF6e6e0vpaq7bMs
dpssmudeKymrij7rZJw7vlBiBTOW0GENlvK7b78A/3tvvgLv4C+K+AJgAJwAFKDvtzAyi+3EtlZb
bps7sGCDiRYUUAADItRQgwssiEyyySWPnPLJKqMs8gsYGGCAAw94DLLLLY/cwsY2IBBiACd0mIOk
FEdsY9A7DC2rBIVCYHPIObMs9cpU48wyzDI3QMLGJ1m9s4kxyzyD0ESXbfSWPgMQwLM3MA2AAGEC
sILVVUdd99Q4Yz0zBFlD/311xwU0ULPH4LprOLVgvhokDUIz3qHGNnRtN92UT17DC4A3wLcBDfh9
d8o1pL324UWj6LgOT15M5w4RZL115J9XjrflmD8t+9c2rCk6umbX6bjSk7oNQOt7u8517JbPrjzy
ehtwKJK7k967nV8C4HTggwtue/Jf08R198gv/zLgBYyd9O+/c+u2AAeEyP7PvF/r+A5zJ3/31zFk
nv3mnd/+/f+wE9nBSte2nyEtB6dLXfzQtL72vc2Bo+tQ/cSns43lb3suwB/gbhY1DXpMe9jb3gDV
Z0CywchtQDNhs1B4QPSpMGPHq5ze+pez2n3Mc3nbIA4tFzr4yUpiK0ofoLyE6K0dXI+Ds5vhDjMY
Q+4BUHJMjBzuzAc86ikuXShcYAEf6EMGus+BcpNdymyIxDGGjYZJ1N/2bAjCAhTOdypMFxCl5MKk
BbFxO5pg+O5nwTMucWXgE6MA30jA9cVraV3EFv1MFkj7je+DgysjI/vYN6818WBbjODE6lhFIxny
ip7s4iIv50dBOrKCHIMkBvFXSpFZ6k6q610mW6jCLcJNcTuwF8IIZrCA9bJgBxtgwhwGzFElbGG8
3EFAAAA7
'''


def apply_icon(w):
    try:
        icon = tk.PhotoImage(data=icondata)
        w.iconphoto(True, icon)
    except Exception as e:
        print("Could not load icon due to:\n  ", e)


class ConwayGameUI:
    def __init__(self, root):
        self.file_path = None
        self.warning_label = None
        self.result_label = None
        self.checksum_path_entry = None
        self.file_path_entry = None
        self.root = root
        self.show_conway_visual = False
        self.setup_ui()
        self.root.resizable(False, False)
        apply_icon(root)

    def setup_ui(self):
        # Create and place widgets
        file_path_label = tk.Label(self.root, text="Choose Text File:")
        file_path_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.file_path_entry = tk.Entry(self.root, width=50)
        self.file_path_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        browse_file_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        browse_file_button.grid(row=0, column=2, sticky="e", padx=10, pady=10)

        checksum_path_label = tk.Label(self.root, text="Choose hash file:")
        checksum_path_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.checksum_path_entry = tk.Entry(self.root, width=50)
        self.checksum_path_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        browse_checksum_button = tk.Button(self.root, text="Browse", command=self.browse_checksum)
        browse_checksum_button.grid(row=1, column=2, sticky="e", padx=10, pady=10)

        conway_visual_checkbox = tk.Checkbutton(self.root, text="Show Conway Board", command=self.toggle_conway_visual)
        conway_visual_checkbox.grid(row=2, column=0, pady=10, columnspan=3, sticky="nsew")

        self.warning_label = tk.Label(self.root, text="!!! Slower !!!", fg="red")
        self.warning_label.grid(row=2, column=1, pady=10, padx=40, sticky="e")

        check_button = tk.Button(self.root, text="Check", command=lambda: self.main(progress_var, result_var))
        check_button.grid(row=3, column=0, columnspan=3, pady=20)

        progress_var = tk.StringVar()
        progress_label = tk.Label(self.root, textvariable=progress_var)
        progress_label.grid(row=4, column=0, columnspan=3, pady=10)

        result_var = tk.StringVar()
        self.result_label = tk.Label(self.root, textvariable=result_var)
        self.result_label.grid(row=5, column=0, columnspan=3, pady=10)

    def browse_file(self):
        original_file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        temp_file_path = convert_to_txt(original_file_path)

        # Store the original file path in the label, but use the temporary file path for processing
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, original_file_path)

        # Update the actual file path that will be used in the program
        self.file_path = temp_file_path

    def browse_checksum(self):
        checksum_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        checksum_path = convert_to_txt(checksum_path)
        self.checksum_path_entry.delete(0, tk.END)
        self.checksum_path_entry.insert(0, checksum_path)

    def update_result_label(self, result_var, result_message, color):
        result_var.set(result_message)
        self.result_label.config(text=result_message, fg=color)
        self.root.update_idletasks()

    def toggle_conway_visual(self):
        self.show_conway_visual = not self.show_conway_visual

    def main(self, progress_var, result_var):
        pygame.init()

        text_file_path = self.file_path
        checksum_file_path = self.checksum_path_entry.get()

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

        def update_progress_label(progress):
            progress_var.set(f"Progress: {progress:.2f}%")
            self.root.update_idletasks()

        def visualize():
            screen.fill((0, 0, 0))
            draw_grid(screen, grid, cell_size, grid_color)
            pygame.display.flip()

        def update_and_visualize():
            nonlocal grid
            for steps in range(max_steps):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                grid = update(grid)

                # Update the progress bar every half step
                progress = (steps + 1) / max_steps * 100
                self.root.after(10, update_progress_label, progress)  # Update every 10 milliseconds

                elapsed_time = time.time() - start_time
                estimated_time_to_finish = (elapsed_time / (steps + 1)) * (max_steps - (steps + 1))

                progress_label_text = (f"Progress: {progress:.2f}% | Elapsed Time: {elapsed_time:.2f}s "
                                       f"| Estimated Time to Finish: {estimated_time_to_finish:.2f}s")
                self.root.after(10, progress_var.set, progress_label_text)  # Update progress label

                if self.show_conway_visual:
                    self.root.after(10, visualize)

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Time taken: {elapsed_time:.01f} seconds")

            if self.show_conway_visual:
                # Save the final Conway board image
                image_directory = "ConwayBoardImages"
                if not os.path.exists(image_directory):
                    os.makedirs(image_directory)

                image_filename = os.path.join(
                    image_directory,
                    f"final_conway_board_{os.path.splitext(os.path.basename(text_file_path))[0]}_"
                    f"{time.strftime('%Y%m%d_%H%M%S')}.png"
                )
                save_image(screen, image_filename)

                print(f"Final Conway board image saved to {image_filename}")

            hash_directory = "ConwayBoardHashes"
            if not os.path.exists(hash_directory):
                os.makedirs(hash_directory)

            input_data = compress_and_encode_lzma(''.join(map(str, grid.flatten())))
            hashed_value = custom_hash(input_data)

            hash_filename = os.path.join(
                hash_directory,
                f"final_conway_hash_{os.path.splitext(os.path.basename(text_file_path))[0]}"
                f"_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            )
            save_hash_to_file(hashed_value, hash_filename)

            print(f"Hash saved to {hash_filename}")

            with open(checksum_file_path, 'r') as file:
                saved_hash = file.read()

            if hashed_value == saved_hash:
                result_message = "The file is unchanged"
                result_color = "green"
            else:
                result_message = "The file is changed"
                result_color = "red"

            self.root.after(10, lambda: self.update_result_label(result_var, result_message, result_color))

        # Start a separate thread for the computational tasks
        thread = threading.Thread(target=update_and_visualize)
        thread.start()

        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conway's Game of Life Checker")

    ConwayGameUI(root)

    root.mainloop()
