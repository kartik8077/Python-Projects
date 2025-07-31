import random

user_score=0
computer_score=0

option=["rock","paper","scissor"]

while True:
    user_input=input("Type Rock/Paper/Scissor or Q to quit :").lower()
    if user_input=="q":
        break
    
    if user_input not in ["rock","paper","scissor"]:
        continue

    random_number=random.randint(0,2)
    # rock :0 , paper :1 ,scissor :2
    
    computer_guess=option[random_number] 
    print("computer picked",computer_guess+".")

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



