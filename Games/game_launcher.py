import pygame
import time
import threading
import json
import os
from base_game import BaseGame
from meniu_display import MenuDisplay


class GameLauncher(BaseGame, MenuDisplay):
    def __init__(self):
        BaseGame.__init__(self)
        MenuDisplay.__init__(self)
        self.current_game_instance = None
        self.running = True

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


    def display_menu(self):
        while self.running:
            self.clear_screen()
            self.draw_menu_options()
            self.draw_border()
            self.handle_input()
            self.pixels.show()
            time.sleep(0.1)
        self.clear_screen()  

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.JOYAXISMOTION:
                self.process_axis_motion(event)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.process_button_down(event)

    def process_axis_motion(self, event):
        if event.axis == 1:  # Y-axis motion
            if event.value < -0.5:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.value > 0.5:
                self.selected_option = (self.selected_option + 1) % len(self.options)

    def process_button_down(self, event):
        if event.button == 0:  # Assuming button 0 is for selection
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
            time.sleep(10)  # Verifica schimbarile la fiecare 10 secunde

    def get_run_time(self):
        try:
            # Obtine calea catre directorul curent al scriptului
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Merge in folderul `app` din directorul parinte pentru a gasi runtime.json
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
    menu = GameLauncher()
    menu.display_menu()
