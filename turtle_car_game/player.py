from turtle import Turtle

STARTING_POSITION = (0, -270)
MOVE_DISTANCE = 15
FINISH_LINE_Y = 255

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("#FFFFFF")  # Crisp white player character stands out perfectly
        self.penup()
        self.go_to()
        self.setheading(90)

    def move(self):
        self.forward(MOVE_DISTANCE)

    def player_is_at_finish(self):
        return self.ycor() > FINISH_LINE_Y

    def go_to(self):
        self.goto(STARTING_POSITION)