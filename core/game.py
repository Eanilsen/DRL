# The Game is where it all starts. A Game is an abstract and thin package in
# which all of the elements of the game are stored. It is responsible for
# creating the world, parsing and writing to save files, and turning on/off
# graphics.

from core import graphics

import sys
import traceback
import curses

# A Game represents a single instance of a game, including its maps,
# data, and everything else.
class Game(object):
    def __init__(self):
        self.x, self.y = 0, 0

    def step(self):
        running = True
        x,y = 0,0
        while running:
            c = graphics.scr().getch()
            if c == curses.KEY_UP: y -= 1
            elif c == curses.KEY_DOWN: y += 1
            elif c == curses.KEY_LEFT: x -= 1
            elif c == curses.KEY_RIGHT: x += 1
            elif c == ord('q'): running = False

            if c != -1:
                graphics.scr().clear()
                graphics.scr().addch(y, x, '@')

    # Runs an interactive session of our game with the player.
    def play(self):
        graphics.start()

        try:
            self.step()
        except:
            graphics.stop()
            print traceback.format_exc()
            sys.exit(-1)
