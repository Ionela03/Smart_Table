import pygame
import random
import time
from gameOverMessage import display_score
from base_game import BaseGame

class RacketGame(BaseGame):
    def __init__(self):
        super().__init__()
        self.ship = {'x': self.width // 2 - 1, 'width': 3, 'y': self.height - 2}
        self.objects = []
        self.bullets = []
        self.hits = 0

    def draw_ship(self):
        for x in range(self.ship['x'], self.ship['x'] + self.ship['width']):
            self.draw_pixel(x, self.ship['y'], (255, 255, 255))

    def draw_bullets(self):
        for bullet in self.bullets:
            self.draw_pixel(bullet[0], bullet[1], (0, 255, 0))

    def draw_objects(self):
        for obj in self.objects:
            self.draw_pixel(obj[0], obj[1], (255, 0, 0))

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

    def game_over(self):
        super().game_over() 
        display_score(self.hits)  
        time.sleep(2)
        self.running = False

    def check_collisions(self):
        remaining_objects = []
        for obj in self.objects:
            if obj[1] == self.ship['y'] and self.ship['x'] <= obj[0] < self.ship['x'] + self.ship['width']:
                self.game_over()
                return False
            hit = False
            for bullet in self.bullets:
                if bullet[0] == obj[0] and bullet[1] == obj[1]:
                    self.draw_pixel(obj[0], obj[1], (0, 0, 0))
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
                self.running = False
            elif event.type == pygame.JOYAXISMOTION:
                self.process_joy_axis_motion(event)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.process_joy_button_down(event)

    def process_joy_axis_motion(self, event):
        if event.axis == 0:
            if event.value < -0.5:
                self.move_ship("left")
            elif event.value > 0.5:
                self.move_ship("right")

    def process_joy_button_down(self, event):
        if event.button in (4, 5):  # 4 and 5 are for shooting
            bullet_positions = range(self.ship['x'], self.ship['x'] + self.ship['width'])
            for pos in bullet_positions:
                self.bullets.append([pos, self.ship['y'] - 1])
    
    def draw_elements(self):
        self.draw_ship()
        self.draw_objects()
        self.draw_bullets()

    def handle_objects(self):
        self.generate_objects()
        self.move_objects()
        self.move_bullets()

    def run(self):
        self.running = True
        while self.running:
            self.clear_screen()
            self.handle_input()
            self.handle_objects()
            if not self.check_collisions():
                break
            self.draw_elements()
            self.update_display()
            time.sleep(0.1)


# if __name__ == "__main__":
#     game = RacketGame()
#     game.run()
