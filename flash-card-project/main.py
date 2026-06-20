from tkinter import Tk, Canvas, PhotoImage, Button
import pandas
import random
import os

BACKGROUND_COLOR = "#B1DDC6"

# ---------- Data loading ----------
# Use words_to_learn.csv if it exists (i.e. user has already played before
# and we've saved their progress), otherwise fall back to the original list.
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/japanese_words.csv")

to_learn = data.to_dict(orient="records")
current_card = {}
flip_timer = None

def next_card():
    global current_card, flip_timer
    # cancel any pending flip from the previous card
    if flip_timer is not None:
        window.after_cancel(flip_timer)

    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(card_title, text="Japanese Words", fill="black")
    canvas.itemconfig(card_word, text=current_card["Japanese"], fill="black")

    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(canvas_image, image=back_card_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")

def is_known():
    # User knows this word: remove it from the pool so it can't reappear,
    # persist the remaining words, then move on to a new card.
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash Card Project")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 262, font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# wrong button — word stays in the pool, just move to next card
cross = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=cross, highlightthickness=0, command=next_card)
wrong_button.config(bg=BACKGROUND_COLOR, highlightthickness=0)
wrong_button.grid(row=1, column=0)

# check button — word is known, remove it permanently
check = PhotoImage(file="images/right.png")
right_button = Button(image=check, highlightthickness=0, command=is_known)
right_button.config(bg=BACKGROUND_COLOR, highlightthickness=0)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()