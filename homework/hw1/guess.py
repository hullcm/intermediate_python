import random
import math

max_guess = input("Enter the max value: ")
if max_guess == 'quit':
  exit()
while max_guess.isnumeric() == False:
    print("Invalid input. Enter a number greater than 0")
    max_guess = input("Enter the max value: ")
    if max_guess == 'quit':
        exit()

max_guess_final = math.log(int(max_guess), 2) + 1
print(f"Max Guesses: {max_guess_final}")

secret = random.randint(0, 1000)
response = input("Enter a guess, or 'quit': ")

if response == 'quit':
  exit()

while response.isnumeric() == False:
  print("Invalid input. Enter a number between 0 and 1000")
  response = input("Enter a guess, or 'quit': ")

if int(response) == secret:
  print("You got it!")
else:
    while int(response) != secret:
        count = 0
        max_range = int(max_guess_final)
        max_range_f = max_range - 1
        for count in range(0, max_range_f):
            if response.isalpha() == True:
                print("Invalid input. Enter a number between 0 and 1000")
            if count == -1:
                print(f"You lost the game! The secret is {secret}")
                exit()
            elif response == 'quit':
                exit()
            elif int(response) < 0:
                print("Invalid input. Enter a number between 0 and 1000")
            elif int(response) > 1000:
                print("Invalid input. Enter a number between 0 and 1000")
            elif int(response) > secret and int(response) < 1001:
                print('Too high! Try again.')
                count = count + 1
            elif int(response) < secret and int(response) > 0:
                print('Too low! Try again.')
                count = count + 1

            guesses = max_range - count
            print(f"Remaining Guesses: {guesses}")
            response = input("Enter a guess, or 'quit': ")
            if response == 'quit':
                exit()
            while response.isnumeric() == False or int(response) < 0 or int(response) > 1000:
                print("Invalid input. Enter a number between 0 and 1000")
                response = input("Enter a guess, or 'quit': ")
                if response == 'quit':
                    exit()
            
            if int(response) == secret:
                    print("You got it!")
                    exit()

        if (guesses - 1) == 0:
            print(f"You lost the game! The secret is {secret}") 
            exit()
        else:
            print("You got it!")