"""
Program Name: ICS4U Final Summative
Programmer: Alan Khaev
Date: June 27, 2022
Input: The user uses their mouse to control units on a battlefield, in hopes of taking all of the other team's units in a turn based system
Processing: The user can move or attack, and can claim pieces which the program computes and removes the defeated units from the game
Output: A grid-based game of chess, with different units and turn based combat. User must move all of their units before their turn can end
"""

import math as m
import random as r
import pygame
import time as t

# Import different characters
from character import Pawn, Rook, Bishop

# Create the grid
from Map import *
grid = Grid()

# Dimensions of the game window
width = 900
height = 600

# Used for the grid system - increments
tilewidth = width / grid.cols
tileheight = height / grid.rows

# Colors
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
blue = 0, 0, 255
green = 0, 255, 0

# Basic pygame initializations
pygame.init()
pygame.mixer.pre_init(44100, 16, 4, 4096)
pygame.mixer.init()
fps = pygame.time.Clock()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battle of Alania")

# Images
titlejpg = pygame.image.load("Fire Emblem/Assets/titlescreen.jpg")
titlejpg = pygame.transform.scale(titlejpg, (width, height))
cursorpng = pygame.image.load("Fire Emblem/Assets/fecursor.png").convert_alpha()
mappng = pygame.image.load("Fire Emblem/Assets/mappng.png").convert_alpha()
gamemap = pygame.transform.scale(mappng, (width, height))

# Sound effects + music
selectwav = pygame.mixer.Sound("Fire Emblem/Assets/select.wav")
cursorwav = pygame.mixer.Sound("Fire Emblem/Assets/cursor.wav")
critwav = pygame.mixer.Sound("Fire Emblem/Assets/crit.wav")
deathwav = pygame.mixer.Sound("Fire Emblem/Assets/death.wav")
fanfare = pygame.mixer.Sound("Fire Emblem/Assets/fanfare.wav")

themesong = "Fire Emblem/Assets/themesong.mp3"
bgm1 = "Fire Emblem/Assets/bgm1.mp3"
bgm2 = "Fire Emblem/Assets/bgm2.mp3"
bgm3 = "Fire Emblem/Assets/bgm3.mp3"
bgms = [bgm1, bgm2, bgm3]   # Randomly play one of three songs for the background
bgm = r.choice(bgms)

pygame.mixer.music.load(themesong)

# Function for playing music
def playMusic(repeat=-1, start=0, volume=0.3):
    pygame.mixer.music.play(repeat, start=start)
    pygame.mixer.music.set_volume(volume)
playMusic()


font = pygame.font.Font("freesansbold.ttf", 60)


titlescreen = True
while titlescreen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            titlescreen = False
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            titlescreen = False


    window.blit(titlejpg, (0, 0))

    text = font.render(str("Fire Emblem - Battle of Alania"), True, blue, True)
    textrect = text.get_rect()
    textrect.center = (width / 2, 150)
    window.blit(text, textrect)

    text = font.render(str("Press any Key to Start"), True, green)
    textrect = text.get_rect()
    textrect.center = (width / 2, 400)
    window.blit(text, textrect)

    pygame.display.update()
    fps.tick(60)


font = pygame.font.Font("freesansbold.ttf", 40)

# Create the teams
BluePawn1 = Pawn("Blue")
BluePawn2 = Pawn("Blue")
BluePawn3 = Pawn("Blue")

BlueRook1 = Rook("Blue")
BlueRook2 = Rook("Blue")

BlueBishop1 = Bishop("Blue")
BlueBishop2 = Bishop("Blue")


RedPawn1 = Pawn("Red")
RedPawn2 = Pawn("Red")
RedPawn3 = Pawn("Red")

RedRook1 = Rook("Red")
RedRook2 = Rook("Red")

RedBishop1 = Bishop("Red")
RedBishop2 = Bishop("Red")

# Create the teams
blueTeam = [BluePawn1, BluePawn2, BluePawn3, BlueRook1, BlueRook2, BlueBishop1, BlueBishop2]
redTeam = [RedPawn1, RedPawn2, RedPawn3, RedRook1, RedRook2, RedBishop1, RedBishop2]

# Get list of all characters
chars = blueTeam + redTeam

# Ensures characters can't spawn on top of each other, and each character has a unique spawn
def checkOverlap(chars):
    poslist = [char.pos for char in chars]
    for pos in poslist:
        if poslist.count(pos) > 1:
            print("Overlap Detected")
            return True
    return False

overlap = True
while overlap:
    for char in chars:
        char.startPos()
    overlap = checkOverlap(chars)


# Take cursor png, and draw at cursor position
def drawCursor(cursorpos):
    gridx = cursorpos[0] * width/grid.cols
    gridy = cursorpos[1] * height/grid.rows

    cursor = pygame.transform.scale(cursorpng, (width/grid.cols + 20, height/grid.rows + 20))
    window.blit(cursor, (gridx - 10, gridy - 10))


# Get info for where the cursor is, and return information about the position
def getInfo(cursor):
    for char in chars:
        if str(cursor) == str(char.pos):
            return [str(char.side + " " + char.unittype), str(char.side).lower()]

    if cursor in waters:
        return ["Water", "black"]
    elif cursor in bridges:
        return ["Bridge", "black"]
    elif cursor in walls:
        return ["Wall", "black"]
    elif cursor in forests:
        return ["Forest", "black"]
    else:
        return ["Plains", "black"]

# Display the information in the bottom right corner, with color        
def infoBox(info, color):
    text = font.render(str(info), True, color)
    textrect = text.get_rect()
    textrect.center = (width - 120, height - 50)
    window.blit(text, textrect)     #trash

# Display who's turn it is in the bottom left
def turnBox(info):
    if turn % 2 == 0:
        text = font.render("Red Turn", True, black)
    else:
        text = font.render("Blue Turn", True, black)

    textrect = text.get_rect()
    textrect.center = (120, height - 50)
    window.blit(text, textrect) 

# When a winner is decided, transition to win screen, play music, and display winner
def winScreen(win):
    pygame.mixer.music.stop()
    fanfare.play()

    if win == "Blue":
        pygame.draw.rect(window, blue, (0, 0, width, height))
    else:
        pygame.draw.rect(window, red, (0, 0, width, height))

    wins = str(win) + " Wins!"
    text = font.render(wins, True, black)
    textrect = text.get_rect()
    textrect.center = (width/2, height/2)
    window.blit(text, textrect)
    pygame.display.update()

    t.sleep(8)

    pygame.draw.rect(window, white, (0, 0, width, height))
    text = "(Sorry for the sudden music cutoff)"
    text = font.render(text, True, black)
    textrect = text.get_rect()
    textrect.center = (width/2, height/2)
    window.blit(text, textrect)
    pygame.display.update()

# Play Background Music
pygame.mixer.music.load(bgm)
playMusic()

# In-game variables
selecting = False   # Character selection state
turn = 1    # Turn count - used for deciding who moves
pos2 = None # Cursor position
winner = None   # Winner of the game

# Count how many units have moved to decide when turn ends
redmoved = 0
bluemoved = 0

running = True  # Main loop
while running:

    # Get mouse position
    mousepos = pygame.mouse.get_pos()
    cursor = [m.floor(mousepos[0] / width * grid.cols), m.floor(mousepos[1] / height * grid.rows)]
    pos1 = cursor

    # If position changes, play sound effect
    if pos1 != pos2:
        cursorwav.play()
    pos2 = pos1

    # List of all character positions
    poslist = [char.pos for char in chars]

    for event in pygame.event.get():
        
        # If user quits, exit game
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # If mouse is pressed...
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Get position on the grid... [0, 0], [14, 2]...
            clickpos = [int(mousepos[0] // tilewidth), int(mousepos[1] // tileheight)]
            
            for char in chars:

                # Select the character
                if char.pos == clickpos and char.moved == False and not selecting and char.turn == turn % 2:
                    char.selected = True
                    char.moveRange()
                    selecting = True
                    selectwav.play()
                    break
                
                if char.selected and selecting:
                    
                    # If the move is illegal or on itself
                    if clickpos == char.pos or clickpos not in char.moverange:
                        char.selected = False
                        selecting = False
                        break

                    # If the move is on open terrain and it's legal
                    if clickpos in char.moverange:
                        valid = True
                        if clickpos in poslist:
                            for defending in chars:

                                # If unit is attacking other side, and can defeat them
                                if defending.pos == clickpos and defending.side != char.side:
                                    defending.isAlive = False
                                    critwav.play()
                                    deathwav.play()
                                    chars.remove(defending)

                                    # Remove defeated character from their team list
                                    if defending.side == "Blue":
                                        blueTeam.remove(defending)
                                    else:
                                        redTeam.remove(defending)
                                    break

                                # If the move is on itself or on the same side
                                elif defending.pos == clickpos and defending.side == char.side:
                                    valid = False
                                    char.selected = False
                                    selecting = False
                                    break

                        # If invalid, stop selecting
                        if not valid:
                            break

                        # If valid, move the character to desired location
                        char.pos = clickpos
                        char.moved = True
                        char.selected = False
                        selecting = False

                        # Used in knowing when to end the turn
                        if char.side == "Blue":
                            bluemoved += 1
                        elif char.side == "Red":
                            redmoved += 1

                        break

        
        # Debugging controls
        # if event.type == pygame.KEYDOWN:
        #     for char in chars:
        #         char.moved = False
        #     turn += 1
        #     winner = "Blue"
        #     running = False

    # Display map on screen
    window.blit(gamemap, (0, 0))

    # Display each character
    for char in chars:        
        char.show(window, tilewidth, tileheight, char.img)

    # Get info to be displayed in the bottom right
    info = getInfo(cursor)
    infoBox(info[0], info[1])
    turnBox(turn)
    drawCursor(cursor)

    # If all units on a side have been moved, end the turn and move on to the next
    if len(redTeam) == redmoved or len(blueTeam) == bluemoved:
        redmoved = 0
        bluemoved = 0
        for char in chars:
            char.moved = False
        turn += 1

    # Refresh the screen
    pygame.display.update()
    fps.tick(60)

    # If all units are gone from a side, declare the winner
    if len(redTeam) == 0:
        winner = "Blue"
        break
        
    elif len(blueTeam) == 0:
        winner = "Red"
        break

# Show the winner
endscreen = True
winScreen(winner)
while endscreen:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            endscreen = False
            pygame.quit()