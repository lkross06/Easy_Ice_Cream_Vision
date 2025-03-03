from pynput.mouse import Button, Controller

class MouseController:
    def __init__(self):
        self.__mouse = Controller()
        self.__is_pressing = False

    def get_position(self):
        #NOTE: top left corner is (0,0)
        return self.__mouse.position

    def set_position(self, x = -1, y = -1):
        #if x or y not specified, don't change it (i.e. set it to its current position)
        if x == -1:
            x = self.__mouse.position[0]
        elif y == -1:
            y = self.__mouse.position[1]
        self.__mouse.position = (x, y)
    
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
