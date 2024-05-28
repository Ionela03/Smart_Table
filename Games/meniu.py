import pygame
import time
import neopixel
import board
import threading
import json
import os
from snakeLed import SnakeGame
from tetrisLed import TetrisGame
from racketInSpace import RacketGame
from snakeRandObj import SnakeGameWithBorder
from pygame.locals import *

LED_LETTERS = {
    'S': [' ##### ', '#     ', '#     ', '##### ', '     #', '     #', '##### '],
    'O': [' ### ', '#   #', '#   #', '#   #', '#   #', '#   #', ' ### '],
    'T': ['##### ', '  #   ', '  #   ', '  #   ', '  #   ', '  #   ', '  #   '],
    'R': ['#### ', '#   #', '#   #', '#### ', '# #  ', '#  # ', '#   #']
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
        self.options = ['S', 'T', 'R', 'O']
        self.games = {'S': SnakeGame, 'T': TetrisGame, 'R': RacketGame, 'O': SnakeGameWithBorder}
        self.current_game_instance = None
        self.running = True
        pygame.init()
        pygame.display.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        # Start shutdown timer
        self.run_time = self.get_run_time()
        self.start_time = time.time()
        self.remaining_time = self.run_time * 60
        self.timer_thread = threading.Thread(target=self.shutdown_timer)
        self.timer_thread.start()

        # Start thread to monitor runtime changes
        self.monitor_thread = threading.Thread(target=self.monitor_runtime_changes)
        self.monitor_thread.start()

    def signal_handler(self, sig, frame):
        print(f'Signal {sig} received, stopping...')
        self.running = False
        if self.current_game_instance:
            self.current_game_instance.stop()

    def clear_screen(self):
        self.pixels.fill((0, 0, 0))

    def draw_pixel(self, x, y, color):
        mirrored_y = self.PIXEL_Y - 1 - y
        if 0 <= x < self.PIXEL_X and 0 <= mirrored_y < self.PIXEL_Y:
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
        violet = (148, 0, 211)
        for x in range(self.PIXEL_X):
            self.draw_pixel(x, 0, violet)
            self.draw_pixel(x, self.PIXEL_Y - 1, violet)

        for y in range(self.PIXEL_Y):
            self.draw_pixel(0, y, violet)
            self.draw_pixel(self.PIXEL_X - 1, y, violet)

        self.pixels.show()

    def display_menu(self):
        while self.running:
            self.clear_screen()
            self.draw_menu_options()
            self.draw_border()
            self.handle_input()
            self.pixels.show()
            time.sleep(0.1)
        self.clear_screen()  # Oprește LED-urile după oprirea meniului

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

    def handle_input(self):
        pygame.event.pump()
        y_axis = self.joystick.get_axis(1)
        if y_axis < -0.5:
            self.selected_option = (self.selected_option - 1) % len(self.options)
            time.sleep(0.3)
        elif y_axis > 0.5:
            self.selected_option = (self.selected_option + 1) % len(self.options)
            time.sleep(0.3)
        if self.joystick.get_button(0):
            self.run_game(self.options[self.selected_option])

    def run_game(self, game_choice):
        print(f"Starting {game_choice}...")
        self.current_game_instance = self.games[game_choice]()
        game_thread = threading.Thread(target=self.current_game_instance.run)
        game_thread.start()
        while game_thread.is_alive() and self.running:
            elapsed_time = time.time() - self.start_time
            remaining_time = self.run_time * 60 - elapsed_time
            if remaining_time <= 0:
                print("Timer expired during game. Stopping...")
                self.running = False
                self.current_game_instance.stop()
                game_thread.join()
                break
            time.sleep(0.1)
        self.clear_screen()
        self.pixels.show()

    def shutdown_timer(self):
        while self.running:
            elapsed_time = time.time() - self.start_time
            remaining_time = self.run_time * 60 - elapsed_time
            if remaining_time <= 0:
                print("Timer expired. Shutting down...")
                self.clear_screen()
                self.pixels.show()
                self.running = False
                if self.current_game_instance:
                    self.current_game_instance.stop()
                break
            time.sleep(1)

    def monitor_runtime_changes(self):
        while self.running:
            new_runtime = self.get_run_time()
            if new_runtime != self.run_time:
                elapsed_time = time.time() - self.start_time
                print(f"Runtime changed. Adding new runtime {new_runtime} minutes.")
                self.run_time = new_runtime
                self.start_time = time.time()  # Reset start time to now
            time.sleep(10)  # Verifică schimbările la fiecare 10 secunde

    def get_run_time(self):
        try:
            # Obține calea către directorul curent al scriptului
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Merge în folderul `app` din directorul părinte pentru a găsi runtime.json
            runtime_path = os.path.join(current_dir, '..', 'app', 'runtime.json')
            print(f"Reading runtime from: {runtime_path}")
            with open(runtime_path, 'r') as f:
                data = json.load(f)
                print(f"Data read from runtime.json: {data}")
                return data.get('run_time', 0)
        except FileNotFoundError:
            print("runtime.json file not found")
            return 0

if __name__ == '__main__':
    menu = Menu()
    menu.display_menu()
