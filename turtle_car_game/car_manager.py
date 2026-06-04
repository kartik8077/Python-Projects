import random
from turtle import Turtle

# Brighter neon colors that pop beautifully against the dark background
COLORS = ["#FF0055", "#00F0FF", "#FFCC00", "#FF6600", "#9933FF", "#33FF33"]
STARTING_MOVE_DISTANCE = 20
MOVE_INCREMENT = 5  # Reduced slightly so the difficulty scales smoothly

class CarManager:
    def __init__(self):
        self.cars = []
        self.car_speed = STARTING_MOVE_DISTANCE

    def generate(self):
        # Balanced generation logic so cars spread out evenly
        num = random.randint(1, 6)
        if num == 1:
            new_car = Turtle()
            new_car.shape("square")
            new_car.color(random.choice(COLORS))
            new_car.penup()
            # Stretched to look like a realistic arcade vehicle
            new_car.shapesize(stretch_wid=1, stretch_len=2.5) 
            y_cord = random.randint(-220, 220)  # Constrained within the highway lines
            new_car.goto(310, y_cord)
            self.cars.append(new_car)

    def car_move(self):
        for car in self.cars:
            car.backward(self.car_speed)
            
        # Clean up off-screen cars to optimize performance
        self.cars = [car for car in self.cars if car.xcor() > -320]

    def increase_speed(self):
        self.car_speed += MOVE_INCREMENT