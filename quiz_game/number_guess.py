import random

random_number=random.randint(0,100)
guesses=0

while True:
    guesses+=1
    num=int(input("Enter a Number :"))

    if num==random_number:
        print(f'You got the number !!')
        break
    elif num<random_number:
        print(f'Enter a higher number ......')
    else :
        print(f'Enter a lower number ......')

print(f'You got it in {guesses} guesses')













