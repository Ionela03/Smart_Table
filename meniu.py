import pygame
import time
import neopixel
import board
from snakeLed import SnakeGame
from tetrisLed import TetrisGame
from racketInSpace import RacketGame
from snakeRandObj import SnakeGameWithRandomObstacles
from pygame.locals import *

LED_LETTERS = {
    'S': [' ##### ', '#     ', '#     ', '##### ', '     #', '     #', '##### '],
    'O':
      [
        ' ### ', 
        '#   #', 
        '#   #', 
        '#   #', 
        '#   #', 
        '#   #', 
        ' ### '],
    'T':
      [
          '##### ', 
          '  #   ',
          '  #   ', 
          '  #   ', 
          '  #   ', 
          '  #   ', 
          '  #   '
        ],
    'R':
      [
            '#### ',
            '#   #',
            '#   #',
            '#### ',
            '# #  ',
            '#  # ',
            '#   #',
         ]
}

class Menu:
    def __init__(self):
        self.PIXEL_X = 16  # Width of the matrix
        self.PIXEL_Y = 26  # Height of the matrix
        self.LED_BRIGHTNESS = 0.5
        self.pixel_pin = board.D21
        self.num_pixels = self.PIXEL_X * self.PIXEL_Y
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=self.LED_BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB)
        self.selected_option = 0
        self.options = ['S', 'T','R','O']
        self.games = {'S': SnakeGame, 'T': TetrisGame, 'R': RacketGame, 'O':SnakeGameWithRandomObstacles}
        self.running = True
        pygame.init()
        pygame.display.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def clear_screen(self):
        self.pixels.fill((0, 0, 0))

    def draw_pixel(self, x, y, color):
    # Adjust y to draw from top to bottom
        mirrored_y = self.PIXEL_Y - 1 - y
        if 0 <= x < self.PIXEL_X and 0 <= mirrored_y < self.PIXEL_Y:
            # Calculate index based on current row being even or odd
            if x % 2 == 0:
                index = (x * self.PIXEL_Y) + mirrored_y
            else:
                index = (x * self.PIXEL_Y) + (self.PIXEL_Y - 1 - mirrored_y)
            if index < self.num_pixels:
                self.pixels[index] = color
            else:
                print(f"Index out of range: index={index}")
        else:
            print(f"Coordinates out of range: x={x}, y={mirrored_y}")
    

    def draw_border(self):
        violet = (148, 0, 211)  # RGB for violet
        # Draw top and bottom rows
        for x in range(self.PIXEL_X):
            self.draw_pixel(x, 0, violet)  # Top row
            self.draw_pixel(x, self.PIXEL_Y - 1, violet)  # Bottom row

        # Draw left and right columns
        for y in range(self.PIXEL_Y):
            self.draw_pixel(0, y, violet)  # Left column
            self.draw_pixel(self.PIXEL_X - 1, y, violet)  # Right column

        self.pixels.show()  # Update the display to show the border


    def display_menu(self):
        while self.running:
            self.clear_screen()
            self.draw_menu_options()
            self.draw_border()
            self.handle_input()
            self.pixels.show()
            time.sleep(0.1)

    def draw_menu_options(self):
        # Horizontal start positions
        base_x_s = 2  # Position for 'S'
        base_x_t = 9  # Position for 'T', adjust spacing as needed

        # Vertical start positions
        base_y_top = 4   
        base_y_bottom = base_y_top + len(LED_LETTERS['S']) + 2  

        # Draw 'S' and 'T' on the top row
        color_s = (255, 255, 255) if self.selected_option != 0 else (0, 255, 0)
        self.draw_text('S', base_x_s, base_y_top, color_s)

        color_t = (255, 255, 255) if self.selected_option != 1 else (0, 255, 0)
        self.draw_text('T', base_x_t, base_y_top, color_t)

        # Draw 'R' and 'O' on the bottom row
        color_r = (255, 255, 255) if self.selected_option != 2 else (0, 255, 0)
        self.draw_text('R', base_x_s, base_y_bottom, color_r)

        color_o = (255, 255, 255) if self.selected_option != 3 else (0, 255, 0)
        self.draw_text('O', base_x_t, base_y_bottom, color_o)




    def draw_text(self, text, start_x, start_y, color):
        for letter in text:
            self.draw_letter(letter, start_x, start_y, color)
            start_x += len(LED_LETTERS[letter][0]) + 1  # Adjust space between letters

    def draw_letter(self, letter, start_x, start_y, color):
        if letter not in LED_LETTERS:
            return
        for y, row in enumerate(LED_LETTERS[letter]):
            for x, char in enumerate(row):
                if char == '#':
                    self.draw_pixel(start_x + x, start_y + y, color)

    def handle_input(self):
        pygame.event.pump()  # Update event status
        y_axis = self.joystick.get_axis(1)
        if y_axis < -0.5:  # Up
            self.selected_option = (self.selected_option - 1) % len(self.options)
            time.sleep(0.3)
        elif y_axis > 0.5:  # Down
            self.selected_option = (self.selected_option + 1) % len(self.options)
            time.sleep(0.3)
        if self.joystick.get_button(0):  # Button 0 for selection
            self.run_game(self.options[self.selected_option])
            time.sleep(0.3)

    def run_game(self, game_choice):
        print(f"Starting {game_choice}...")
        game_instance = self.games[game_choice]()
        game_instance.run()
        if game_choice == 'Exit':
            self.running = False

if __name__ == '__main__':
    menu = Menu()
    menu.display_menu()
