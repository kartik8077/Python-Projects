from turtle import Turtle , Screen

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.goto(0, 250)
        self.score = 0
        self.hideturtle()
        self.color("white")
        self.penup()
        self.write(f"score : {self.score}", align='center', font=("Arial", 20, "normal"))
        self.screen=Screen()


    def increase_score(self):
        self.score += 1
        self.clear()
        self.write(f"score : {self.score}", align='center', font=("Arial", 20, "normal"))

    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", align='center', font=("Arial", 20, "normal"))





