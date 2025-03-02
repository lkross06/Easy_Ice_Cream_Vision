import cv2
from pynput.keyboard import Listener
import time

from gaze_tracking import GazeTracking
from mouse_controller import MouseController

######### INITIALIZATION #############

#delay the gaze tracking by software by x milliseconds so
#the mouse controller isnt lagging
GAZE_DELAY = 50
#however we want the mouse movement to be smooth, so it can update instantaneously
MOUSE_DELAY = 10;
MS_ELAPSED = 0;

keep_updating = True

def handle_key_press(event):
    try:
        #for keyboard keys
        if event.char == 'q':
            print("Q PRESSED")
            global keep_updating
            keep_updating = False
    except AttributeError:
        #for other keys (cmd, shift, tab, etc.)
        return


#create a mouse controller for emulation
mc = MouseController()

#create a keyboard listener for listening
kl = Listener(on_press=handle_key_press)
kl.start()

#set up gaze tracker
gaze_tracker = GazeTracking()
webcam = cv2.VideoCapture(0) #will feed in frames from the laptop's webcam


######### UPDATE LOOP #############
while True:
    if MS_ELAPSED % GAZE_DELAY == 0:
        _, frame = webcam.read()

        #analyze and update gaze tracker
        gaze_tracker.refresh(frame)

        #add markers for pupil location to frame image data
        frame = gaze_tracker.annotated_frame()

        text = "N/A"
        if gaze_tracker.is_blinking():
            text = "Blinking"
        elif gaze_tracker.is_right():
            text = "Looking right"
        elif gaze_tracker.is_left():
            text = "Looking left"
        elif gaze_tracker.is_center():
            text = "Looking center"

        print(text, end=" ")

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = gaze_tracker.pupil_left_coords()
        right_pupil = gaze_tracker.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("HOTH XII", frame)

    if MS_ELAPSED % MOUSE_DELAY == 0:
        #update mouse stuff here? with accel/decel
        _ = 0

    MS_ELAPSED += 1
    
    #try to perform next update
    print(keep_updating)
    if keep_updating:
        time.sleep(0.001) #pause for 1ms
    else:
        break

######### DESTRUCTION #############
#stop the video recording
webcam.release()
cv2.destroyAllWindows()
