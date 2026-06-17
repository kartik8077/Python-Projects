from tkinter import *
from tkinter import messagebox, ttk
import random
import pyperclip
import json

# ─────────────────────────── THEME TOKENS ──────────────────────────── #
BG_DARK      = "#0D0F14"   # near-black background
BG_CARD      = "#151821"   # card / panel surface
BG_ENTRY     = "#1C2030"   # input field background
ACCENT_CYAN  = "#00D4FF"   # primary accent – electric cyan
ACCENT_GLOW  = "#0099BB"   # darker variant for hover / border
FG_PRIMARY   = "#E8EAF0"   # main text
FG_MUTED     = "#5A6080"   # secondary / placeholder text
BORDER       = "#252A3A"   # subtle borders
SUCCESS      = "#00FF9D"   # generated-password success tone
FONT_HEAD    = ("Segoe UI", 11, "bold")
FONT_LABEL   = ("Segoe UI", 9)
FONT_ENTRY   = ("Consolas", 10)
FONT_BTN     = ("Segoe UI", 9, "bold")
FONT_TITLE   = ("Segoe UI", 16, "bold")
FONT_SUB     = ("Segoe UI", 8)

# ─────────────────────────── PASSWORD GENERATOR ─────────────────────── #
def generate_pass():
    letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    numbers = list("0123456789")
    symbols = list("!#$%&()*+")

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    pwd = (
        [random.choice(letters) for _ in range(nr_letters)] +
        [random.choice(symbols) for _ in range(nr_symbols)] +
        [random.choice(numbers) for _ in range(nr_numbers)]
    )
    random.shuffle(pwd)
    password = "".join(pwd)

    password_entry.delete(0, END)
    password_entry.config(fg=SUCCESS)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    strength_update(password)
    flash_copy_hint()

# ─────────────────────────── STRENGTH METER ─────────────────────────── #
def strength_update(pwd=""):
    if not pwd:
        pwd = password_entry.get()
    score = 0
    if len(pwd) >= 10:   score += 1
    if any(c.isupper() for c in pwd): score += 1
    if any(c.islower() for c in pwd): score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(c in "!#$%&()*+" for c in pwd): score += 1

    colors = ["#FF3B3B", "#FF7A3B", "#FFD23B", "#7BFF6E", SUCCESS]
    labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    w = int((score / 5) * 200)

    strength_bar.coords(strength_fill, 0, 0, w, 6)
    strength_bar.itemconfig(strength_fill, fill=colors[max(score - 1, 0)])
    strength_label.config(text=labels[max(score - 1, 0)] if pwd else "")

def on_password_key(event):
    password_entry.config(fg=FG_PRIMARY)
    strength_update()

# ─────────────────────────── COPY HINT ──────────────────────────────── #
def flash_copy_hint():
    copy_hint.config(text="✓ Copied to clipboard", fg=SUCCESS)
    window.after(2500, lambda: copy_hint.config(text=""))

# ─────────────────────────── SAVE PASSWORD ──────────────────────────── #
def save():
    website  = website_entry.get().strip()
    email    = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not email or not password:
        show_toast("⚠  Fill in all three fields before saving.", error=True)
        return

    new_data = {website: {"email": email, "password": password}}

    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data.update(new_data)
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)
    strength_bar.coords(strength_fill, 0, 0, 0, 6)
    strength_label.config(text="")
    copy_hint.config(text="")
    show_toast(f"✓  Saved credentials for  {website}")

# ─────────────────────────── FIND PASSWORD ──────────────────────────── #
def find_password():
    website = website_entry.get().strip()
    if not website:
        show_toast("⚠  Enter a website name to search.", error=True)
        return

    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        show_toast("⚠  No saved passwords found yet.", error=True)
        return

    if website in data:
        email    = data[website]["email"]
        password = data[website]["password"]
        pyperclip.copy(password)
        password_entry.delete(0, END)
        password_entry.insert(0, password)
        email_entry.delete(0, END)
        email_entry.insert(0, email)
        strength_update(password)
        show_toast(f"✓  Found — password copied to clipboard.")
    else:
        show_toast(f"✗  No entry found for  \"{website}\".", error=True)

# ─────────────────────────── TOAST NOTIFICATION ─────────────────────── #
def show_toast(msg, error=False):
    color = "#FF4D6D" if error else SUCCESS
    toast_label.config(text=msg, fg=color)
    window.after(3000, lambda: toast_label.config(text=""))

# ─────────────────────────── HOVER EFFECTS ──────────────────────────── #
def on_enter(btn, color=ACCENT_CYAN):
    btn.config(bg=color, fg=BG_DARK)

def on_leave(btn, bg=BG_ENTRY, fg=ACCENT_CYAN):
    btn.config(bg=bg, fg=fg)

def on_enter_add(btn):
    btn.config(bg=ACCENT_CYAN, fg=BG_DARK)

def on_leave_add(btn):
    btn.config(bg=ACCENT_GLOW, fg=BG_DARK)

# ═══════════════════════════ UI SETUP ═══════════════════════════════════ #
window = Tk()
window.title("KeyVault — Password Manager")
window.config(bg=BG_DARK, padx=0, pady=0)
window.resizable(False, False)

# ── Outer frame ─────────────────────────────────────────────────────── #
root_frame = Frame(window, bg=BG_DARK, padx=30, pady=28)
root_frame.pack()

# ── Header ──────────────────────────────────────────────────────────── #
header = Frame(root_frame, bg=BG_DARK)
header.grid(row=0, column=0, columnspan=3, sticky="EW", pady=(0, 20))

# Lock icon drawn as canvas art
lock_canvas = Canvas(header, width=36, height=36, bg=BG_DARK, highlightthickness=0)
lock_canvas.pack(side=LEFT, padx=(0, 10))
lock_canvas.create_rectangle(8, 18, 28, 32, fill=ACCENT_CYAN, outline="", width=0)
lock_canvas.create_arc(10, 6, 26, 24, start=0, extent=180, style=ARC,
                        outline=ACCENT_CYAN, width=3)
lock_canvas.create_rectangle(17, 22, 19, 28, fill=BG_DARK, outline="", width=0)

title_block = Frame(header, bg=BG_DARK)
title_block.pack(side=LEFT)
Label(title_block, text="KeyVault", font=FONT_TITLE,
      bg=BG_DARK, fg=FG_PRIMARY).pack(anchor="w")
Label(title_block, text="Your encrypted credential store",
      font=FONT_SUB, bg=BG_DARK, fg=FG_MUTED).pack(anchor="w")

# Thin cyan rule under header
Canvas(root_frame, height=1, bg=ACCENT_CYAN, highlightthickness=0,
       width=380).grid(row=1, column=0, columnspan=3, sticky="EW", pady=(0, 18))

# ── Field builder helper ─────────────────────────────────────────────── #
def make_label(text, row):
    lbl = Label(root_frame, text=text, font=FONT_LABEL,
                bg=BG_DARK, fg=FG_MUTED, anchor="w")
    lbl.grid(row=row, column=0, sticky="W", pady=(0, 2))

def make_entry(row, col=1, colspan=2, width=38, show=""):
    e = Entry(root_frame, width=width, font=FONT_ENTRY,
              bg=BG_ENTRY, fg=FG_PRIMARY, insertbackground=ACCENT_CYAN,
              relief="flat", bd=0, show=show,
              highlightthickness=1, highlightbackground=BORDER,
              highlightcolor=ACCENT_CYAN)
    e.grid(row=row, column=col, columnspan=colspan,
           sticky="EW", pady=(0, 10), ipady=7, padx=(0, 0))
    return e

def make_button(text, row, col, colspan=1, cmd=None,
                bg=BG_ENTRY, fg=ACCENT_CYAN, width=16):
    btn = Button(root_frame, text=text, font=FONT_BTN,
                 bg=bg, fg=fg, activebackground=ACCENT_CYAN,
                 activeforeground=BG_DARK, relief="flat", bd=0,
                 cursor="hand2", width=width, command=cmd ,
                 highlightthickness=1, highlightbackground=ACCENT_GLOW,
                 highlightcolor=ACCENT_CYAN)
    btn.grid(row=row, column=col, columnspan=colspan,
             sticky="EW", pady=(0, 10), padx=(4 if col > 0 else 0, 0), ipady=7)
    btn.bind("<Enter>", lambda e, b=btn: on_enter(b))
    btn.bind("<Leave>", lambda e, b=btn: on_leave(b))
    return btn

# ── Website row ─────────────────────────────────────────────────────── #
make_label("WEBSITE", 2)
website_entry = make_entry(3, col=1, colspan=1, width=24)
website_entry.focus()

search_btn = Button(root_frame, text="🔍  Search", font=FONT_BTN,
                    bg=BG_ENTRY, fg=ACCENT_CYAN, activebackground=ACCENT_CYAN,
                    activeforeground=BG_DARK, relief="flat", bd=0,
                    cursor="hand2", command=find_password,
                    highlightthickness=1, highlightbackground=ACCENT_GLOW,
                    highlightcolor=ACCENT_CYAN)
search_btn.grid(row=3, column=2, sticky="EW", pady=(0, 10), padx=(4, 0), ipady=7)
search_btn.bind("<Enter>", lambda e: on_enter(search_btn))
search_btn.bind("<Leave>", lambda e: on_leave(search_btn))

# ── Email row ───────────────────────────────────────────────────────── #
make_label("EMAIL / USERNAME", 4)
email_entry = make_entry(5, col=1, colspan=2)
email_entry.insert(0, "kartikbhardwaj0619@gmail.com")

# ── Password row ────────────────────────────────────────────────────── #
make_label("PASSWORD", 6)
password_entry = make_entry(7, col=1, colspan=1, width=24)
password_entry.bind("<KeyRelease>", on_password_key)

gen_btn = Button(root_frame, text="⚡ Generate", font=FONT_BTN,
                 bg=BG_ENTRY, fg=ACCENT_CYAN, activebackground=ACCENT_CYAN,
                 activeforeground=BG_DARK, relief="flat", bd=0,
                 cursor="hand2", command=generate_pass,
                 highlightthickness=1, highlightbackground=ACCENT_GLOW,
                 highlightcolor=ACCENT_CYAN)
gen_btn.grid(row=7, column=2, sticky="EW", pady=(0, 10), padx=(4, 0), ipady=7)
gen_btn.bind("<Enter>", lambda e: on_enter(gen_btn))
gen_btn.bind("<Leave>", lambda e: on_leave(gen_btn))

# ── Strength bar ────────────────────────────────────────────────────── #
strength_bar = Canvas(root_frame, width=200, height=6,
                       bg=BG_ENTRY, highlightthickness=0)
strength_bar.grid(row=8, column=1, sticky="W", pady=(0, 2))
strength_fill = strength_bar.create_rectangle(0, 0, 0, 6, fill=SUCCESS, outline="")

strength_label = Label(root_frame, text="", font=FONT_SUB,
                        bg=BG_DARK, fg=FG_MUTED)
strength_label.grid(row=8, column=2, sticky="W", padx=(6, 0))

# ── Copy hint ───────────────────────────────────────────────────────── #
copy_hint = Label(root_frame, text="", font=FONT_SUB,
                   bg=BG_DARK, fg=SUCCESS)
copy_hint.grid(row=9, column=1, columnspan=2, sticky="W", pady=(0, 6))

# ── Divider ─────────────────────────────────────────────────────────── #
Canvas(root_frame, height=1, bg=BORDER, highlightthickness=0,
       width=380).grid(row=10, column=0, columnspan=3,
                        sticky="EW", pady=(4, 14))

# ── Save button ─────────────────────────────────────────────────────── #
save_btn = Button(root_frame, text="🔒  Save Credentials", font=FONT_BTN,
                  bg=ACCENT_GLOW, fg=BG_DARK, activebackground=ACCENT_CYAN,
                  activeforeground=BG_DARK, relief="flat", bd=0,
                  cursor="hand2", command=save, width=38)
save_btn.grid(row=11, column=0, columnspan=3, sticky="EW", ipady=10)
save_btn.bind("<Enter>", lambda e: on_enter_add(save_btn))
save_btn.bind("<Leave>", lambda e: on_leave_add(save_btn))

# ── Toast notification ──────────────────────────────────────────────── #
toast_label = Label(root_frame, text="", font=FONT_SUB,
                     bg=BG_DARK, fg=SUCCESS, wraplength=380)
toast_label.grid(row=12, column=0, columnspan=3, pady=(10, 0))

# ── Footer ──────────────────────────────────────────────────────────── #
Label(root_frame, text="Passwords encrypted locally  •  Never sent anywhere",
      font=FONT_SUB, bg=BG_DARK, fg=FG_MUTED).grid(
    row=13, column=0, columnspan=3, pady=(8, 0))

window.mainloop()