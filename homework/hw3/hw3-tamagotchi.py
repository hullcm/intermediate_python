from random import randrange
import random

## CONSTANTS ##

##Art by Hayley Jane Wakenshaw - https://www.asciiart.eu/animals/dogs
DOG_LEFT = """
   __
o-''|\_____/)
 \_/|_)     )
    \  __  /
    (_/ (_/ 
"""

DOG_RIGHT = """
        __
(\_____/|''-o
(     (_|\_/
 \  __   / 
  \_) \_) 
"""

##Art by Joan Stark - https://www.asciiart.eu/animals/cats
CAT_LEFT = """
 /\    /    
(' )  (
 (  \  )
 |(__)/
"""

CAT_RIGHT = """
\    /\\
 )  ( ')
(  /  )
 \(__)|
"""

class Pet:
    '''A Tamagotchi pet!
    Attributes
    ----------
    name : string
        The pet's name
    sound : string
        The sound a pet makes
    '''
    max_boredom = 6
    max_hunger = 10
    leaves_hungry = 16
    leaves_bored = 12

    ascii_art_left = ""
    ascii_art_right = ""
    play_turns = 3


    def __init__(self, name, sound):
        self.name = name
        self.hunger = randrange(self.max_hunger)
        self.boredom = randrange(self.max_boredom)
        self.sound = sound


    def mood(self):
        '''Get the mood of a pet. A pet can be happy, hungry or bored,
        depending on wether it was fed or has played enough.

        Parameters
        ----------
        none

        Returns
        -------
        str
            The mood of the pet
        '''
        if self.hunger <= self.max_hunger and self.boredom <= self.max_boredom:
            return "happy"
        elif self.hunger > self.max_hunger:
            return "hungry"
        else:
            return "bored"


    def status(self):
        '''Get the status of a pet to know it's name, how it feels and what it wants.

        Parameters
        ----------
        none

        Returns
        -------
        str
            The name, mood and wants of the pet.
        '''
        state = "I'm " + self.name + '. '
        state += 'I feel ' + self.mood() + '. '
        if self.mood() == 'hungry':
            state += 'Please feed me.'
        if self.mood() == 'bored':
            state += 'You can play with me.'
        return state


    def do_command(self, resp):
        '''Calls the appropriate methods of a pet based on command "resp" given by player.

        Parameters
        ----------
        resp : string
            The command to be issued to the pet.

        Returns
        -------
        none
        '''
        if resp == "speak":
            print(self.speak())
        elif resp == "play":
            self.play()
        elif resp == "feed":
            self.feed()
        elif resp == "wait" and isinstance(self, Dog) == True:
            print("Please provide a valid command.")
        elif resp == "wait":
            print("Nothing to do...")
        else:
            print("Please provide a valid command.")


    def has_left(self):
        '''Returns True if a pet has left the game due to hunger or boredom, otherwise False.

        Parameters
        ----------
        none

        Returns
        -------
        bool
            If a pet has left
        '''
        return self.hunger > self.leaves_hungry or self.boredom > self.leaves_bored


    def clock_tick(self):
        '''Adds 2 to the pet's hunger and boredom for each turn. 

        Parameters
        ----------
        none

        Returns
        -------
        none
        '''
        self.hunger += 2
        self.boredom += 2


    def speak(self):
        '''Returns a pet's unique sound when prompted 
        
        Parameters
        -----------
        none

        Returns
        --------
        string
            the unique sound for the given pet 
        '''
        return "I say: " + self.sound


    def feed(self):
        '''Decreases a pet's hunger level 
        
        Parameters
        -----------
        none

        Returns
        --------
        none
        '''
        if self.hunger > 5:
            self.hunger -= 5 
        elif self.hunger <= 5:
            self.hunger = 0
            if self.hunger < 0:
                self.hunger = 0


    def play(self):
        '''User plays with pet, guessing which way the pet will look up to three times. 
        If user guesses successfully, pet's boredom decreases by 5.
        
        Parameters
        -----------
        none

        Returns
        --------
        string
            if guessed correctly, correct is printed 
            if not guessed correctly, the animal string is printed and another guess is prompted
        '''
        turns_left = self.play_turns
        while turns_left > 0:
            guess_direction = input("Which direction will the pet look?\n")
            direction_options = ['left', 'right']
            while guess_direction.lower() not in direction_options:
                print('Only left and right are valid guesses. Try again')
                guess_direction = input("Which direction will the pet look?\n")
            if guess_direction == random.choice(direction_options):
                print("Correct!")
                if self.boredom > 5:
                    self.boredom = self.boredom - 5
                else:
                    self.boredom = 0
                if self.boredom < 0:
                    self.boredom = 0
                    break
                break
            else: 
                turns_left -= 1
                if guess_direction.lower() == 'left':
                    print('I look to the left/right. Try again.')
                    print(self.ascii_art_left)
                if guess_direction.lower() == 'right':
                    print('I look to the left/right. Try again.')
                    print(self.ascii_art_right)


#######################################################################
#---------- Part 2: Inheritance - subclasses
#######################################################################

class Dog(Pet):
    '''A pet that is a Dog!
    Attributes
    ----------
    name : string
        The pet's name
    sound : string
        The sound a pet makes
    '''
    ascii_art_left = DOG_LEFT
    ascii_art_right = DOG_RIGHT

    def __init__(self, name, sound):
        super().__init__(name, sound)


    def speak(self):
        '''Returns a dog's unique sound when prompted 
        
        Parameters
        -----------
        none

        Returns
        --------
        string
            the unique sound for the dog 
        '''
        return super().speak() + " arrrf!"


class Poodle(Dog):
    '''A pet that is a Poodle!
    Attributes
    ----------
    name : string
        The pet's name
    sound : string
        The sound a pet makes
    '''
    

    def do_command(self, resp):
        '''Calls the appropriate methods of a pet based on command "resp" given by player.

        Parameters
        ----------
        resp : string
            The command to be issued to the pet.

        Returns
        -------
        none
        '''
        if resp == "dance":
            print(self.dance())
        else:
            return super().do_command(command)


    def dance(self):
        '''Returns a dancing notification when Poodle is selected and asked to dance

        Parameters
        ----------
        none

        Returns
        ---------
        string
            the unique dancing statement for Poodles
        '''
        return "Dancing in circles like Poodles do!"
    

    def speak(self):
        '''Returns a Poodle's unique sound when prompted 
        
        Parameters
        -----------
        none

        Returns
        --------
        string
            the unique dancing statement and unique sound for the poodle 
        '''
        print(self.dance())
        return super().speak()


class Cat(Pet):
    '''A pet that is a Cat!
    Attributes
    ----------
    name : string
        The pet's name
    sound : string
        The sound a pet makes
    meow_count: int
        The number of times the cat repeats its sound
    '''
    ascii_art_left = CAT_LEFT
    ascii_art_right = CAT_RIGHT
    play_turns = 5

    def __init__(self, name, sound, meow_count):
        super().__init__(name, sound)
        self.meow_count = meow_count


    def speak(self):
        '''Returns a cat's unique sound when prompted 
        
        Parameters
        -----------
        none

        Returns
        --------
        string
            the unique sound for the cat
        '''
        return "I say: " + self.sound*self.meow_count


def get_name():
    '''Asks the player which name a pet should have.

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    return input("How do you want to name your pet?\n")


def get_sound():
    '''Asks the player what sound a pet should make

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    return input("What does your pet say?\n")


def get_meow_count():
    '''Asks the player how often a cat should make a sound.

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    while True:
        resp = input("How often does your Cat make a sound?\n")
        if resp.isnumeric():
            return int(resp)


p = None

while p == None:
    resp_pet_type = input("What kind of pet would you like to adopt?\n")
    pet_types = ['dog', 'cat', 'poodle']
    if resp_pet_type.lower() in pet_types:
        pet_name = get_name()
        pet_sound = get_sound()
        if resp_pet_type.capitalize() == 'Cat':
            pet_meow = get_meow_count()
            p = Cat(pet_name, pet_sound, pet_meow)
        if resp_pet_type.capitalize() == 'Dog':
            p = Dog(pet_name, pet_sound)
        if resp_pet_type.capitalize() == 'Poodle':
            p = Poodle(pet_name, pet_sound)
    else:
        print("We only have Cats, Dogs, and Poodles. Please provide a valid pet.")

while not p.has_left():
    print()
    p.status()
    print(p.status())

    command = input("What should I do?\n")
    p.do_command(command)
    p.clock_tick()

print("Your pet has left.")