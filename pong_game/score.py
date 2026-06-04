from turtle import Turtle

class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.left_score  = 0
        self.right_score = 0
        self.draw()

    def draw(self):
        self.clear()
        # Left score
        self.goto(-150, 200)
        self.write(self.left_score, align="center", font=("Courier", 60, "bold"))
        # Colon separator
        self.goto(0, 200)
        self.write(":", align="center", font=("Courier", 60, "bold"))
        # Right score
        self.goto(150, 200)
        self.write(self.right_score, align="center", font=("Courier", 60, "bold"))

    def increment_left(self):
        self.left_score += 1
        self.draw()

    def increment_right(self):
        self.right_score += 1
        self.draw()