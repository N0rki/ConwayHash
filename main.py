import tkinter as tk
from ConwayBoardChecksum.conway_ui import ConwayGameUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conway's Game of Life Checker")

    # Create an instance of ConwayGameUI, passing the Tkinter root window
    ConwayGameUI(root)

    # Start the Tkinter main loop
    root.mainloop()
