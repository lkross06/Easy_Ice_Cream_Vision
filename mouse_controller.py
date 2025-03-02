from pynput.mouse import Button, Controller

class MouseController:
    def __init__(self):
        self._mouse = Controller()
        self._isPressing = False

    def get_position(self):
        #NOTE: top left corner is (0,0)
        return self._mouse.position

    def set_position(self, x = -1, y = -1):
        #if x or y not specified, don't change it (i.e. set it to its current position)
        if x == -1:
            x = self._mouse.position[0]
        elif y == -1:
            y = self._mouse.position[1]
        self._mouse.position = (x, y)
    
    def press(self):
        #set guards on whether or not to start pressing or releasing
        if not self._isPressing:
            self._mouse.press(Button.left)
        self._isPressing = True
    
    def release(self):
        if self._isPressing:
            self._mouse.release(Button.left)
        self._isPressing = False

    def click(self, n = 1):
        #clicks n times
        self._mouse.click(Button.left, n)