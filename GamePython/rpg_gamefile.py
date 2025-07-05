import random
import time
import os
import pygame

# Initialize mixer once
pygame.mixer.init()

def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_intro():
    banner = """
    \033[1;31m███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗   ██╗
    ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗╚██╗ ██╔╝
    ███████╗███████║███████║██████╔╝██║   ██║ ╚████╔╝ 
    ╚════██║██╔══██║██╔══██║██╔═══╝ ██║   ██║  ╚██╔╝  
    ███████║██║  ██║██║  ██║██║     ╚██████╔╝   ██║   
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝    ╚═╝   
       \033[1;33m⚔ SHADOW SHOWDOWN: Rock-Paper-Scissors ⚔\033[0m
    """
    play_sound(os.path.join(os.path.dirname(__file__), 'start.mp3'))

    print(banner)

def get_user_choice():
    choices = ['rock', 'paper', 'scissors']
    choice = input("\nChoose \033[1;36mrock\033[0m, \033[1;35mpaper\033[0m, or \033[1;34mscissors\033[0m: ").lower()
    if choice in choices:
        return choice
    else:
        slow_print("\033[1;31mInvalid choice. The shadows are disappointed.\033[0m")
        return get_user_choice()

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def decide_winner(user, comp):
    if user == comp:
        return "tie"
    if (user == 'rock' and comp == 'scissors') or \
       (user == 'paper' and comp == 'rock') or \
       (user == 'scissors' and comp == 'paper'):
        return "user"
    else:
        return "computer"

def print_result(user, comp, winner):
    slow_print(f"\n🧍 You chose: \033[1;36m{user}\033[0m")
    slow_print(f"🤖 Computer chose: \033[1;33m{comp}\033[0m")
    time.sleep(0.5)

    if winner == "tie":
        play_sound(os.path.join(os.path.dirname(__file__), 'tie.mp3'))

        slow_print("\n\033[1;37mIt's a tie! The shadows remain still...\033[0m")
    elif winner == "user":
        play_sound(os.path.join(os.path.dirname(__file__), 'win.mp3'))

        slow_print("\n\033[1;32mYou win this round! The darkness bows to you.\033[0m")
    else:
        play_sound(os.path.join(os.path.dirname(__file__), 'lose.mp3'))

        slow_print("\n\033[1;31mYou lose. The AI strikes from the void.\033[0m")

def play_game():
    user_score = 0
    computer_score = 0
    round_num = 1

    while True:
        clear()
        show_intro()
        print(f"\n\033[1;34m--- ROUND {round_num} ---\033[0m")
        print(f"\033[1;32mYou: {user_score} | 🤖 Computer: {computer_score}\033[0m")

        user = get_user_choice()
        comp = get_computer_choice()
        winner = decide_winner(user, comp)

        if winner == "user":
            user_score += 1
        elif winner == "computer":
            computer_score += 1

        print_result(user, comp, winner)

        choice = input("\nDo you want to play again? (y/n): ").lower()
        if choice != 'y':
            break
        round_num += 1

    slow_print("\n\033[1;35mThanks for playing SHADOW SHOWDOWN.\033[0m")
    slow_print(f"\033[1;32mFinal Score - You: {user_score} | Computer: {computer_score}\033[0m\n")

if __name__ == "__main__":
    play_game()
