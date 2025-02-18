import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)  # Fullscreen mode
        self.root.title("Snake Game")
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button

        self.canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_screen()

    def start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(self.root.winfo_screenwidth()//2, self.root.winfo_screenheight()//2,
                                text="Press SPACE to Start",
                                font=("Arial", 30), fill="white")
        self.root.bind("<space>", self.start_game)

    def start_game(self, event):
        self.root.unbind("<space>")
        self.game_running = True

        # Snake and food setup
        self.snake = [(20, 20), (40, 20), (60, 20)]
        self.snake_direction = 'Right'
        self.food = self.place_food()

        self.root.bind("<Up>", lambda event: self.change_direction('Up'))
        self.root.bind("<Down>", lambda event: self.change_direction('Down'))
        self.root.bind("<Left>", lambda event: self.change_direction('Left'))
        self.root.bind("<Right>", lambda event: self.change_direction('Right'))

        self.update_game()

    def place_food(self):
        x = random.randint(0, self.root.winfo_screenwidth()//10 - 1) * 10
        y = random.randint(0, self.root.winfo_screenheight()//10 - 1) * 10
        return x, y

    def change_direction(self, direction):
        opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if direction != opposite[self.snake_direction]:
            self.snake_direction = direction

    def update_game(self):
        if not self.game_running:
            return

        head_x, head_y = self.snake[-1]
        if self.snake_direction == 'Up':
            head_y -= 10
        elif self.snake_direction == 'Down':
            head_y += 10
        elif self.snake_direction == 'Left':
            head_x -= 10
        elif self.snake_direction == 'Right':
            head_x += 10

        new_head = (head_x, head_y)

        # Check wall collision
        if (head_x < 0 or head_x >= self.root.winfo_screenwidth() or
            head_y < 0 or head_y >= self.root.winfo_screenheight()):
            self.game_over()
            return

        self.snake.append(new_head)

        # Check food collision
        if new_head == self.food:
            self.food = self.place_food()  # Place new food
        else:
            self.snake.pop(0)  # Remove tail segment

        self.draw_elements()
        self.root.after(100, self.update_game)

    def draw_elements(self):
        self.canvas.delete("all")
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x+20, y+20, fill="green")
        food_x, food_y = self.food
        self.canvas.create_rectangle(food_x, food_y, food_x+20, food_y+20, fill="red")

    def game_over(self):
        self.game_running = False
        self.canvas.delete("all")
        self.canvas.create_text(self.root.winfo_screenwidth()//2, self.root.winfo_screenheight()//2 - 50,
                                text="Game Over",
                                font=("Arial", 50), fill="red")
        self.canvas.create_text(self.root.winfo_screenwidth()//2, self.root.winfo_screenheight()//2 + 50,
                                text="Press R to Restart",
                                font=("Arial", 30), fill="white")
        self.root.bind("<r>", self.restart_game)

    def restart_game(self, event):
        self.root.unbind("<r>")
        self.start_screen()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
