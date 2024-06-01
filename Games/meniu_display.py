import board
import neopixel
from classic_snake import SnakeGame
from classic_tetris import TetrisGame
from racket_in_space import RacketInSpace
from snake_with_borders import SnakeGameWithBorder
LED_LETTERS = {
    'S': [' ##### ', '#     ', '#     ', '##### ', '     #', '     #', '##### '],
    'O': [' ### ', '#   #', '#   #', '#   #', '#   #', '#   #', ' ### '],
    'T': ['##### ', '  #   ', '  #   ', '  #   ', '  #   ', '  #   ', '  #   '],
    'R': ['#### ', '#   #', '#   #', '#### ', '# #  ', '#  # ', '#   #']
}
class MenuDisplay:
    def __init__(self):
        self.width= 16
        self.height= 26
        self.LED_BRIGHTNESS = 0.5
        self.pixel_pin=board.D21
        self.num_pixels=self.width*self.height
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=self.LED_BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB)
        self.selected_option = 0
        self.options = ['S', 'T', 'R', 'O']
        self.games = {'S': SnakeGame, 'T': TetrisGame, 'R': RacketInSpace, 'O': SnakeGameWithBorder}


    def draw_border(self):
        violet = (148, 0, 211)
        for x in range(self.width):
            self.draw_pixel(x, 0, violet)
            self.draw_pixel(x, self.height- 1, violet)

        for y in range(self.height):
            self.draw_pixel(0, y, violet)
            self.draw_pixel(self.width - 1, y, violet)

        self.pixels.show()

    def draw_menu_options(self):
        base_x_s = 2
        base_x_t = 9

        base_y_top = 4
        base_y_bottom = base_y_top + len(LED_LETTERS['S']) + 2

        color_s = (255, 255, 255) if self.selected_option != 0 else (0, 255, 0)
        self.draw_text('S', base_x_s, base_y_top, color_s)

        color_t = (255, 255, 255) if self.selected_option != 1 else (0, 255, 0)
        self.draw_text('T', base_x_t, base_y_top, color_t)

        color_r = (255, 255, 255) if self.selected_option != 2 else (0, 255, 0)
        self.draw_text('R', base_x_s, base_y_bottom, color_r)

        color_o = (255, 255, 255) if self.selected_option != 3 else (0, 255, 0)
        self.draw_text('O', base_x_t, base_y_bottom, color_o)

    def draw_text(self, text, start_x, start_y, color):
        for letter in text:
            self.draw_letter(letter, start_x, start_y, color)
            start_x += len(LED_LETTERS[letter][0]) + 1

    def draw_letter(self, letter, start_x, start_y, color):
        if letter not in LED_LETTERS:
            return
        for y, row in enumerate(LED_LETTERS[letter]):
            for x, char in enumerate(row):
                if char == '#':
                    self.draw_pixel(start_x + x, start_y + y, color)

    def draw_pixel(self, x, y, color):
        mirrored_y = self.height - 1 - y
        if 0 <= x < self.width and 0 <= mirrored_y < self.height:
            if x % 2 == 0:
                index = (x * self.height) + mirrored_y
            else:
                index = (x * self.height) + (self.height - 1 - mirrored_y)
            if index < self.num_pixels:
                self.pixels[index] = color
