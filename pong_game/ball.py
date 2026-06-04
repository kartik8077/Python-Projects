from turtle import Turtle

STARTING_SPEED = 0.08   # seconds per frame (lower = faster)
SPEED_INCREMENT = 0.005 # how much faster each hit makes it
MIN_SPEED = 0.02        # cap so it never becomes unplayable

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 15
        self.y_move = 15
        self.move_speed = STARTING_SPEED

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1

    def speed_up(self):
        # Decrease sleep time = increase speed, but never below the cap
        self.move_speed = max(MIN_SPEED, self.move_speed - SPEED_INCREMENT)

    def reset_position(self):
        self.goto(0, 0)
        self.move_speed = STARTING_SPEED  # reset speed on new round
        self.bounce_x()                   # reverse direction toward loser's side   