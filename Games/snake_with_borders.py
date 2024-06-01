import random
import time
from classic_snake import SnakeGame

class SnakeGameWithBorder(SnakeGame):
    def __init__(self):
        super().__init__()

    def draw_border(self):
        violet = (148, 0, 211)
        for x in range(self.width):
            self.draw_pixel(x, 0, violet)
            self.draw_pixel(x, self.height - 1, violet)

        for y in range(self.height):
            self.draw_pixel(0, y, violet)
            self.draw_pixel(self.width - 1, y, violet)

        self.pixels.show()

    def add_food(self):
        while True:
            self.food = {'x': random.randint(1, self.width - 2), 'y': random.randint(1, self.height - 2)}
            if self.food not in self.snake_coords and not self.is_food_on_border():
                return self.food

    def is_food_on_border(self):
        # Check if the food is on the border
        return self.food['x'] == 0 or self.food['x'] == self.width - 1 or self.food['y'] == 0 or self.food['y'] == self.height - 1

    def update_snake(self):
        if not super().update_snake():
            return False
        new_head = self.snake_coords[0]
        
        # Check if the snake hits the border
        if new_head['x'] == 0 or new_head['x'] == self.width - 1 or new_head['y'] == 0 or new_head['y'] == self.height - 1:
            return False  # Game over if hits the border

        return True

    def draw_elements(self):
        super().draw_elements()
        self.draw_border()

# snake_game = SnakeGameWithBorder()
# result = snake_game.run()
