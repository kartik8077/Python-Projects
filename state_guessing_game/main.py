import turtle
import pandas


screen = turtle.Screen()
screen.title("U.S STATES GAME")
image= "D:/VS CODE/GIT HUB/Python-Projects/state_guessing_game/blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

data = pandas.read_csv("Python-Projects\state_guessing_game\50_states.csv")
state_list = data.state.to_list()
x_list = data.x.to_list()
y_list = data.y.to_list()

guessed_state = []

while len(guessed_state) < 50:
    answer_state = screen.textinput(title=f"Guessed state {len(guessed_state)} / 50 ", prompt="what state do you have?")
    if answer_state == "Exit":
        missing_states = []
        for state in state_list:
            if state not in guessed_state:
                missing_states.append(state)
        print(missing_states)
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break

    if answer_state in state_list:
        guessed_state.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data.state == answer_state]
        t.goto(state_data.x.item(),state_data.y.item())
        t.write(answer_state,font=("Arial",15,"bold"))



# screen.exitonclick()
