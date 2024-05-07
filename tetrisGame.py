import time
import board as pyboard
import neopixel
import random
import pygame
from pygame.locals import *
from gameOverMessage import display_game_over

# Configurația matricei LED
PIXEL_X = 26  # Lățimea matricei (schimbat pentru a se potrivi cu dimensiunile matricei fizice)
PIXEL_Y = 16  # Înălțimea matricei
LED_BRIGHTNESS=0.5

pixel_pin = pyboard.D21
num_pixels = PIXEL_X * PIXEL_Y
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=neopixel.GRB)

# Setări pentru Tetris
BOARDWIDTH = 26  # Lățimea tablei de joc în blocuri
BOARDHEIGHT = 16 # Înălțimea tablei de joc în blocuri
BLANK = None

# Initialize Pygame for the controller
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Culori
COLORS = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 165, 0), (0, 0, 0)]

# Formele pieselor Tetris
S_SHAPE_TEMPLATE = [['....',
                     '....',
                     '..OO',
                     '.OO.'],
                    ['....',
                     '..O.',
                     '..OO',
                     '...O']]

Z_SHAPE_TEMPLATE = [['....',
                     '....',
                     '.OO.',
                     '..OO'],
                    ['....',
                     '..O.',
                     '.OO.',
                     '.O..']]

I_SHAPE_TEMPLATE = [['..O.',
                     '..O.',
                     '..O.',
                     '..O.'],
                    ['....',
                     'OOOO',
                     '....',
                     '....']]

O_SHAPE_TEMPLATE = [['....',
                     '.OO.',
                     '.OO.',
                     '....']]

J_SHAPE_TEMPLATE = [['....',
                     '.O..',
                     '.OOO',
                     '....'],
                    ['....',
                     '..OO',
                     '..O.',
                     '..O.'],
                    ['....',
                     '....',
                     '.OOO',
                     '...O'],
                    ['....',
                     '..O.',
                     '..O.',
                     '.OO.']]

L_SHAPE_TEMPLATE = [['....',
                     '...O',
                     '.OOO',
                     '....'],
                    ['....',
                     '..O.',
                     '..O.',
                     '..OO'],
                    ['....',
                     '....',
                     '.OOO',
                     '.O..'],
                    ['....',
                     '.OO.',
                     '..O.',
                     '..O.']]

T_SHAPE_TEMPLATE = [['....',
                     '..O.',
                     '.OOO',
                     '....'],
                    ['....',
                     '..O.',
                     '..OO',
                     '..O.'],
                    ['....',
                     '....',
                     '.OOO',
                     '..O.'],
                    ['....',
                     '..O.',
                     '.OO.',
                     '..O.']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

TEMPLATEWIDTH = 4
TEMPLATEHEIGHT = 4

game_board = [[BLANK for _ in range(BOARDHEIGHT)] for _ in range(BOARDWIDTH)]


def game_over():
    display_game_over()

def drawPixel(x, y, color):
    """ Draw a single pixel on the LED matrix. """
    if 0 <= x < BOARDWIDTH and 0 <= y < BOARDHEIGHT:
        index = y * PIXEL_X + (x if y % 2 == 0 else PIXEL_X - 1 - x) 
        pixels[index] = color


def getBlankBoard():
    return [[BLANK for _ in range(BOARDHEIGHT)] for _ in range(BOARDWIDTH)]

def drawPiece(piece):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] == 'O':
                ledX = piece['x'] + x
                ledY = piece['y'] + y
                if 0 <= ledX < BOARDWIDTH and 0 <= ledY < BOARDHEIGHT:
                    drawPixel(ledX, ledY, COLORS[piece['color']])


def getNewPiece():
    shape = random.choice(list(PIECES.keys()))
    new_piece = {
        'shape': shape,
        'rotation': random.randint(0, len(PIECES[shape]) - 1),
        'x': (BOARDWIDTH // 2) - (TEMPLATEWIDTH // 2),
        'y': 0,
        'color': random.randint(0, len(COLORS)-2)
    }
    if not isValidPosition(game_board, new_piece):
        return None  
    return new_piece


def isValidPosition(board, piece, adjX=0, adjY=0):
    piece_template = PIECES[piece['shape']][piece['rotation']]
    template_height = len(piece_template)
    template_width = len(piece_template[0]) if template_height > 0 else 0

    for y in range(template_height):
        for x in range(template_width):
            template_cell = piece_template[y][x]
            if template_cell == 'O':
                boardX = x + piece['x'] + adjX
                boardY = y + piece['y'] + adjY
                if not (0 <= boardX < BOARDWIDTH and 0 <= boardY < BOARDHEIGHT):
                    return False  # Part is out of board bounds
                if board[boardX][boardY] != BLANK:
                    return False  # Part collides with others
    return True


def addToBoard(board, piece):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] == 'O':
                board[piece['x'] + x][piece['y'] + y] = piece['color']

def drawBoard(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            color = COLORS[board[x][y]] if board[x][y] != BLANK else (0, 0, 0)
            drawPixel(x, y, color)

def clearPixels():
    pixels.fill((0, 0, 0))

def movePiece(piece, board, adjX=0, adjY=0):
    temp_x = piece['x'] + adjX
    temp_y = piece['y'] + adjY

    # Verifică fiecare celulă a piesei înainte de a muta
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] == 'O':
                new_x = temp_x + x
                new_y = temp_y + y
                if not (0 <= new_x < BOARDWIDTH and 0 <= new_y < BOARDHEIGHT):
                    return False  # Prevenirea ieșirii din limite
                if board[new_x][new_y] != BLANK:
                    return False  # Prevenirea coliziunii cu alte piese
    # Dacă toate testele sunt trecute, actualizează poziția piesei
    piece['x'] = temp_x
    piece['y'] = temp_y
    return True


def removeCompleteLines(board):
    # Identificăm liniile complete
    completeLines = [y for y in range(BOARDHEIGHT) if all(board[x][y] != BLANK for x in range(BOARDWIDTH))]
    # Eliminăm liniile complete
    for y in completeLines:
        for upY in range(y, 0, -1):
            for x in range(BOARDWIDTH):
                board[x][upY] = board[x][upY - 1]
        for x in range(BOARDWIDTH):
            board[x][0] = BLANK  # Setăm prima linie la BLANK după ce o linie este mutată în jos


def game_loop():
    fallingPiece = getNewPiece()
    lastFallTime = time.time()
    running = True
    while running:
        clearPixels()
        drawBoard(game_board)
        drawPiece(fallingPiece)
        pixels.show()
        time.sleep(0.1)

        for event in pygame.event.get():
            if event.type == JOYAXISMOTION:
                handle_joystick_motion(event, fallingPiece, game_board)
            elif event.type == JOYBUTTONDOWN:
                if event.button == 4:  # Rotirea piesei la apăsarea butonului 4
                    rotate_piece(fallingPiece, game_board)
            elif event.type == pygame.QUIT:
                running = False

        # Mișcarea automată în jos a piesei
        if time.time() - lastFallTime > 1:
            if not movePiece(fallingPiece, game_board, adjY=1):
                addToBoard(game_board, fallingPiece)
                removeCompleteLines(game_board)  # Verificăm și eliminăm liniile complete după adăugarea piesei pe tablă
                fallingPiece = getNewPiece() 
                if fallingPiece is None:  
                    game_over()
                    break
            lastFallTime = time.time()


def handle_joystick_motion(event, piece, board):
    if event.axis == 0:  # Left/Right movement
        if event.value < -0.5:  # Left direction
            if not movePiece(piece, board, adjX=-1):
                print("Nu se poate muta la stânga.")
        elif event.value > 0.5:  # Right direction
            if not movePiece(piece, board, adjX=1):
                print("Nu se poate muta la dreapta.")
    elif event.axis == 1 and event.value > 0.5:  # Downward movement
        if not movePiece(piece, board, adjY=1):
            print("Nu se poate muta în jos.")

def rotate_piece(piece, board):
    old_rotation = piece['rotation']
    piece['rotation'] = (piece['rotation'] + 1) % len(PIECES[piece['shape']])
    if not isValidPosition(board, piece, 0, 0):
        piece['rotation'] = old_rotation  # Revenire la rotația anterioară dacă rotația nu este validă

if __name__ == '__main__':
    game_loop()