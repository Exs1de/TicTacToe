import tkinter as tk
from tkinter import ttk
import sys

# custom class used to change ttk button size (wraps ttk Button with Frame)
class MyButton(ttk.Frame):
        def __init__(self, parent, height=None, width=None, text="", command=None, style=None):
            ttk.Frame.__init__(self, parent, height=height, width=width, style="MyButton.TFrame")
            self.pack_propagate(0)
            self._btn = ttk.Button(self, text=text, command=command, style=style)
            self._btn.pack(fill=tk.BOTH, expand=True)


GAME_WIDTH = 800
GAME_HEIGHT = 800

root = tk.Tk()
root.title("TIC TAC TOE")

# Gets the height and width of Monitor
monitor_width = root.winfo_screenwidth()
monitor_height = root.winfo_screenheight()

# Gets both half the screen width/height and GAME_WINDOW width/height
X_OFFSET = int(monitor_width/2 - GAME_WIDTH/2)
Y_OFFSET = int(monitor_height/2 - GAME_HEIGHT/2) 

# Apply game window size
root.geometry(f'{GAME_WIDTH}x{GAME_HEIGHT}+{X_OFFSET}+{Y_OFFSET}')
root.resizable(False, False)

# SCREEN contains currrent game state, 
# when state changes, SCREEN destroys and recreates
SCREEN = tk.Frame() # bg='red')
SCREEN.pack(side="top", fill="both", expand = True)
