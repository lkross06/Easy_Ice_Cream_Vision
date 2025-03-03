from pynput.mouse import Controller

class MouseController:
    DECEL = 0.08
    TERMINAL = 25
    DEFAULT_MAGNITUDE = 4

    def __init__(self):
        self.__mouse = Controller()
        self.__is_pressing = False

        self._vx = 0
        self._vy = 0

    def get_position(self):
        #NOTE: top left corner is (0,0)
        return self.__mouse.position

    def update_position(self):
        cx, cy = self.get_position()
        self.__mouse.position = (cx + self._vx, cy + self._vy)

        #apply deceleration
        self.apply_decel()
    
    def press(self):
        #set guards on whether or not to start pressing or releasing
        if not self.__is_pressing:
            self.__mouse.press(Button.left)
        self.__is_pressing = True
    
    def release(self):
        if self.__is_pressing:
            self.__mouse.release(Button.left)
        self.__is_pressing = False

    def click(self, n = 1):
        #clicks n times
        self.__mouse.click(Button.left, n)

    def apply_force(self, direction, magnitude = DEFAULT_MAGNITUDE):
        if direction == "up":
            self._vy -= magnitude
        elif direction == "down":
            self._vy += magnitude
        elif direction == "right":
            self._vx += magnitude
        elif direction == "left":
            self._vx -= magnitude
        
        #cap the speed at which the vector can accelerate to
        if abs(self._vx) > self.TERMINAL:
            if self._vx < 0: self._vx = -1 * self.TERMINAL
            else: self._vx = self.TERMINAL
        if abs(self._vy) > self.TERMINAL:
            if self._vy < 0: self._vy = -1 * self.TERMINAL
            else: self._vy = self.TERMINAL

    def apply_decel(self, x = True, y = True):
        if x:
            self._vx -= self.DECEL * self._vx
            if self._vx > 0:
                if self._vx < 0: self._vx = 0
            elif self._vx < 0:
                if self._vx > 0: self._vx = 0

        if y:
            self._vy -= self.DECEL * self._vy
            if self._vy > 0:
                self._vy -= self.DECEL
                if self._vy < 0: self._vy = 0
            elif self._vy < 0:
                self._vy += self.DECEL
                if self._vy > 0: self._vy = 0
    
    def reset(self):
        self._vx = 0
        self._vy = 0