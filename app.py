import tkinter as tk
from tkinter.ttk import *
import time as t
from mouse_controller import MouseController

class Application:
    def __init__(self):
        #set up tkinter application
        self.root = tk.Tk()

        #dimensions of screen
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.root.title("HOTH_XII")
        self.root.geometry("{len:.0f}x{len:.0f}+{xoffset:.0f}+{yoffset:.0f}".format(
            len = min(self.width, self.height) * 0.5,
            xoffset = self.width * 0.2,
            yoffset = self.height * 0.2
        ))
        self.root.resizable(width = False, height = False)

        self.root.mainloop()

app = Application() #start the tkinter application

            