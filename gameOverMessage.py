import board
import neopixel
import time

PIXEL_X = 26  # Width of the matrix
PIXEL_Y = 16  # Height of the matrix
LED_BRIGHTNESS = 0.5
score=0

pixel_pin = board.D21  
num_pixels = PIXEL_X * PIXEL_Y
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=LED_BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB)
def draw_pixel(x, y, color):
    if 0 <= x < PIXEL_X and 0 <= y < PIXEL_Y:
        if y % 2 == 0:
            index = (y * PIXEL_X) + x
        else:
            index = (y * PIXEL_X) + (PIXEL_X - 1 - x)
        pixels[index] = color

def display_game_over():
    LETTER_SIZE = {'G': (5, 7), 'A': (5, 7), 'M': (5, 7), 'E': (5, 7), 'O': (5, 7), 'V': (5, 7), 'R': (5, 7)}
    LED_LETTERS = {
        'G': [
            ' ### ',
            '#    ',
            '#    ',
            '#  # ',
            '#   #',
            '#   #',
            ' ### ',
        ],
        'A': [
            '#####',
            '#   #',
            '#   #',
            '#####',
            '#   #',
            '#   #',
            '#   #',
        ],
        'M': [
            '#   #',
            '## ##',
            '# # #',
            '#   #',
            '#   #',
            '#   #',
            '#   #',
        ],
        'E': [
            '#####',
            '#    ',
            '#    ',
            '#####',
            '#    ',
            '#    ',
            '#####',
        ],
        'O': [
            ' ### ',
            '#   #',
            '#   #',
            '#   #',
            '#   #',
            '#   #',
            ' ### ',
        ],
        'V': [
            '#   #',
            '#   #',
            '#   #',
            '#   #',
            ' # # ',
            ' # # ',
            '  #  ',
        ],
        'R': [
            '#### ',
            '#   #',
            '#   #',
            '#### ',
            '#  # ',
            '#   #',
            '#   #',
        ],
    }
    pixels.fill((0, 0, 0))

    
    x_offset = 1  # Start position from the left side of the matrix
    y_offset = 0  # Start position from the top of the matrix
    for letter in "GAME":  
        led_representation = [row for row in LED_LETTERS[letter]] 
        for row_index, row in enumerate(led_representation):
            for col_index, char in enumerate(row):
                if char == '#':
                    draw_pixel(x_offset + col_index, y_offset + row_index, (255, 0,0))
        x_offset += LETTER_SIZE[letter][0] + 1  # Increment x_offset for spacing between letters

    # Display "OVER" on the second line
    x_offset = 1  # Reset x_offset for the start of the second line
    y_offset = 9  # Move down to the second line 
    for letter in "OVER":  
        led_representation = [row for row in LED_LETTERS[letter]] 
        for row_index, row in enumerate(led_representation):
            for col_index, char in enumerate(row):
                if char == '#':
                    draw_pixel(x_offset + col_index, y_offset + row_index, (255, 0,0))
        x_offset += LETTER_SIZE[letter][0] + 1  

    pixels.show()

def display_score(score):
   
    # Definitions for the word "SCORE" and the digits
    LETTER_SIZE = {'S': (4, 7), 'C': (4, 7), 'O': (4, 7), 'R': (4, 7), 'E': (4, 7), '=': (6,3) }
    LED_LETTERS = {
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

        '=': [
            '######',
            '      ',
            '######',
        ],
    }
    
    DIGIT_SIZE = {'1': (5, 7), '2': (5, 7), '3': (5, 7),'4': (5, 7),'5': (5, 7),'6': (5, 7),'7': (5, 7),'8': (5, 7),'0': (5, 7),'9': (5, 7)}
    LED_NUMBERS = {
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

    pixels.fill((0, 0, 0))

    x_offset = 0  # Start position from the left side of the matrix
    y_offset = 0  # Start position from the top of the matrix
    for letter in "SCORE":  
        led_representation = [row for row in LED_LETTERS[letter]] 
        for row_index, row in enumerate(led_representation):
            for col_index, char in enumerate(row):
                if char == '#':
                    draw_pixel(x_offset + col_index, y_offset + row_index, (255, 255, 255))
        x_offset += LETTER_SIZE[letter][0] + 1  # Increment x_offset for spacing between letters

    x_offset = 5  # Reset x_offset for the start of the second line
    y_offset = 10  # Move down to the second line 
    for letter in "=":  
        led_representation = [row for row in LED_LETTERS[letter]]  
        for row_index, row in enumerate(led_representation):
            for col_index, char in enumerate(row):
                if char == '#':
                    draw_pixel(x_offset + col_index, y_offset + row_index, (255, 255, 255))
        x_offset += LETTER_SIZE[letter][0] + 1  # Increment x_offset for spacing between letters

    x_offset = 12 
    y_offset = 8

    score_str = str(score)
    for digit in score_str:
        if digit in LED_NUMBERS:
            led_representation = [row for row in LED_NUMBERS[digit]]
            for row_index, row in enumerate(led_representation):
                for col_index, char in enumerate(row):
                    if char == '#':
                        draw_pixel(x_offset + col_index, y_offset + row_index, (0, 255, 0))
            x_offset += DIGIT_SIZE[digit][0] + 1 
    pixels.show()

display_game_over()