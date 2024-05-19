import time
import board
import neopixel
import pygame
from pygame.locals import *
from abc import ABC, abstractmethod
from gameOverMessage import display_game_over

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
        display_game_over() 
        time.sleep(2)
    
    @abstractmethod
    def run(self):
        #Method that should be implemented by subclasses
        pass
    @abstractmethod
    def handle_input(self):
        #Method that should be implemented by subclasses
        pass
