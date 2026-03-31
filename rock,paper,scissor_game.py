# import random

# user_score=0
# computer_score=0

# option=["rock","paper","scissor"]

# while True:
#     user_input=input("Type Rock/Paper/Scissor or Q to quit :").lower()
#     if user_input=="q":
#         break
    
#     if user_input not in ["rock","paper","scissor"]:
#         continue

#     random_number=random.randint(0,2)
#     # rock :0 , paper :1 ,scissor :2

#     computer_guess=option[random_number] 
#     print("computer picked",computer_guess+".")

#     if user_input=="rock" and computer_guess=="scissor":
#         print("You won !!")
#         user_score+=1
#         continue
    
#     if user_input=="rock" and computer_guess=="paper":
#         print("You Loose !!")
#         computer_score+=1
#         continue

#     if user_input == computer_guess:
#         print("Tie !!")
#         continue

#     if user_input=="paper" and computer_guess=="rock":
#         print("You Win !!")
#         user_score+=1
#         continue
    
#     if user_input=="paper" and computer_guess=="scissor":
#         print("You loss !!")
#         computer_score+=1
#         continue
    
#     if user_input=="scissor" and computer_guess=="rock":
#         print("You Loss !!")
#         computer_score+=1
#         continue
    
#     if user_input=="scissor" and computer_guess=="paper":
#         print("You Win !!")
#         user_score+=1
#         continue
    

# print(f"computer wins {computer_score} times .")
# print(f"you won {user_score} times .")
# print("Goodbye !!!")


"""
Rock-Paper-Scissor GUI with animation (Pygame)
Save as: rps_gui_pygame.py
Requirements: Python 3.8+, pygame (pip install pygame)

Features:
- Clicking buttons for Rock/Paper/Scissor
- Computer "thinking" spinner
- Animated choice slide-in and glow
- Score pop animation and small particle bursts
- Final summary and graceful exit

This is self-contained and uses simple geometric shapes/text for visuals so no image assets are required.
"""
import pygame
import random
import math
import sys
from pygame import gfxdraw

# ---------- Config ----------
FPS = 60
WIDTH, HEIGHT = 900, 600
BG_COLOR = (24, 24, 30)
CARD_COLOR = (35, 35, 48)
ACCENT = (90, 200, 255)
TXT_COLOR = (230, 230, 235)
BUTTON_H = 70

OPTIONS = ["rock", "paper", "scissor"]

# ---------- Helpers ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissor — Animated GUI")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont(None, 48)
font_med = pygame.font.SysFont(None, 28)
font_small = pygame.font.SysFont(None, 20)

# simple icons drawn with shapes
def draw_icon(surface, kind, center, size=80):
    x, y = center
    if kind == "rock":
        # a rounded stone-like polygon
        pygame.draw.circle(surface, (200, 200, 200), (x, y), int(size*0.45))
        pygame.draw.circle(surface, (190, 190, 190), (x-18, y-12), int(size*0.2))
    elif kind == "paper":
        r = int(size*0.48)
        rect = pygame.Rect(x-r, y-r, 2*r, 2*r)
        pygame.draw.rect(surface, (245, 245, 255), rect, border_radius=8)
        pygame.draw.line(surface, (220,220,240), (x-r+12, y-r+18), (x+r-12, y-r+18), 3)
    elif kind == "scissor":
        # two blades
        pygame.draw.line(surface, (220,220,220), (x-35, y-10), (x+35, y+20), 6)
        pygame.draw.line(surface, (220,220,220), (x-35, y+20), (x+35, y-10), 6)
        pygame.draw.circle(surface, (200,200,200), (x-6, y+6), 10)

# particle for small burst
class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        ang = random.uniform(0, math.tau)
        sp = random.uniform(2, 6)
        self.vx = math.cos(ang) * sp
        self.vy = math.sin(ang) * sp
        self.life = random.uniform(0.5, 1.0)
        self.radius = random.randint(2,4)
        self.age = 0

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.12  # gravity-ish
        self.age += dt

    def draw(self, surf):
        a = max(0, 255 * (1 - self.age/self.life))
        if a <= 0: return
        col = (255, 220, 140, int(a))
        s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, col, (self.radius, self.radius), self.radius)
        surf.blit(s, (int(self.x-self.radius), int(self.y-self.radius)))

# ---------- Game State ----------
user_score = 0
comp_score = 0
particles = []

# animated cards positions
user_card_x = WIDTH*0.25
comp_card_x = WIDTH*0.75
card_y = HEIGHT*0.4

action_state = "idle"  # idle, counting, reveal, animating
countdown = 0.0
countdown_time = 0.9
spinner_ang = 0.0

user_choice = None
comp_choice = None
result_text = ""
score_pop = 0.0

# buttons
button_rects = {}
btn_w = 180
spacing = 24
start_x = WIDTH/2 - (btn_w*3 + spacing*2)/2
for i, opt in enumerate(OPTIONS):
    r = pygame.Rect(start_x + i*(btn_w+spacing), HEIGHT-120, btn_w, BUTTON_H)
    button_rects[opt] = r

# ---------- Logic ----------
def decide_winner(user, comp):
    if user == comp:
        return "tie"
    wins = {"rock":"scissor","paper":"rock","scissor":"paper"}
    return "user" if wins[user] == comp else "comp"

# ---------- Main Loop ----------
running = True
while running:
    dt = clock.tick(FPS)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if action_state == "idle":
                mx,my = event.pos
                for opt, rect in button_rects.items():
                    if rect.collidepoint((mx,my)):
                        # start round
                        user_choice = opt
                        comp_choice = None
                        result_text = ""
                        action_state = "counting"
                        countdown = 0.0
                        spinner_ang = 0.0
                        # small pop particles to indicate click
                        for _ in range(8): particles.append(Particle((mx,my)))

    # update
    if action_state == "counting":
        countdown += dt
        spinner_ang += 10 * dt
        if countdown >= countdown_time:
            # pick computer choice, then go to reveal
            comp_choice = random.choice(OPTIONS)
            action_state = "reveal"
            # animate score pop if immediate
            res = decide_winner(user_choice, comp_choice)
            if res == "user":
                user_score += 1
                score_pop = 1.0
                for _ in range(18): particles.append(Particle((WIDTH*0.33, HEIGHT*0.18)))
            elif res == "comp":
                comp_score += 1
                score_pop = 1.0
                for _ in range(18): particles.append(Particle((WIDTH*0.66, HEIGHT*0.18)))
            else:
                score_pop = 0.6

    # update particles
    for p in particles[:]:
        p.update(dt)
        if p.age >= p.life:
            particles.remove(p)

    # score pop easing
    if score_pop > 0:
        score_pop -= dt * 1.8
        if score_pop < 0: score_pop = 0

    # ---------- draw ----------
    screen.fill(BG_COLOR)

    # header
    title = font_big.render("Rock  •  Paper  •  Scissor", True, TXT_COLOR)
    screen.blit(title, (WIDTH*0.5 - title.get_width()/2, 18))

    # scoreboard cards
    # user card
    ux = WIDTH*0.33
    uy = 100
    card_w, card_h = 260, 96
    pygame.draw.rect(screen, CARD_COLOR, (ux-card_w/2, uy-card_h/2, card_w, card_h), border_radius=12)
    user_label = font_med.render("YOU", True, TXT_COLOR)
    screen.blit(user_label, (ux-110, uy-10))
    # animated score
    us_text = font_big.render(str(user_score), True, ACCENT if score_pop>0 else TXT_COLOR)
    scale = 1.0 + 0.35*score_pop
    ssurf = pygame.transform.smoothscale(us_text, (int(us_text.get_width()*scale), int(us_text.get_height()*scale)))
    screen.blit(ssurf, (ux+30 - ssurf.get_width()/2, uy - ssurf.get_height()/2))

    # comp card
    cx = WIDTH*0.66
    cy = 100
    pygame.draw.rect(screen, CARD_COLOR, (cx-card_w/2, cy-card_h/2, card_w, card_h), border_radius=12)
    comp_label = font_med.render("COMPUTER", True, TXT_COLOR)
    screen.blit(comp_label, (cx-110, cy-10))
    cs_text = font_big.render(str(comp_score), True, TXT_COLOR if score_pop==0 else ACCENT)
    screen.blit(cs_text, (cx+30 - cs_text.get_width()/2, cy - cs_text.get_height()/2))

    # center arena card
    arena_w, arena_h = 520, 240
    arena_x = WIDTH/2 - arena_w/2
    arena_y = HEIGHT*0.28
    pygame.draw.rect(screen, (18,18,22), (arena_x, arena_y, arena_w, arena_h), border_radius=16)

    # user/computer icons - animate slide in during reveal
    # positions
    user_dest = (int(WIDTH*0.33), int(arena_y + arena_h*0.5))
    comp_dest = (int(WIDTH*0.66), int(arena_y + arena_h*0.5))

    # compute slide progress
    if action_state == "idle":
        # idle floating small bob
        t = pygame.time.get_ticks()/1000.0
        bob = math.sin(t*2.0)*6
        if user_choice:
            draw_icon(screen, user_choice, (user_dest[0], int(user_dest[1]+bob)), size=86)
        if comp_choice:
            draw_icon(screen, comp_choice, (comp_dest[0], int(comp_dest[1]-bob)), size=86)
    elif action_state == "counting":
        # show user's locked choice static and spinner for computer
        draw_icon(screen, user_choice, user_dest, size=96)
        # spinner at comp spot
        spr = font_med.render("...", True, TXT_COLOR)
        screen.blit(spr, (comp_dest[0]-spr.get_width()/2, comp_dest[1]-spr.get_height()/2))
        # small rotating ring
        spinner_ang += dt*8
        for i in range(6):
            ang = spinner_ang + i*(math.tau/6)
            rx = comp_dest[0] + math.cos(ang)*36
            ry = comp_dest[1] + math.sin(ang)*36
            pygame.gfxdraw.filled_circle(screen, int(rx), int(ry), 6, (120,120,140))
    elif action_state == "reveal":
        # draw both choices with a pop glow
        draw_icon(screen, user_choice, user_dest, size=108)
        draw_icon(screen, comp_choice, comp_dest, size=108)
        # result text
        res = decide_winner(user_choice, comp_choice)
        if res == "tie":
            result_text = "TIE!"
        elif res == "user":
            result_text = "YOU WIN!"
        else:
            result_text = "COMPUTER WINS!"
        # after reveal, go back to idle after a small delay
        # use countdown_time as a short pause
        countdown_time2 = 0.9
        countdown += dt
        if countdown >= countdown_time + countdown_time2:
            action_state = "idle"
            countdown = 0
    
    # draw result text
    if result_text:
        res_surf = font_big.render(result_text, True, ACCENT if "YOU" in result_text else (220,140,120))
        screen.blit(res_surf, (WIDTH/2 - res_surf.get_width()/2, arena_y + arena_h + 6))

    # draw buttons
    for opt, rect in button_rects.items():
        # hover effect
        mx,my = pygame.mouse.get_pos()
        hovered = rect.collidepoint((mx,my))
        clr = (44,44,60) if not hovered else (64,64,86)
        pygame.draw.rect(screen, clr, rect, border_radius=12)
        label = font_med.render(opt.upper(), True, TXT_COLOR)
        screen.blit(label, (rect.x + rect.width/2 - label.get_width()/2, rect.y + rect.height/2 - label.get_height()/2))
        # tiny icon above button
        draw_icon(screen, opt, (rect.x + rect.width/2, rect.y - 24), size=28)

    # particles
    for p in particles:
        p.draw(screen)

    # footer hint
    hint = font_small.render("Click a button to play. Close window or press ESC to quit.", True, (140,140,150))
    screen.blit(hint, (WIDTH/2 - hint.get_width()/2, HEIGHT-20))

    # input handling for ESC
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
