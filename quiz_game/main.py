from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
import html

# ANSI Colors for the main screen
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

def print_welcome():
    print(f"{MAGENTA}")
    print(r"""
     _____  _    _  _____  ______     _____           __  __  ______ 
    |  _  || |  | ||_   _||___  /    / ____|   /\    |  \/  ||  ____|
    | | | || |  | |  | |     / /    | |  __   /  \   | \  / || |__   
    | | | || |  | |  | |    / /     | | |_ | / /\ \  | |\/| ||  __|  
    \ \_/ /| |__| | _| |_  / /__    | |__| |/ ____ \ | |  | || |____ 
     \___/  \____/ |_____|/_____|    \_____/_/    \_\|_|  |_||______|
    """)
    print(f"{CYAN}--- Welcome to the Computer Science Challenge ---{RESET}\n")

print_welcome()

question_bank = []

for question in question_data["results"]:
    # Cleaning text during creation
    question_text = html.unescape(question["question"])
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

Quiz = QuizBrain(question_bank)

while Quiz.still_has_question():
    Quiz.next_question()

# Final screen
print(f"{MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"🏁 QUIZ COMPLETED!")
print(f"🏆 Final Score: {Quiz.score}/{Quiz.question_number}")

percentage = (Quiz.score / Quiz.question_number) * 100
if percentage == 100:
    print("GODLIKE! You are a tech master! 👑")
elif percentage >= 70:
    print("Great job! You really know your stuff. 👏")
else:
    print("Keep learning! Tech changes every day. 📚")
print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")