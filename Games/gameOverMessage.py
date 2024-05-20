import board
import neopixel
import time

class LEDDisplay:
    def __init__(self, width=26, height=16, brightness=0.5):
        self.width = width
        self.height = height
        self.brightness = brightness
        self.pixel_pin = board.D21  
        self.num_pixels = self.width * self.height
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=self.brightness, auto_write=False, pixel_order=neopixel.GRB)
    
    def draw_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            if y % 2 == 0:
                index = (y * self.width) + x
            else:
                index = (y * self.width) + (self.width - 1 - x)
            self.pixels[index] = color

    def display_message(self, message, x_offset, y_offset,color):
        for char in message:
            if char.isdigit():
                # Draw numbers
                self.draw_number(int(char), x_offset, y_offset, color)
                x_offset += 6  # Adjust for the width of a digit
            else:
                # Draw letters
                self.draw_letter(char, x_offset, y_offset, color)
                x_offset += 5  # Adjust for the width of a letter
    
    def draw_number(self, number, x_offset, y_offset, color):
        numbers_layout = {
            '0': [
                ' ### ',
                '#   #',
                '#   #',
                '#   #',
                '#   #',
                '#   #',
                ' ### ',
            ],
            '1': [
                '  #  ',
                ' ##  ',
                '# #  ',
                '  #  ',
                '  #  ',
                '  #  ',
                '#####',
            ],
            '2': [
                ' ### ',
                '#   #',
                '    #',
                '   # ',
                '  #  ',
                '#    ',
                '#####',
            ],
            '3': [
                '#####',
                '    #',
                '    #',
                ' ### ',
                '    #',
                '    #',
                '#####',
            ],
            '4': [
                '#   #',
                '#   #',
                '#   #',
                '#####',
                '    #',
                '    #',
                '    #',
            ],
            '5': [
                '#####',
                '#    ',
                '#    ',
                '#### ',
                '    #',
                '#   #',
                ' ### ',
            ],
            '6': [
                ' ### ',
                '#    ',
                '#    ',
                '#### ',
                '#   #',
                '#   #',
                ' ### ',
            ],
            '7': [
                '#####',
                '    #',
                '    #',
                '   # ',
                '  #  ',
                ' #   ',
                '#    ',
            ],
            '8': [
                ' ### ',
                '#   #',
                '#   #',
                ' ### ',
                '#   #',
                '#   #',
                ' ### ',
            ],
            '9': [
                ' ### ',
                '#   #',
                '#   #',
                ' ####',
                '    #',
                '    #',
                ' ### ',
            ]
        }
        layout = numbers_layout[str(number)]
        for row_idx, row in enumerate(layout):
            for col_idx, pixel in enumerate(row):
                if pixel == '#':
                    self.draw_pixel(x_offset + col_idx, y_offset + row_idx, color)

    def draw_letter(self, char, x_offset, y_offset, color):
        letters_layout = {
            'S': [
                '####',
                '#   ',
                '#   ',
                '####',
                '   #',
                '   #',
                '####'
            ],
            'C': [
                ' ###',
                '#   ',
                '#   ',
                '#   ',
                '#   ',
                '#   ',
                ' ###'
            ],
            'O': [
                ' ## ',
                '#  #',
                '#  #',
                '#  #',
                '#  #',
                '#  #',
                ' ## '
            ],
            'R': [
                '### ',
                '#  #',
                '#  #',
                '### ',
                '# # ',
                '#  #',
                '#  #',
            ],
            'E': [
                '####',
                '#   ',
                '#   ',
                '####',
                '#   ',
                '#   ',
                '####',
            ],
            'G': [
                ' ###',
                '#   ',
                '#   ',
                '# ## ',
                '#  #',
                '#  #',
                ' ###',
            ],
            'A': [
                '####',
                '#  #',
                '#  #',
                '####',
                '#  #',
                '#  #',
                '#  #',
            ],
            'M': [
                '#  #', 
                '####', 
                '#  #', 
                '#  #', 
                '#  #', 
                '#  #', 
                '#  #'],

            'V': [
                '#  #',
                '#  #',
                '#  #',
                '#  #',
                '#  #',
                ' ## ',
                ' #  ',
            ],
            '=': [
                '######',
                '      ',
                '######',
            ]

        }
        layout = letters_layout[char]
        for row_idx, row in enumerate(layout):
            for col_idx, pixel in enumerate(row):
                if pixel == '#':
                    self.draw_pixel(x_offset + col_idx, y_offset + row_idx, color)

    def display_game_over(self):
        self.pixels.fill((0, 0, 0))
        self.display_message("GAME",2, 0, (255, 0, 0))
        y_offset=9
        self.display_message("OVER",2 ,y_offset, (255, 0, 0))
        self.pixels.show()

    def display_score(self, score):
        self.pixels.fill((0, 0, 0))
        self.display_message("SCORE", 0, 0, (255, 255, 255))
        self.display_message("=", 1, 11, (255, 255, 255))
        self.display_message(str(score), 8, 9, (0, 255, 0))
        self.pixels.show()
            

# def main():
#     display = LEDDisplay()
#     display.display_score(23) 

# if __name__ == "__main__":
#     main()
