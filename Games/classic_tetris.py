import time
import random
import pygame
from pygame.locals import *
from base_game import BaseGame

class TetrisGame(BaseGame):
    def __init__(self):
        super().__init__()
        self.COLORS = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 165, 0)]
        self.PIECES = {
            'S': [['....', '....', '..OO', '.OO.'], ['....', '..O.', '..OO', '...O']],
            'Z': [['....', '....', '.OO.', '..OO'], ['....', '..O.', '.OO.', '.O..']],
            'I': [['..O.', '..O.', '..O.', '..O.'], ['....', 'OOOO', '....', '....']],
            'O': [['....', '.OO.', '.OO.', '....']],
            'J': [['....', '.O..', '.OOO', '....'], ['....', '..OO', '..O.', '..O.'], ['....', '....', '.OOO', '...O'], ['....', '..O.', '..O.', '.OO.']],
            'L': [['....', '...O', '.OOO', '....'], ['....', '..O.', '..O.', '..OO'], ['....', '....', '.OOO', '.O..'], ['....', '.OO.', '..O.', '..O.']],
            'T': [['....', '..O.', '.OOO', '....'], ['....', '..O.', '..OO', '..O.'], ['....', '....', '.OOO', '..O.'], ['....', '..O.', '.OO.', '..O.']]
        }
        self.TEMPLATEWIDTH=4
        self.TEMPLATEHEIGHT=4
        self.game_board = [[None for _ in range(self.height)] for _ in range(self.width)]
        self.BLANK = None
        self.current_piece=None
        self.score = 0

    def get_new_piece(self):
        shape = random.choice(list(self.PIECES.keys()))
        new_piece = {
            'shape': shape,
            'rotation': random.randint(0, len(self.PIECES[shape]) - 1),
            'x': int(self.width  / 2 - self.TEMPLATEWIDTH / 2),
            'y': 0,
            'color': random.randint(0, len(self.COLORS) - 1)
        }
        if not self.is_valid_position(self.game_board, new_piece):
            return None
        return new_piece
    
    def add_to_board(self, board, piece):
        for x in range(self.TEMPLATEWIDTH):
            for y in range(self.TEMPLATEHEIGHT):
                 if self.PIECES[piece['shape']][piece['rotation']][y][x] == 'O':
                    board[piece['x'] + x][piece['y'] + y] = piece['color']


    def is_valid_position(self, board, piece, adjX=0, adjY=0):
        for x in range(self.TEMPLATEWIDTH):
            for y in range(self.TEMPLATEHEIGHT):
                if self.PIECES[piece['shape']][piece['rotation']][y][x] == 'O':
                    boardX = piece['x'] + x + adjX
                    boardY = piece['y'] + y + adjY
                    if not (0 <= boardX < self.width and 0 <= boardY < self.height ):
                        return False
                    if board[boardX][boardY] != self.BLANK:
                        return False
        return True
    
    def draw_board(self):
        for x in range(self.width ):
            for y in range(self.height):
                pixel_color = self.COLORS[self.game_board[x][y]] if self.game_board[x][y] != self.BLANK else (0, 0, 0)
                self.draw_pixel(x, y, pixel_color)

    def draw_piece(self, piece):
        for x in range(self.TEMPLATEWIDTH):
            for y in range(self.TEMPLATEHEIGHT):
                if self.PIECES[piece['shape']][piece['rotation']][y][x] == 'O':
                    ledX = piece['x'] + x
                    ledY = piece['y'] + y
                    if 0 <= ledX < self.width and 0 <= ledY < self.height:
                        self.draw_pixel(ledX, ledY, self.COLORS[piece['color']])


    def move_piece(self, piece, adjX=0, adjY=0):
        new_x = piece['x'] + adjX
        new_y = piece['y'] + adjY
        if self.is_valid_position(self.game_board, piece, adjX, adjY):
            piece['x'] = new_x
            piece['y'] = new_y
            return True
        return False  

    def rotate_piece(self, piece):
        original_rotation = piece['rotation']
        piece['rotation'] = (piece['rotation'] + 1) % len(self.PIECES[piece['shape']])
        if not self.is_valid_position(self.game_board, piece):
            piece['rotation'] = original_rotation

    def remove_complete_lines(self):
        complete_lines = []
        for y in range(self.height):
            if all(self.game_board[x][y] is not self.BLANK for x in range(self.width)):
                complete_lines.append(y)

        for y in complete_lines:
            for move_down_y in range(y, 0, -1):
                for x in range(self.width):
                    self.game_board[x][move_down_y] = self.game_board[x][move_down_y - 1]
            for x in range(self.width ):
                self.game_board[x][0] = self.BLANK

        return len(complete_lines)  

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.JOYAXISMOTION:
                self.process_axis_motion(event)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.process_button_down(event)

    def process_axis_motion(self, event):
        if not self.current_piece:
            return
        if event.axis == 0:
            if event.value < -0.5:
                self.move_piece(self.current_piece, adjX=-1)
            elif event.value > 0.5:
                self.move_piece(self.current_piece, adjX=1)
        elif event.axis == 1 and event.value > 0.5:
            self.move_piece(self.current_piece, adjY=1)

    def process_button_down(self, event):
        if not self.current_piece:
            return
        if event.button == 4:
            self.rotate_piece(self.current_piece)
            
    def run(self):
        self.running = True
        self.current_piece = self.get_new_piece()
        last_fall_time = time.time()
        while self.running:
            if time.time() - last_fall_time > 1:
                if not self.move_piece(self.current_piece, adjY=1):
                    self.add_to_board(self.game_board, self.current_piece)
                    lines_cleared = self.remove_complete_lines()
                    self.score += lines_cleared  
                    self.current_piece = self.get_new_piece()
                    if self.current_piece is None:
                        self.game_over()
                        break
                last_fall_time = time.time()
            self.clear_screen()
            self.draw_board()
            self.draw_piece(self.current_piece)
            self.pixels.show()
            self.handle_input()
            time.sleep(0.1)

# tetris_game = TetrisGame()
# result = tetris_game.run()