#-------------------------------------------------------------------------------
# ADJECOSYSTEM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import sys
import tkinter
import time
import random

#-------------------------------------------------------------------------------
# GLOBAL CONSTANTS
#-------------------------------------------------------------------------------
RED_LIGHT = '#ff6961'
RED_DARK = '#c23b22'
BLUE_LIGHT = '#aec6cf'
BLUE_DARK = '#779ecb'
GREEN = '#bdecb6'
PINK = '#dea5a4'
WHITE = '#f0ead6'

COLORS = [RED_LIGHT, RED_DARK, BLUE_LIGHT, BLUE_DARK, GREEN, PINK, WHITE]

OBJECT_RADIUS = 25
OBJECT_BORDER_WIDTH = 2

#-------------------------------------------------------------------------------
# GLOBAL FUNCTIONS
#-------------------------------------------------------------------------------
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tkinter.Canvas.create_circle = _create_circle

#-------------------------------------------------------------------------------
# CLASS GRAPHICS
#-------------------------------------------------------------------------------
class BellFunction(object):
    """docstring for BellFunction."""

# METHOD INIT
#-------------------------------------------------------------------------------
    def __init__(self, a, b, c):
        super(BellFunction, self).__init__()
        self.a = a
        self.b = b
        self.c = c

# METHOD CALL
#-------------------------------------------------------------------------------
    def __call__(self, x):
        return 1 / (1 + abs((x - self.c) / self.a)**(2*self.b))

#-------------------------------------------------------------------------------
# CLASS GRAPHICS
#-------------------------------------------------------------------------------
class Graphics(object):
    """docstring for Graphics."""

# METHOD INIT
#-------------------------------------------------------------------------------
    def __init__(self):
        super(Graphics, self).__init__()
        self.objectList = []
        self.colorMapping = {}

        self.tk = tkinter.Tk()
        self.tk.title("AdjEcosystem")

        self.windowHeight = self.tk.winfo_screenheight() - 100
        self.windowWidth = self.tk.winfo_screenwidth() - 100

        self.canvas = tkinter.Canvas(self.tk, height=self.windowHeight, \
            width=self.windowWidth, highlightthickness=0, background=WHITE)

        self.canvas.pack()
        self.tk.update()

# METHOD UPDATE
#-------------------------------------------------------------------------------
    def update(self, agentSet):
        # clear old object list
        for item in self.objectList:
            self.canvas.delete(item)
        self.objectList.clear()

        # fill new objects
        for agent in agentSet:
            if agent.name is 'environment':
                continue

            normalizedX = agent.traits['xCoord'].value + self.windowWidth / 2
            normalizedY = agent.traits['yCoord'].value + self.windowHeight / 2

            color = self.colorMapping.get(agent.traits['type'].value)
            if color is None:
                colorIndex = random.randint(0, len(COLORS) - 1)
                color = COLORS[colorIndex]
                self.colorMapping[agent.traits['type'].value] = color

            newObject = self.canvas.create_circle(normalizedX, normalizedY, \
                OBJECT_RADIUS, fill=color, width=OBJECT_BORDER_WIDTH)
            self.objectList.append(newObject)

        # update
        self.tk.update()
