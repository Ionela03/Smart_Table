import board
import neopixel
import pygame
import random
import time
from gameOverMessage import display_game_over

# Settings for the LED matrix
PIN = board.D21
WIDTH = 26
HEIGHT = 16
NUM_PIXELS = WIDTH * HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Configure NeoPixel
pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, brightness=0.5, auto_write=False, pixel_order=neopixel.GRB)
objects = []
bullets = []

ship_width = 3  # Initial width of the ship
hits = 0  # Count of red LEDs hit

def clear():
    pixels.fill(BLACK)

def update_display():
    pixels.show()

def set_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        index = (y * WIDTH) + (x if y % 2 == 0 else WIDTH - 1 - x)
        pixels[index] = color

def draw_ship(ship_x, ship_y, ship_width):
    for x in range(ship_x, ship_x + ship_width):
        set_pixel(x, ship_y, WHITE)

def draw_bullets():
    for bullet in bullets:
        set_pixel(bullet[0], bullet[1], GREEN)

def draw_objects():
    for obj in objects:
        set_pixel(obj[0], obj[1], RED)

def move_ship(direction, ship_x, ship_width):
    max_position = WIDTH - ship_width
    if direction == "left" and ship_x > 0:
        ship_x -= 1
    elif direction == "right" and ship_x < max_position:
        ship_x += 1
    return ship_x

def move_objects():
    global objects
    new_objects = []
    for obj in objects:
        obj[1] += 1
        if obj[1] < HEIGHT:
            new_objects.append(obj)
    objects = new_objects

def move_bullets():
    global bullets
    new_bullets = []
    for bullet in bullets:
        bullet[1] -= 1
        if bullet[1] >= 0:
            new_bullets.append(bullet)
    bullets = new_bullets

def check_collisions(ship_x, ship_y):
    global objects, bullets, hits, ship_width
    remaining_objects = []
    for obj in objects:
        if obj[1] == ship_y and ship_x <= obj[0] < ship_x + ship_width:
            display_game_over()
            pygame.quit()
            return False
        hit = False
        for bullet in bullets:
            if bullet[0] == obj[0] and bullet[1] == obj[1]:
                set_pixel(obj[0], obj[1], BLACK)
                bullets.remove(bullet)
                hit = True
                hits += 1
                break
        if not hit:
            remaining_objects.append(obj)

    objects = remaining_objects

    # Increase ship size and modify firing mechanism after 5 hits
    if hits >= 5 and ship_width == 3:
        ship_width = 5  # Increase ship width

    return True

def generate_objects():
    if random.random() < 0.1:
        x = random.randint(0, WIDTH - 1)
        objects.append([x, 0])

def main():
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    ship_x = WIDTH // 2 - 1
    ship_y = HEIGHT - 2

    running = True
    while running:
        clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -0.5:
                        ship_x = move_ship("left", ship_x, ship_width)
                    elif event.value > 0.5:
                        ship_x = move_ship("right", ship_x, ship_width)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 4 or event.button == 5:
                    # Fire bullets from new positions when ship is enlarged
                    bullet_positions = range(ship_x, ship_x + ship_width)
                    for pos in bullet_positions:
                        bullets.append([pos, ship_y - 1])

        generate_objects()
        move_objects()
        move_bullets()
        if not check_collisions(ship_x, ship_y):
            break

        draw_ship(ship_x, ship_y, ship_width)
        draw_objects()
        draw_bullets()
        update_display()

        time.sleep(0.1)

    pygame.quit()

if __name__ == "__main__":
    main()
