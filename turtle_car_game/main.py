import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

# Screen Setup
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("#222222")  # Sleek dark theme
screen.title("Turtle Crossing Arcade")
screen.tracer(0)

# Initialize Objects
score_board = Scoreboard()
score_board.draw_highway()  # Draw the road before the game starts
new_turtle = Player()
car = CarManager()

# Key Bindings
screen.listen()
screen.onkeypress(fun=new_turtle.move, key="Up")

game_is_on = True

while game_is_on:
    car.generate()
    car.car_move()
    score_board.score()

    # Detection with car
    for c in car.cars:
        if c.distance(new_turtle) < 22:  # Slightly adjusted for visual accuracy
            game_is_on = False
            score_board.game_over()

    # Detection of successful crossing
    if new_turtle.player_is_at_finish():
        new_turtle.go_to()
        car.increase_speed()
        score_board.increase_level()

    time.sleep(0.1)
    screen.update()

screen.exitonclick()