import cv2
from pynput.keyboard import Listener

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

def put_bordered_text(img, text, pos, font = cv2.FONT_HERSHEY_DUPLEX, font_scale = 2, text_color = (0, 0, 255), border_color = (0, 0, 0), thickness = 1):
    #to put bordered text we really just draw a larger version of the text in the border color
    #than a smaller version of the text in the normal color
    cv2.putText(img, text, pos, font, font_scale, border_color, thickness + 7) #border
    cv2.putText(img, text, pos, font, font_scale, text_color, thickness) #normal
    

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
    fr_height, fr_width, _ = frame.shape
    sm_padding = 60
    md_padding = 120

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

    put_bordered_text(frame, dir_text, (0 + sm_padding, 0 + sm_padding))

    try:
        put_bordered_text(frame, "HR: {br:.3f}".format(br=gaze_tracker.get_hr()), (0 + sm_padding, md_padding + sm_padding))
        put_bordered_text(frame, "VR: {bl:.3f}".format(bl=gaze_tracker.get_vr()), (0 + sm_padding, 2 * md_padding))
    except TypeError:
        continue

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

    put_bordered_text(frame, blink_text, (0 + sm_padding, round(fr_height / 2) + sm_padding))

    try:
        put_bordered_text(frame, "BR: {br:.1f}".format(br=gaze_tracker.get_br()), (0 + sm_padding, round(fr_height / 2) + md_padding + sm_padding))
        put_bordered_text(frame, "BL: {bl:.1f}".format(bl=gaze_tracker.get_bl()), (0 + sm_padding, round(fr_height / 2) + 2 * md_padding))
    except TypeError:
        continue

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
