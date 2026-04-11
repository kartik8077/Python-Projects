import html

# Adding some simple ANSI color constants
G = "\033[92m"  # Green
R = "\033[91m"  # Red
Y = "\033[93m"  # Yellow
B = "\033[94m"  # Blue
C = "\033[96m"  # Cyan
W = "\033[0m"  # Reset


class QuizBrain:
    def __init__(self, q_list):
        self.question_number = 0
        self.question_list = q_list
        self.score = 0

    def still_has_question(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        current_question = self.question_list[self.question_number]
        self.question_number += 1

        # Unescape HTML entities so "It's" doesn't look like "It&#039;s"
        clean_text = html.unescape(current_question.text)

        print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Y}Question {self.question_number}:{W} {clean_text}")
        ans = input(f"{B}True or False? {W}❯ ")

        self.check_answer(ans, current_question.answer)

    def check_answer(self, ans, answer):
        if ans.lower() == answer.lower():
            print(f"{G}✔ Correct! That's impressive.{W}")
            self.score += 1
        else:
            print(f"{R}✘ Wrong! Not quite.{W}")
            print(f"{Y}The correct answer was: {answer}{W}")

        print(f"Current Score: {G}{self.score}{W}/{Y}{self.question_number}{W}")
        print("\n")