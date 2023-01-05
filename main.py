import os
from sys import platform
from random import shuffle
from time import sleep
from requests import get

# Constants
TITLE = "Tarot Prediction"
INPUT_SPEED = 7 # speed for Input
PRINT_SPEED = 6 # speed for printing output

# Check platform for system commands
if platform in ["linux", "darwin"]:
    """ Clears the screen """
    clear = lambda: os.system("clear")
elif platform == "win32":
    clear = lambda: os.system("cls")

# Print speed and effect
class Print:
    """ Print output with a typing effect, speed can be adjusted class contains two modes first one is a direct print function -> Print(string, speed) second mode is a decorator"""
    def __init__(self, string=None, speed=0.005):
        # limiting speed between 0 and 10
        speed = 10 if speed > 10 else 0 if speed < 0 else speed
        self.speed = (10-speed) * 0.005 # reducing speed to decimals
        
        # if the class is initialized with a string works as a function
        if string:
            for i in string:
                print(i, end="", flush=True)
                sleep(self.speed)
                
    def __call__(self, func):
        # execute funtion inside a decorator
        def wrapper(*args, **kwargs):
            """ wrapper function for passing arbitrary positional arguments and keyword arguments """
            for i in func(*args, **kwargs):
                print(i, end="", flush=True)
                sleep(self.speed)
        return wrapper

# validate and get input
def get_input(string, datatype="str", choice=None):
    """ validates the input with given datatype, if there is choice provided it checks if the input given is a choice, if not it repeatedly asks for the input until it gets the desired input from the choice given """
    string = string.capitalize()
    count = 1
    max_tries = 3
    while count <= max_tries:
        count += 1
        try:
            if datatype == "str":
                Print(f"{string}: ", speed=INPUT_SPEED)
                action = input()
                # if there is a choice and if it is under maximum tries
                if count <= max_tries and choice:
                    # loops again if the input is not in the choices assigned
                    if action not in choice:
                        Print(f"Choose ({' or '.join([i for i in choice])})\n", speed=PRINT_SPEED)
                        continue
                    else:
                        return action
                return action
                
            elif datatype == "int":
                Print(f"{string}: ", speed=INPUT_SPEED)
                action = int(input())
                # if there is a choice and if it is under maximum tries
                if count <= max_tries and choice:
                    # loops again if the input is not in the choices assigned
                    if action not in choice:
                        Print(f"Valid choice (0 to 77)\n", speed=PRINT_SPEED)
                        continue
                    else:
                        return action
                return action
            else:
                Print(f"{string}: ", speed=INPUT_SPEED)
                return float(input())
        except ValueError:
            Print(f"Invalid input... Expecting {datatype}\n")
    Print("Exeeded maximum number of tries..")
    exit()

# get tarot data
def get_card(num):
    """ gets the json data required for the script from github """
    url = "https://raw.githubusercontent.com/Albiahbii/json/main/tarot_card.json"
    res = get(url).json()
    # assigning keys of all the tarot cards in a variable
    dict_keys = list(res["cards"].keys())
    shuffle(dict_keys) # shuffles the list for randomness
    card = dict_keys[num-1] # getting key for a single card
    data = res["cards"][card] # assigning card data to a variable
    return (card, data)

# Print Title
@Print(speed=6)
def display_intro():
    """ introduction about tarot card... returns a string """
    Print(f"\t\t{TITLE}\n")
    Print("Synopsis:\n")
    intro = "\tPlaying cards first entered Europe in the late 14th century, but the origin is unknown. The first records date to 1367 in Berne and they appear to have spread very rapidly across the whole of Europe, as may be seen from the records, mainly of card games being banned. Little is known about the appearance and number of these cards.\n\nOne early pattern of playing cards that evolved was one with the suits of Batons or Clubs, Coins, Swords, and Cups. These suits are still used in traditional Italian, Spanish and Portuguese playing card decks, and are also used in modern (occult) tarot divination cards that first appeared in the late 18th century.\n\n"
    return intro

# Get a random tarot card
def random_tarot(name):
    """ it gets a random tarot card details """
    Print(f"Hello {name}, let's find out what the cards tells you about your future... \n")
    num = get_input("Choose a random number between (1, 78)", "int", choice=range(1,79))
    clear()
    print(f"\t\t{TITLE}\n")
    card, data = get_card(num) 
    print(f"{name} your card is {card}\n")
    action = get_input("Read, what tarot card tells about you (yes,no)", choice=("yes", "no"))
    if action == "yes":
        # loops the output for displaying and printing details about a particular topic
        while True:
            clear()
            print(f"\t\t{TITLE}\n")
            Print("Topics:\n", speed=PRINT_SPEED)
            dict_keys = list(data.keys())
            for idx, i in enumerate(dict_keys):
                Print(f"{idx+1}. {i.title()}\n", speed=PRINT_SPEED)
                
            choice = get_input("Your choice", "int", choice=range(1,len(dict_keys)))
            clear()
            print(f"\t\t{TITLE}\n")
            Print(f"{dict_keys[choice-1].title()}:\n", speed=PRINT_SPEED)
            Print(data[dict_keys[choice-1]], speed=PRINT_SPEED)
            action = get_input("\nKnow more? (yes, no)", choice=("yes", "no"))
            if action == "yes":
                continue
            else:
                break
        Print("Hope you enjoyed knowing your luck {name}...\n", speed=PRINT_SPEED)
        Print("Good Bye...", speed=PRINT_SPEED)
        Print()
    else:
        Print("That's a shame {name}, not knowing your card!!..\n", speed=PRINT_SPEED)
        Print("Good Bye...", speed=PRINT_SPEED)  

# Entry point
def main():
    """ this function is the entry point for the whole script, our program starts here, first displays the intro then executes rest of the function """
    display_intro()
    action = get_input("Continue? (yes,no)", choice=("yes", "no"))
    if action == "yes":
        clear()
        print(f"\t\t{TITLE}\n")
        name = get_input("Enter your name").title()
        random_tarot(name)
    else:
        Print("Exiting program... ", speed=PRINT_SPEED)
        Print("Good Bye...", speed=PRINT_SPEED)
        Print()

if __name__ == "__main__":
    main()
    
