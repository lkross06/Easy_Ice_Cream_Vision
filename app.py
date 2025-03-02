import cv2
from pynput.keyboard import Listener
import time

from gaze_tracking import GazeTracking
from mouse_controller import MouseController


class Application:
    def __init__(self):
        #create a mouse controller for emulation
        self.mc = MouseController()

        #create a keyboard listener for listening
        kl = Listener(on_press=self.handle_key_press)
        kl.start()

        #set up gaze tracker
        self.gaze_tracker = GazeTracking()
        self.webcam = cv2.VideoCapture(0) #will feed in frames from the laptop's webcam
        
        #delay the gaze tracking by software by x milliseconds so
        #the mouse controller isnt lagging
        self.ms_delay = 50
        self.keep_updating = True

        # #create a separate thread for processing each frame of
        # #webcam capture and figuring out pupil position/gaze direction
        # self.gaze_thread = threading.Thread(target=self.update)
        # self.gaze_thread.start()

        # self.root.mainloop() #tkinter MUST be on main thread
        self.update()

    def update(self):
        print("update")
        _, frame = self.webcam.read()

        #analyze and update gaze tracker
        self.gaze_tracker.refresh(frame)

        #add markers for pupil location to frame image data
        frame = self.gaze_tracker.annotated_frame()

        text = "N/A"
        if self.gaze_tracker.is_blinking():
            text = "Blinking"
        elif self.gaze_tracker.is_right():
            text = "Looking right"
        elif self.gaze_tracker.is_left():
            text = "Looking left"
        elif self.gaze_tracker.is_center():
            text = "Looking center"

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = self.gaze_tracker.pupil_left_coords()
        right_pupil = self.gaze_tracker.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("Demo", frame)

        #delay until next update
        if self.keep_updating:
            time.sleep(self.ms_delay / 1000)
            self.update()
    
    def destroy(self):
        #stop the video recording
        self.webcam.release()
        cv2.destroyAllWindows()
    
    def handle_key_press(self, event):
        if event.char == 'q':
            print("Q PRESSED")
            self.keep_updating = False
            self.destroy()
        
app = Application() #start the application
