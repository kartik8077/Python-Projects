from turtle import Screen, Turtle
from paddle import Paddle
from score import Score
from ball import Ball
import time

screen = Screen()
screen.tracer(0)
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("PONG")

# Draw center dashed line
divider = Turtle()
divider.color("white")
divider.hideturtle()
divider.penup()
divider.goto(0, 300)
divider.setheading(270)
for _ in range(30):
    divider.pendown()
    divider.forward(10)
    divider.penup()
    divider.forward(10)

right_paddle = Paddle(x_position=350, y_position=0)
left_paddle  = Paddle(x_position=-350, y_position=0)
ball         = Ball()
score_of     = Score()

screen.listen()
screen.onkeypress(fun=right_paddle.move_up,   key="Up")
screen.onkeypress(fun=right_paddle.move_down, key="Down")
screen.onkeypress(fun=left_paddle.move_up,    key="w")
screen.onkeypress(fun=left_paddle.move_down,  key="s")

game_on = True

while game_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Wall bounce (top / bottom)
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Paddle collision — right
    if ball.distance(right_paddle) < 50 and ball.xcor() > 320:
        ball.bounce_x()
        ball.speed_up()

    # Paddle collision — left
    if ball.distance(left_paddle) < 50 and ball.xcor() < -320:
        ball.bounce_x()
        ball.speed_up()

    # Ball out of bounds — right wall
    if ball.xcor() > 400:
        score_of.increment_left()
        ball.reset_position()

    # Ball out of bounds — left wall
    elif ball.xcor() < -400:
        score_of.increment_right()
        ball.reset_position()

screen.exitonclick()