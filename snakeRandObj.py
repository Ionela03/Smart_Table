import random
import time
from snakeLed import SnakeGame

class SnakeGameWithRandomObstacles(SnakeGame):
    def __init__(self):
        super().__init__()
        self.obstacles = self.generate_obstacles()
 

    def generate_obstacles(self):
        obstacles = []
        while len(obstacles) < 5:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            length = random.randint(3, 7)  # Ensure the length is between 3 and 7
            direction = random.choice(['up', 'down', 'left', 'right'])
            temp_obstacle = []
            valid_obstacle = True

            for i in range(length):
                new_x = x + (i if direction == 'right' else -i if direction == 'left' else 0)
                new_y = y + (i if direction == 'down' else -i if direction == 'up' else 0)
                new_x %= self.width
                new_y %= self.height
                new_pos = {'x': new_x, 'y': new_y}

                # Check if the position conflicts with the snake, food, or overlaps any existing obstacles
                if new_pos in self.snake_coords or new_pos in [o for sublist in obstacles for o in sublist] or new_pos == self.food:
                    valid_obstacle = False
                    break
                temp_obstacle.append(new_pos)

            if valid_obstacle:
                obstacles.append(temp_obstacle)  # Append the whole obstacle as a sublist

        return obstacles



    def update_snake(self):
        if not super().update_snake():
            return False 
        new_head = self.snake_coords[0]
        if any(new_head in obstacle for obstacle in self.obstacles):
            return False  # Game over if hits an obstacle

        return True

    def draw_obstacle(self):
        for obstacle in self.obstacles:
            for coord in obstacle:
                self.draw_pixel(coord['x'], coord['y'], (0, 0, 255))


    def draw_elements(self):
        super().draw_elements() 
        self.draw_obstacle()  

# snake_game = SnakeGameWithRandomObstacles()
# result = snake_game.run() 