from turtle import Turtle

SCREEN_TOP    =  250
SCREEN_BOTTOM = -250
MOVE_DISTANCE =  25

class Paddle(Turtle):
    def __init__(self, x_position, y_position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(x_position, y_position)

    def move_up(self):
        if self.ycor() < SCREEN_TOP:       # prevent paddle leaving screen
            self.goto(self.xcor(), self.ycor() + MOVE_DISTANCE)

    def move_down(self):
        if self.ycor() > SCREEN_BOTTOM:    # prevent paddle leaving screen
            self.goto(self.xcor(), self.ycor() - MOVE_DISTANCE)