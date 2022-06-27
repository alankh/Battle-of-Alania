import pygame
import random
import Map

blue = (0, 0, 255)
red = (255, 0, 0)

"""
Unit superclass -> Subunits subclass. Subunits are Pawns, Rooks, and Bishops
Each unit shares a lot of attributes, but subunits have their own unique movement ranges,
    ways to move, and sprites to be displayed on the board. These attributes are defined
    in their own respective subclasses
"""

class Unit:
    def __init__(self, pos, side, mov, unittype):
        self.pos = pos  # Position
        self.side = side    # Affiliation (Blue, Red)
        self.isAlive = True # Vitality state
        self.selected = False   # Selection state
        self.moved = False  # Has moved or no
        self.mov = mov  # Movement range - how far they can go
        self.unittype = unittype    # Type - Pawn, Rook, Bishop

        if self.side == "Blue": # Blues move on odd turns (1, 3, 5...)
            self.turn = 1
        if self.side == "Red":  # Reds move on even turns (2, 4, 6...)
            self.turn = 0

    def startPos(self): # Shuffle the start positions, but make them spawn in their own respective halves of the map - red on top, blues on the bottom
        if self.side == "Blue":
            position = [random.randint(0, 14), random.randint(5, 9)]
            while position in Map.waters or position in Map.walls:
                position = [random.randint(0, 14), random.randint(5, 9)]

        elif self.side == "Red":
            position = [random.randint(0, 14), random.randint(0, 4)]
            while position in Map.waters or position in Map.walls:
                position = [random.randint(0, 14), random.randint(0, 4)]

        self.pos = position

    # Show the unit, and the movement range when selected
    def show(self, window, tilewidth, tileheight, png):
        img = pygame.transform.scale(png, (tilewidth - 10, tileheight - 10))

        if self.selected:
            
            if self.side == "Red":
                for moves in self.moverange:
                    s = pygame.Surface((tilewidth, tileheight))
                    s.set_alpha(128)
                    s.fill(red)
                    window.blit(s, (moves[0] * tilewidth, moves[1] * tileheight))

            elif self.side == "Blue":
                for moves in self.moverange:
                    s = pygame.Surface((tilewidth, tileheight))
                    s.set_alpha(100)
                    s.fill(blue)
                    window.blit(s, (moves[0] * tilewidth, moves[1] * tileheight))
                    
        # Display unit on top
        window.blit(img, (self.pos[0] * tilewidth + 5, self.pos[1] * tileheight + 5))


# Pawn subclass - simple unit, simple all directional 2 range movement
class Pawn(Unit):
    def __init__(self, side):
        super().__init__([0, 0], side, 2, "Pawn")
        if self.side == "Blue":
            self.img = pygame.image.load("Fire Emblem/Assets/Blue/bluepawn.png").convert_alpha()
        elif self.side == "Red":
            self.img = pygame.image.load("Fire Emblem/Assets/Red/redpawn.png").convert_alpha()

    # Moverange - all possible directions
    def moveRange(self):
        moverange = []
        for i in range(-self.mov, self.mov + 1):
            for j in range(-self.mov, self.mov + 1):
                if abs(i) + abs(j) <= self.mov:
                    moverange.append([i + self.pos[0], j + self.pos[1]])
        
        # Check to see if the moves are on illegal tiles
        legalmoves = []
        for move in moverange:
            if move not in Map.waters and move not in Map.walls:
                legalmoves.append(move)

        moverange = legalmoves

        self.moverange = moverange


# Rook subclass - One direction only, in a straight line
class Rook(Unit):
    def __init__(self, side):
        super().__init__([0, 0], side, 6, "Rook")
        if self.side == "Blue":
            self.img = pygame.image.load("Fire Emblem/Assets/Blue/bluerook.png").convert_alpha()
        elif self.side == "Red":
            self.img = pygame.image.load("Fire Emblem/Assets/Red/redrook.png").convert_alpha()

    # Straight up/down, and left/right
    def moveRange(self):
        moverange = []
        for i in range(-self.mov, self.mov + 1):
            moverange.append([i + self.pos[0], self.pos[1]])

        for j in range(-self.mov, self.mov + 1):
            moverange.append([self.pos[0], j + self.pos[1]])
        
        legalmoves = []
        for move in moverange:
            if move not in Map.waters and move not in Map.walls:
                legalmoves.append(move)

        moverange = legalmoves

        self.moverange = moverange


# Bishop subclass - Only diagonal movement
class Bishop(Unit):
    def __init__(self, side):
        super().__init__([0, 0], side, 5, "Bishop")
        if self.side == "Blue":
            self.img = pygame.image.load("Fire Emblem/Assets/Blue/bluebishop.png")
        if self.side == "Red":
            self.img = pygame.image.load("Fire Emblem/Assets/Red/redbishop.png")

    def moveRange(self):
        moverange = []
        for i in range(-self.mov, self.mov + 1):
            for j in range(-self.mov, self.mov + 1):
                if abs(i) == abs(j):
                    moverange.append([self.pos[0] + i, self.pos[1] + j])
        
        legalmoves = []
        for move in moverange:
            if move not in Map.waters and move not in Map.walls:
                legalmoves.append(move)

        moverange = legalmoves

        self.moverange = moverange