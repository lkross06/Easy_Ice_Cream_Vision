import cv2
from pynput.keyboard import Listener

from gaze_tracking import GazeTracking
from mouse_controller import MouseController

######### INITIALIZATION #############

#must be blinking for 1000ms to simulate a click
BLINK_TIMER_DURATION = 5
BLINK_TIMER_COOLDOWN = 10 #gotta wait before you can click again

WINK_TIMER_DURATION = 5
WINK_TIMER_COOLDOWN = 10

keep_updating = True

blink_timer = BLINK_TIMER_DURATION
blink_cooldown = BLINK_TIMER_COOLDOWN

wink_timer = WINK_TIMER_DURATION
wink_cooldown = WINK_TIMER_COOLDOWN

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
    mc.update_position()

    _, frame = webcam.read()
    fr_height, fr_width, _ = frame.shape
    sm_padding = 60
    md_padding = 120

    #analyze and update gaze tracker
    gaze_tracker.refresh(frame)

    if gaze_tracker.both_pupils_found():
        #add markers for pupil location to frame image data
        frame = gaze_tracker.annotated_frame()

        dir_text = "looking --"
        dir = gaze_tracker.true_gaze_direction()
        
        match dir:
            case 0:
                dir_text = "looking top left"
                mc.apply_force("left")
                mc.apply_force("up")
            case 1:
                dir_text = "looking top middle"
                mc.apply_force("up")
                mc.apply_decel(y = False)
            case 2:
                dir_text = "looking top right"
                mc.apply_force("right")
                mc.apply_force("up")
            case 3:
                dir_text = "looking middle left"
                mc.apply_force("left")
                mc.apply_decel(x = False)
            case 4:
                dir_text = "looking center"
                mc.apply_decel()
            case 5:
                dir_text = "looking middle right"
                mc.apply_force("right")
                mc.apply_decel(x = False)
            case 6:
                dir_text = "looking bottom left"
                mc.apply_force("left")
                mc.apply_force("bottom")
            case 7:
                dir_text = "looking bottom middle"
                mc.apply_force("bottom")
                mc.apply_decel(y = False)
            case 8:
                dir_text = "looking bottom right"
                mc.apply_force("right")
                mc.apply_force("bottom")

        put_bordered_text(frame, dir_text, (0 + sm_padding, 2 * sm_padding))

        hr = "--"
        vr = "--"
        try:
            hr = "{x:.2f}".format(x=gaze_tracker.horizontal_ratio())
            vr = "{x:.2f}".format(x=gaze_tracker.vertical_ratio())
        except TypeError:
            continue

        put_bordered_text(frame, "HR: " + hr, (0 + sm_padding, md_padding + 2 * sm_padding))
        put_bordered_text(frame, "VR: " + vr, (0 + sm_padding, 2 * md_padding + sm_padding))

        blink_text = "--"
        blink = gaze_tracker.true_gaze_blinking()

        match blink:
            case 0:
                blink_text = "not blinking"
                mc.release()

                blink_timer = BLINK_TIMER_DURATION
                blink_cooldown -= 1

                wink_timer = WINK_TIMER_DURATION
                wink_cooldown -= 1
            case 1:
                blink_text = "left winking"
                wink_timer -= 1
            case 2:
                blink_text = "right winking"
                wink_timer -= 1
            case 3:
                blink_text = "blinking"
                blink_timer -= 1

        put_bordered_text(frame, blink_text, (0 + sm_padding, round(fr_height / 2) + sm_padding))

        br = "--"
        bl = "--"
        try:
            br = "{x:.2f}".format(x=gaze_tracker.get_br())
            bl = "{x:.2f}".format(x=gaze_tracker.get_bl())
        except TypeError:
            continue

        put_bordered_text(frame, "BR: " + br, (0 + sm_padding, round(fr_height / 2) + md_padding + sm_padding))
        put_bordered_text(frame, "BL: " + bl, (0 + sm_padding, round(fr_height / 2) + 2 * md_padding))
    else:
        mc.reset()

    cv2.imshow("Easy Ice Cream Vision", frame)

    #update mouse things
    mc.update_position()

    if blink_timer <= 0 and blink_cooldown <= 0:
        mc.click()
        blink_cooldown = BLINK_TIMER_COOLDOWN
        
    if wink_timer <= 0 and wink_cooldown <= 0:
        mc.press()
        wink_cooldown = WINK_TIMER_COOLDOWN
    
    # #try to perform next update
    if not keep_updating:
        break
    else:
        cv2.waitKey(1)


######### DESTRUCTION #############
#stop the video recording
webcam.release()
cv2.destroyAllWindows()
