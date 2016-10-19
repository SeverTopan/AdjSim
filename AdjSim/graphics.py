#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import sys
import tkinter
import time
import random
from constants import *

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
        self.tk.title("AdjSim")

        self.windowHeight = self.tk.winfo_screenheight() - 100
        self.windowWidth = self.tk.winfo_screenwidth() - 100

        self.canvas = tkinter.Canvas(self.tk, height=self.windowHeight, \
            width=self.windowWidth, highlightthickness=0)

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

            # set trait constant
            normalizedX = agent.traits['xCoord'].value + self.windowWidth / 2
            normalizedY = agent.traits['yCoord'].value + self.windowHeight / 2
            size = agent.traits['size'].value
            borderWidth = agent.traits['borderWidth'].value

            # set color
            color = self.colorMapping.get(agent.traits['type'].value)
            if color is None:
                if agent.traits['color'].value is not None:
                    color = agent.traits['color'].value
                else:
                    colorIndex = random.randint(0, len(COLORS) - 1)
                    color = COLORS[colorIndex]
                self.colorMapping[agent.traits['type'].value] = color

            # create object
            newObject = self.canvas.create_circle(normalizedX, normalizedY, \
                size, fill=color, width=borderWidth)
            self.objectList.append(newObject)

        # update
        self.tk.update()
