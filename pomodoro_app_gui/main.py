from tkinter import *
import math

# -------------------------- CONSTANTS ------------------------------- #
BG_COLOR = "#2C3E50"        # Dark slate background
CARD_COLOR = "#34495E"      # Slightly lighter card
RED = "#E74C3C"             # Work session color
GREEN = "#2ECC71"           # Success/break color
PINK = "#FF6B9D"            # Short break color
BLUE = "#3498DB"            # Long break color
TEXT_COLOR = "#ECF0F1"       # Light text
ACCENT = "#F39C12"          # Accent for buttons
FONT_NAME = "Helvetica"

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Pomodoro", fg=TEXT_COLOR)
    check_marks.config(text="")
    progress_bar.coords(progress_rect, 0, 0, 0, 10)
    reps = 0
    start_button.config(state=NORMAL)

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Long Break 🌴", fg=BLUE)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Short Break ☕", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Focus Time 🍅", fg=RED)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec_str = f"0{count_sec}"
    else:
        count_sec_str = str(count_sec)

    if count_min < 10:
        count_min_str = f"0{count_min}"
    else:
        count_min_str = str(count_min)

    canvas.itemconfig(timer_text, text=f"{count_min_str}:{count_sec_str}")

    # Update progress bar
    if reps % 2 != 0 and reps % 8 != 0:
        total = WORK_MIN * 60
    elif reps % 8 == 0:
        total = LONG_BREAK_MIN * 60
    else:
        total = SHORT_BREAK_MIN * 60

    progress = (total - count) / total
    bar_width = 300
    progress_bar.coords(progress_rect, 0, 0, bar_width * progress, 10)

    global timer
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions_completed = math.floor(reps / 2)
        for _ in range(work_sessions_completed):
            marks += "🍅"
        check_marks.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.configure(padx=40, pady=40, bg=BG_COLOR)
window.resizable(False, False)

# Main title
header_label = Label(
    window,
    text="🍅 POMODORO TIMER",
    font=(FONT_NAME, 24, "bold"),
    fg=ACCENT,
    bg=BG_COLOR
)
header_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

# Card frame to hold the timer visuals
card = Frame(window, bg=CARD_COLOR, padx=30, pady=30,
              highlightbackground=ACCENT, highlightthickness=2)
card.grid(row=1, column=0, columnspan=3, pady=10)

# Session status label
title_label = Label(
    card,
    text="Ready to Focus?",
    font=(FONT_NAME, 22, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR
)
title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

# Canvas for timer circle
canvas = Canvas(card, width=250, height=250, bg=CARD_COLOR, highlightthickness=0)

# Draw a decorative circle ring
canvas.create_oval(15, 15, 235, 235, outline=ACCENT, width=6)
canvas.create_oval(25, 25, 225, 225, outline=RED, width=2)

timer_text = canvas.create_text(
    125, 125,
    text="00:00",
    fill=TEXT_COLOR,
    font=(FONT_NAME, 42, "bold")
)
canvas.grid(row=1, column=0, columnspan=3, pady=10)

# Progress bar
progress_bar_bg = Canvas(card, width=300, height=10, bg="#1A1A2E", highlightthickness=0)
progress_bar_bg.grid(row=2, column=0, columnspan=3, pady=(10, 5))
progress_bar = progress_bar_bg
progress_rect = progress_bar.create_rectangle(0, 0, 0, 10, fill=ACCENT, outline="")

# Checkmarks label (completed sessions)
check_marks = Label(
    card,
    text="",
    font=(FONT_NAME, 16),
    fg=GREEN,
    bg=CARD_COLOR
)
check_marks.grid(row=3, column=0, columnspan=3, pady=(10, 0))

# ---------------------------- BUTTONS ------------------------------- #
button_frame = Frame(window, bg=BG_COLOR)
button_frame.grid(row=2, column=0, columnspan=3, pady=20)

start_button = Button(
    button_frame,
    text="▶  START",
    command=start_timer,
    font=(FONT_NAME, 12, "bold"),
    bg=GREEN,
    fg="white",
    activebackground="#27AE60",
    relief=FLAT,
    padx=20,
    pady=10,
    cursor="hand2",
    borderwidth=0
)
start_button.grid(row=0, column=0, padx=10)

reset_button = Button(
    button_frame,
    text="⟲  RESET",
    command=reset_timer,
    font=(FONT_NAME, 12, "bold"),
    bg=RED,
    fg="white",
    activebackground="#C0392B",
    relief=FLAT,
    padx=20,
    pady=10,
    cursor="hand2",
    borderwidth=0
)
reset_button.grid(row=0, column=1, padx=10)

# Footer
footer_label = Label(
    window,
    text="Stay focused. Take breaks. Repeat. 💪",
    font=(FONT_NAME, 10, "italic"),
    fg="#7F8C8D",
    bg=BG_COLOR
)
footer_label.grid(row=3, column=0, columnspan=3, pady=(10, 0))

window.mainloop()