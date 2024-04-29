import random
import time
import board
import neopixel
import pygame
from pygame.locals import *
from gameOverMessage import display_game_over, display_score

PIXEL_X = 16  # Width of the matrix
PIXEL_Y = 26  # Height of the matrix
LED_BRIGHTNESS = 0.5

pixel_pin = board.D21  
num_pixels = PIXEL_X * PIXEL_Y
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=LED_BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB)

# Snake game constants
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD = 0  # Index of the snake's head

# Initialize the snake
snake_coords = [{'x': PIXEL_X // 2, 'y': PIXEL_Y // 2}, {'x': PIXEL_X // 2, 'y': PIXEL_Y // 2 + 1}]
direction = UP
last_direction = direction
food = {'x': random.randint(0, PIXEL_X - 1), 'y': random.randint(0, PIXEL_Y - 1)}  # Initialize food
score = 0  # Initialize score

# Initialize Pygame for the controller
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

def draw_pixel(x, y, color):
    if 0 <= x < PIXEL_X and 0 <= y < PIXEL_Y:
        if x % 2 == 1:
            pixels[x * PIXEL_Y + y] = color
        else:
            pixels[x * PIXEL_Y + (PIXEL_Y - 1 - y)] = color

def clear_screen():
    pixels.fill((0, 0, 0))

def add_food():
    global food, score
    while True:
        new_food = {'x': random.randint(0, PIXEL_X - 1), 'y': random.randint(0, PIXEL_Y - 1)}
        if new_food not in snake_coords:
            food = new_food
            break

def update_snake():
    global last_direction, score, running
    head_x = snake_coords[HEAD]['x']
    head_y = snake_coords[HEAD]['y']

    if last_direction == UP:
        new_head = {'x': head_x, 'y': (head_y - 1) % PIXEL_Y}
    elif last_direction == DOWN:
        new_head = {'x': head_x, 'y': (head_y + 1) % PIXEL_Y}
    elif last_direction == LEFT:
        new_head = {'x': (head_x - 1) % PIXEL_X, 'y': head_y}
    elif last_direction == RIGHT:
        new_head = {'x': (head_x + 1) % PIXEL_X, 'y': head_y}

    if new_head in snake_coords:
        running = False  # Stop the game if collision detected
        return

    snake_coords.insert(0, new_head)
    
    if snake_coords[HEAD] == food:
        score += 1  # Increment score
        add_food()  # Add new food because snake just ate it
    else:
        snake_coords.pop()

def draw_snake():
    for coord in snake_coords:
        draw_pixel(coord['x'], coord['y'], (0, 255, 0))

def draw_food():
    draw_pixel(food['x'], food['y'], (255, 0, 0))

def game_over():

    display_game_over()
    time.sleep(2)
    display_score(score)


def game_loop():
    global direction, last_direction, running
    running = True
    add_food()
    while running:
        clear_screen()
        update_snake()
        draw_snake()
        draw_food()
        pixels.show()
        time.sleep(0.1)

        for event in pygame.event.get():
            if event.type == JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -0.5 and last_direction != RIGHT:
                        direction = LEFT
                    elif event.value > 0.5 and last_direction != LEFT:
                        direction = RIGHT
                elif event.axis == 1:
                    if event.value < -0.5 and last_direction != DOWN:
                        direction = UP
                    elif event.value > 0.5 and last_direction != UP:
                        direction = DOWN

            elif event.type is pygame.QUIT:
                running = False

        # Only update last_direction if the new direction is not opposite to current
        if ((last_direction == UP and direction != DOWN) or
            (last_direction == DOWN and direction != UP) or
            (last_direction == LEFT and direction != RIGHT) or
            (last_direction == RIGHT and direction != LEFT)):
            last_direction = direction

    game_over()

if __name__ == '__main__':
    game_loop()
