import board
import neopixel
import pygame
import random
import time
from gameOverMessage import display_game_over, display_score

class RacketGame:
    def __init__(self):
        self.width = 16
        self.height = 26
        self.pin = board.D21
        self.num_pixels = self.width * self.height
        self.pixels = neopixel.NeoPixel(self.pin, self.num_pixels, brightness=0.5, auto_write=False, pixel_order=neopixel.GRB)
        self.ship = {'x': self.width // 2 - 1, 'width': 3, 'y': self.height - 2}
        self.objects = []
        self.bullets = []
        self.hits = 0
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def clear(self):
        self.pixels.fill((0, 0, 0))

    def update_display(self):
        self.pixels.show()

    def set_pixel(self, x, y, color):
        mirrored_y = self.height - 1 - y
        if 0 <= x < self.width and 0 <= mirrored_y < self.height:
            if x % 2 == 0:
                index = (x * self.height) + mirrored_y
            else:
                index = (x * self.height) + (self.height - 1 - mirrored_y)
            if index < self.num_pixels:
                self.pixels[index] = color

    def draw_ship(self):
        for x in range(self.ship['x'], self.ship['x'] + self.ship['width']):
            self.set_pixel(x, self.ship['y'], (255, 255, 255))

    def draw_bullets(self):
        for bullet in self.bullets:
            self.set_pixel(bullet[0], bullet[1], (0, 255, 0))

    def draw_objects(self):
        for obj in self.objects:
            self.set_pixel(obj[0], obj[1], (255, 0, 0))

    def move_ship(self, direction):
        max_position = self.width - self.ship['width']
        if direction == "left" and self.ship['x'] > 0:
            self.ship['x'] -= 1
        elif direction == "right" and self.ship['x'] < max_position:
            self.ship['x'] += 1

    def move_objects(self):
        new_objects = []
        for obj in self.objects:
            obj[1] += 1
            if obj[1] < self.height:
                new_objects.append(obj)
        self.objects = new_objects

    def move_bullets(self):
        new_bullets = []
        for bullet in self.bullets:
            bullet[1] -= 1
            if bullet[1] >= 0:
                new_bullets.append(bullet)
        self.bullets = new_bullets

    def check_collisions(self):
        remaining_objects = []
        for obj in self.objects:
            if obj[1] == self.ship['y'] and self.ship['x'] <= obj[0] < self.ship['x'] + self.ship['width']:
                display_game_over()
                time.sleep(2)
                display_score(self.hits)  # Display score upon game over
                return False
            hit = False
            for bullet in self.bullets:
                if bullet[0] == obj[0] and bullet[1] == obj[1]:
                    self.set_pixel(obj[0], obj[1], (0, 0, 0))
                    self.bullets.remove(bullet)
                    hit = True
                    self.hits += 1
                    break
            if not hit:
                remaining_objects.append(obj)
        self.objects = remaining_objects
        if self.hits >= 5 and self.ship['width'] == 3:
            self.ship['width'] = 5
        return True

    def generate_objects(self):
        if random.random() < 0.1:
            x = random.randint(0, self.width - 1)
            self.objects.append([x, 0])  

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -0.5:
                        self.move_ship("left")
                    elif event.value > 0.5:
                        self.move_ship("right")
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button in (4, 5):
                    bullet_positions = range(self.ship['x'], self.ship['x'] + self.ship['width'])
                    for pos in bullet_positions:
                        self.bullets.append([pos, self.ship['y'] - 1])

    def run(self):
        self.running = True
        while self.running:
            self.clear()
            self.handle_input()
            self.generate_objects()
            self.move_objects()
            self.move_bullets()
            if not self.check_collisions():
                break

            self.draw_ship()
            self.draw_objects()
            self.draw_bullets()
            self.update_display()

            time.sleep(0.1)


# if __name__ == "__main__":
#     game = RacketGame()
#     game.run()
