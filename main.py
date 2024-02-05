from tkinter import *
from tkinter import messagebox
import random
import os
import sys


# constant variable
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = '#00FF00'
FOOD_COLOR = '#FF0000'
BACKGROUND_COLOR = '#000000'
PLAY_BUTTON = '#00FFFF'


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)


class Food:
    def __init__(self):

        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE)) - 1) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE)) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        # create the food(sphere):
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags='food')


def next_turn(snake, food):

    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIZE

    elif direction == 'down':
        y += SPACE_SIZE

    elif direction == 'left':
        x -= SPACE_SIZE

    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    # checking overlapping Snake and Food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text=f'Score:{score}')

        # delete the food object with tag
        canvas.delete('food')

        # create another food object
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # checking the collisions(snake cant get out the box)
    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):

    global direction

    # control the Snake Movement
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    if new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    if new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    if new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    # getting the head of snake
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # checking snake eat self:
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def restart_game():
    # reopen the game again
    os.execl(sys.executable, sys.executable, *sys.argv)


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text='GAME OVER', fill='red', tags='game over')

    user_response = messagebox.askyesno("Game Over", "Do you want to restart the game?")
    if user_response:
        restart_game()
    else:
        print("Game ended. Thanks for playing!")


window = Tk()
window.title('Snake Game')
window.resizable(False, False)


score = 0
direction = 'down'

label = Label(window, text='Score:{}'.format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR,  height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


# center the window on screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()


x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f'{window_width}x{window_height}+{x}+{y}')

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Up>', lambda event: change_direction('up'))


snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
