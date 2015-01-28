# The Game is where it all starts. A Game is an abstract and thin package in
# which all of the elements of the game are stored. It is responsible for
# creating the world, parsing and writing to save files, and turning on/off
# graphics.

from core import graphics
from core import world

import sys
import traceback

# A Game represents a single instance of a game, including its maps,
# data, and everything else.
class Game(object):
    def __init__(self):
        self.world = world.World()

    # Runs an interactive session of our game with the player until either
    # the player stops playing or an error occurs. Here, we pass input to the
    # world until we are told we do not need to anymore. If an error occurs, we
    # turn off the graphics, print the traceback, and kill the program.
    def play(self):
        graphics.start()

        try:
            running = True
            while running:
                c = graphics.get_input()
                self.world.handle_keys(c)
                if c == 'q': running = False
                self.world.draw()
        except:
            graphics.stop()
            print traceback.format_exc()
            sys.exit(-1)

        graphics.stop()
