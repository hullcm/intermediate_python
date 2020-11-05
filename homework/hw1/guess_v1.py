import random

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
    for count in range(0, 10):
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
      elif int(response) > secret:
        print('Too high! Try again.')
        count = count + 1
      elif int(response) < secret:
        print('Too low! Try again.')
        count = count + 1

      ##figure out how to stop after 10th guess   
      guesses = 10 - count
      print(f"Remaining Guesses: {guesses}")
      response = input("Enter a guess, or 'quit': ")
      if response == 'quit':
        exit()
      while response.isnumeric() == False:
        print("Invalid input. Enter a number between 0 and 1000")
        response = input("Enter a guess, or 'quit': ")
        if response == 'quit':
          exit()

    if guesses == 0:
      print(f"You lost the game! The secret is {secret}") 
      break
    else:
      print("You got it!")


   


