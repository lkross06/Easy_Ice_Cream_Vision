import cv2
from pynput.keyboard import Listener
import time

from gaze_tracking import GazeTracking
from mouse_controller import MouseController

######### INITIALIZATION #############

keep_updating = True

def handle_key_press(event):
    try:
        #for keyboard keys
        if event.char == 'q':
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
    _, frame = webcam.read()

    #analyze and update gaze tracker
    gaze_tracker.refresh(frame)

    #add markers for pupil location to frame image data
    frame = gaze_tracker.annotated_frame()

    dir_text = "idk bruh"
    dir = gaze_tracker.true_gaze_direction()
    
    match dir:
        case 0:
            dir_text = "looking top left"
        case 1:
            dir_text = "looking top middle"
        case 2:
            dir_text = "looking top right"
        case 3:
            dir_text = "looking middle left"
        case 4:
            dir_text = "looking center"
        case 5:
            dir_text = "looking middle right"
        case 6:
            dir_text = "looking bottom left"
        case 7:
            dir_text = "looking bottom middle"
        case 8:
            dir_text = "looking bottom right"

    cv2.putText(frame, dir_text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    blink_text = "idk bruh"
    blink = gaze_tracker.true_gaze_blinking()

    match blink:
        case 0:
            blink_text = "not blinking"
        case 1:
            blink_text = "left winking"
        case 2:
            blink_text = "right winking"
        case 3:
            blink_text = "blinking"

    cv2.putText(frame, blink_text, (90, 130), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)


    cv2.imshow("Demo", frame)

    #update mouse stuff here? with accel/decel
    mc.update()
    
    # #try to perform next update
    if not keep_updating:
        break
    else:
        cv2.waitKey(1)


######### DESTRUCTION #############
#stop the video recording
webcam.release()
cv2.destroyAllWindows()
