import tkinter as tk
from tkinter.ttk import *
import cv2
import threading
import time

from gaze_tracking import GazeTracking
from mouse_controller import MouseController

class Application:
    def __init__(self):
        #set up tkinter application
        self.root = tk.Tk()

        #dimensions of screen
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.root.title("HOTH XII")
        self.root.geometry("{len:.0f}x{len:.0f}+{xoffset:.0f}+{yoffset:.0f}".format(
            len = min(self.width, self.height) * 0.5,
            xoffset = self.width * 0.2,
            yoffset = self.height * 0.2
        ))
        self.root.resizable(width = False, height = False)

        #create a mouse controller for emulation
        self.mc = MouseController()

        #set up gaze tracker
        self.gaze_tracker = GazeTracking()
        self.webcam = cv2.VideoCapture(0) #will feed in frames from the laptop's webcam
        
        #delay the gaze tracking by software by x milliseconds so
        #the mouse controller isnt lagging
        self.ms_delay = 50

        #create a separate thread for processing each frame of
        #webcam capture and figuring out pupil position/gaze direction
        gaze_thread = threading.Thread(target=self.update)
        gaze_thread.start()

        self.root.mainloop() #tkinter MUST be on main thread

        #stop the video recording
        self.webcam.release()
        cv2.destroyAllWindows()

        gaze_thread.join()

    def update(self):
        print("update")

        time.sleep(self.ms_delay / 1000)
        self.update()
        
app = Application() #start the tkinter application

            