from turtle import Turtle

FONT = ("Courier New", 20, "bold")
GAME_OVER_FONT = ("Courier New", 36, "bold")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.hideturtle()
        self.penup()

    def draw_highway(self):
        """Draws static road lines and boundaries to make it look like a highway."""
        drawer = Turtle()
        drawer.hideturtle()
        drawer.speed(0)
        drawer.color("#444444")
        
        # Top and bottom boundaries
        for y in [-250, 250]:
            drawer.penup()
            drawer.goto(-300, y)
            drawer.pendown()
            drawer.goto(300, y)
            
        # Dotted lane markers
        drawer.color("#333333")
        for y in range(-200, 250, 50):
            drawer.penup()
            drawer.goto(-300, y)
            while drawer.xcor() < 300:
                drawer.pendown()
                drawer.forward(20)
                drawer.penup()
                drawer.forward(20)

    def score(self):
        self.clear()  # Prevents text from stacking and blurring
        self.penup()
        self.goto(-270, 260)
        self.color("#00FF66")  # Neon green for level tracking
        self.write(f"LEVEL: {self.level}", align="left", font=FONT)

    def increase_level(self):
        self.level += 1
        self.score()

    def game_over(self):
        # Translucent-effect background box for the Game Over text
        overlay = Turtle()
        overlay.hideturtle()
        overlay.penup()
        overlay.goto(-150, 40)
        overlay.begin_fill()
        overlay.color("#111111")
        for _ in range(2):
            overlay.forward(300)
            overlay.right(90)
            overlay.forward(80)
        overlay.end_fill()

        # Game over text
        self.goto(0, -15)
        self.color("#FF3333")  # Vivid neon red
        self.write("GAME OVER", align="center", font=GAME_OVER_FONT)