import random
import time
import board
import neopixel
import pygame
from pygame.locals import *
from gameOverMessage import display_game_over, display_score

class SnakeGame:
    def __init__(self, led_pin=board.D21):  # Folosește obiectul pinului direct
        self.PIXEL_X = 16
        self.PIXEL_Y = 26
        self.LED_BRIGHTNESS = 0.5
        self.pixel_pin = led_pin  # Folosește direct obiectul pinului D21
        self.num_pixels = self.PIXEL_X * self.PIXEL_Y
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=self.LED_BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB)
        self.directions = ['up', 'down', 'left', 'right']
        self.current_direction = 'up'
        self.snake_coords = [{'x': self.PIXEL_X // 2, 'y': self.PIXEL_Y // 2}, {'x': self.PIXEL_X // 2, 'y': self.PIXEL_Y // 2 + 1}]
        self.food = self.add_food()
        self.score = 0
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def draw_pixel(self, x, y, color):
        if 0 <= x < self.PIXEL_X and 0 <= y < self.PIXEL_Y:
            index = x * self.PIXEL_Y + y if x % 2 == 1 else x * self.PIXEL_Y + (self.PIXEL_Y - 1 - y)
            self.pixels[index] = color

    def clear_screen(self):
        self.pixels.fill((0, 0, 0))
        #self.pixels.show()

    def add_food(self):
        while True:
            new_food = {'x': random.randint(0, self.PIXEL_X - 1), 'y': random.randint(0, self.PIXEL_Y - 1)}
            if new_food not in self.snake_coords:
                return new_food

    def update_snake(self):
        head_x = self.snake_coords[0]['x']
        head_y = self.snake_coords[0]['y']
        new_head = {'x': head_x, 'y': head_y}
        if self.current_direction == 'up':
            new_head['y'] = (head_y - 1) % self.PIXEL_Y
        elif self.current_direction == 'down':
            new_head['y'] = (head_y + 1) % self.PIXEL_Y
        elif self.current_direction == 'left':
            new_head['x'] = (head_x - 1) % self.PIXEL_X
        elif self.current_direction == 'right':
            new_head['x'] = (head_x + 1) % self.PIXEL_X

        if new_head in self.snake_coords:
            return False  # Game over condition

        self.snake_coords.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.add_food()
        else:
            self.snake_coords.pop()

        return True
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:  # Verifică axa orizontală
                    if event.value < -0.5:
                        if self.current_direction != 'right':  # Previne mersul înapoi direct
                            self.current_direction = 'left'
                    elif event.value > 0.5:
                        if self.current_direction != 'left':
                            self.current_direction = 'right'
                elif event.axis == 1:  # Verifică axa verticală
                    if event.value < -0.5:
                        if self.current_direction != 'down':
                            self.current_direction = 'up'
                    elif event.value > 0.5:
                        if self.current_direction != 'up':
                            self.current_direction = 'down'

    def draw_snake(self):
        for coord in self.snake_coords:
            self.draw_pixel(coord['x'], coord['y'], (0, 255, 0))

    def draw_food(self):
        self.draw_pixel(self.food['x'], self.food['y'], (255, 0, 0))

    def game_over(self):
        display_game_over()  # Afișează mesajul de game over
        time.sleep(2)
        display_score(self.score)  # Afișează scorul
        time.sleep(2)
        self.running = False  # Oprirea jocului

    def run(self):
        self.running = True
        while self.running:
            self.handle_input()
            self.clear_screen()
            if not self.update_snake():
                self.game_over()
                break  # Ieșire din bucla de joc dacă este game over
            self.draw_snake()
            self.draw_food()
            self.pixels.show()
            time.sleep(0.1)
    

# snake_game = SnakeGame()
# result = snake_game.run()  # Începe jocul și returnează la meniu după terminare
