from core import graphics

import random

# The ring function returns all of the tiles that make up the ring of radius
# 'r' around (x, y).
def ring(x, y, r):
    report = []
    odd = True if y % 2 == 1 else False

    # We start at 0 degrees, which is directly to the right, and then go
    # counter clockwise.
    x += r
    report.append((x, y))
    for i in range(r): # Going up-left
        if not odd: x -= 1
        y -= 1
        report.append((x, y))
        odd = not odd
    for i in range(r): # Going left
        x -= 1
        report.append((x, y))
    for i in range(r): # Going down-left
        if not odd: x -= 1
        y += 1
        odd = not odd
        report.append((x, y))
    for i in range(r): # Going down-right
        if odd: x += 1
        y += 1
        odd = not odd
        report.append((x, y))
    for i in range(r): # Going right
        x += 1
        report.append((x, y))
    for i in range(r): # Going up-right
        if odd: x += 1
        y -= 1
        report.append((x, y))
        odd = not odd

    # Return the report. Note that the 0-degree tile is at the and end
    # of the list.
    return report

# Get the X, Y coordinates of the adjacent tile to x, y in direction d.
#  2 1  Returns None if no such direction.
# 3 @ 0
#  4 5
def direction(x, y, d):
    if d < 0 or d > 5: return None
    else: return ring(x, y, 1)[d]

#
def fov(x, y, r):
    report = [(x, y)]
    for i in range(r+1):
        report += ring(x, y, i)
    return report


# An entity is anything that exists in the world.
class Entity(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.char = name[0]
        self.target = None

    # Attempt to move 1 tile in a direction.
    def move(self, way, world):
        pos = direction(self.x, self.y, way)
        if pos and world.is_free(*pos): self.x, self.y = pos

    # Attempt to move the target.
    def target_move(self, way):
        if not self.target:
            self.target = self.x, self.y
        x, y = self.target
        pos = direction(x, y, way)
        if pos: self.target = pos


# The World is our view into the tiled game world. Entities exist within the
# world an are located at x, y coordinates that represents tiles.
class World(object):
    def __init__(self):
        self.w = 20
        self.h = 20
        self.map = ['.' * self.w] * self.h
        self.player = Entity("Player", 4, 4)
        self.entities = [self.player]
        self.player.char = '@'

        for a in range(self.h):
            for b in range(self.w):
                if random.randint(0, 100) < 10:
                    self.map[a] = self.map[a][:b] + '#' + self.map[a][b+1:]


    # Returns true if a square is free.
    def is_free(self, x, y):
        if self.map[y][x] != '#':
            return True
        return False

    # Draws the world.
    def draw(self):
        graphics.clear()
        my_fov = fov(self.player.x, self.player.y, 3)
        for y in range(self.h):
            odd = True if y % 2 == 1 else False

            for x in range(self.w):
                ax = x * 2 + (1 if odd else 0)

                # For each tile that can be seen, determine what will be drawn
                # there.
                if (x, y) in my_fov:
                    empty = True
                    for e in self.entities:
                        if (e.x, e.y) == (x, y):
                            graphics.draw(ax, y, e.char)
                            empty = False
                    if empty:
                        c = self.map[y][x]
                        graphics.draw(ax, y, c, 'g' if c == '.' else 'y')
                    if self.player.target == (x, y):
                        graphics.draw(ax-1, y, '[')
                        graphics.draw(ax+1, y, ']')

    # TODO: Fix Qwerty and dvorak mode.
    # Handle input. Dvorak mode
    def handle_keys(self, c):
        if c == 't': self.player.move(0, self)
        elif c == 'c': self.player.move(1, self)
        elif c == 'g': self.player.move(2, self)
        elif c == 'd': self.player.move(3, self)
        elif c == 'b': self.player.move(4, self)
        elif c == 'm': self.player.move(5, self)
        elif c == 'i': self.player.target_move(0)
        elif c == 'y': self.player.target_move(1)
        elif c == 'p': self.player.target_move(2)
        elif c == 'e': self.player.target_move(3)
        elif c == 'j': self.player.target_move(4)
        elif c == 'k': self.player.target_move(5)
        elif c == 'u': self.player.target = None
