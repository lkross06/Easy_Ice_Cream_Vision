from pynput.mouse import Button, Controller, Listener

class MouseController:
    def __init__(self):
        self.mouse = Controller()
        self.isPressing = False

    def get_position(self):
        #NOTE: top left corner is (0,0)
        return self.mouse.position

    def set_position(self, x = -1, y = -1):
        #if x or y not specified, don't change it (i.e. set it to its current position)
        if x == -1:
            x = self.mouse.position[0]
        elif y == -1:
            y = self.mouse.position[1]
        self.mouse.position = (x, y)
    
    def press(self):
        #set guards on whether or not to start pressing or releasing
        if not self.isPressing:
            self.mouse.press(Button.left)
        self.isPressing = True
    
    def release(self):
        if self.isPressing:
            self.mouse.release(Button.left)
        self.isPressing = False

    def click(self, n = 1):
        #clicks n times
        self.mouse.click(Button.left, n)