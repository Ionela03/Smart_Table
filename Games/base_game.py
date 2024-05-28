import time
import board
import neopixel
import pygame
from pygame.locals import *
from abc import ABC, abstractmethod
from gameOverMessage import LEDDisplay

class BaseGame:
    def __init__ (self):
        self.width= 16
        self.height= 26
        self.LED_BRIGHTNESS = 0.5
        self.pixel_pin=board.D21
        self.num_pixels=self.width*self.height
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=self.LED_BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB)
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def clear_screen(self):
        self.pixels.fill((0, 0, 0))

    def draw_pixel(self, x, y, color):
        mirrored_y = self.height - 1 - y
        if 0 <= x < self.width and 0 <= mirrored_y < self.height:
            if x % 2 == 0:
                index = (x * self.height) + mirrored_y
            else:
                index = (x * self.height) + (self.height - 1 - mirrored_y)
            if index < self.num_pixels:
                self.pixels[index] = color
    
    def game_over(self):
        led_display = LEDDisplay()
        led_display.display_game_over()
        time.sleep(2)

    def update_display(self):
        self.pixels.show()

    @abstractmethod
    def run(self):
        #Method that should be implemented by subclasses
        pass
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.JOYAXISMOTION:
                self.process_axis_motion(event)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.process_button_down(event)

    @abstractmethod
    def process_axis_motion(self, event):
        pass

    @abstractmethod
    def process_button_down(self, event):
        pass

    def stop(self):
        self.running = False
