import sys
import os
import signal
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "games"))

from folder_roulette import main as folder_roulette_main
from roulette_of_fate import main as roulette_of_fate_main

def disable_exit_signals():
    """
    Intercepte Ctrl+C (SIGINT) et SIGTERM pour empêcher la sortie.
    """
    def handler(signum, frame):
        print("\n[!] You cannot quit with Ctrl + C. Finish the game!")
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

logo = """
\033[92m   █████████                     ███                                                   
  ███░░░░░███                   ░░░                                                    
 ███     ░░░   ██████    █████  ████  ████████    ██████                               
░███          ░░░░░███  ███░░  ░░███ ░░███░░███  ███░░███                              
░███           ███████ ░░█████  ░███  ░███ ░███ ░███ ░███                              
░░███     ███ ███░░███  ░░░░███ ░███  ░███ ░███ ░███ ░███                              
 ░░█████████ ░░████████ ██████  █████ ████ █████░░██████                               
  ░░░░░░░░░   ░░░░░░░░ ░░░░░░  ░░░░░ ░░░░ ░░░░░  ░░░░░░                                                                                  
                                                                                       
 ██████████    ███                               █████                                 
░░███░░░░███  ░░░                               ░░███                                  
 ░███   ░░███ ████  ████████   ██████   ██████  ███████    ██████  ████████  █████ ████
 ░███    ░███░░███ ░░███░░███ ███░░███ ███░░███░░░███░    ███░░███░░███░░███░░███ ░███ 
 ░███    ░███ ░███  ░███ ░░░ ░███████ ░███ ░░░   ░███    ░███ ░███ ░███ ░░░  ░███ ░███ 
 ░███    ███  ░███  ░███     ░███░░░  ░███  ███  ░███ ███░███ ░███ ░███      ░███ ░███ 
 ██████████   █████ █████    ░░██████ ░░██████   ░░█████ ░░██████  █████     ░░███████ 
░░░░░░░░░░   ░░░░░ ░░░░░      ░░░░░░   ░░░░░░     ░░░░░   ░░░░░░  ░░░░░       ░░░░░███ 
                                                                              ███ ░███ 
                                                                             ░░██████  
                                                                              ░░░░░░\033[0m
"""

def main_menu():
    disable_exit_signals()

    while True:
        username = os.getlogin()
        print(logo)
        print("Welcome", username)
        print("\nAvailable games:")
        print("\033[92m1. Folder Roulette\033[0m")
        print("\033[92m2. Roulette of Fate\033[0m")
        print("\033[91m3. Quit\033[0m\n")

        choice = input("[*] Select a game: ")

        if choice == "1":
            print("\n[+] Launching Folder Roulette...\n")
            folder_roulette_main()
        elif choice == "2":
            print("\n[+] Launching Roulette of Fate...\n")
            roulette_of_fate_main()
        elif choice == "3":
            print("\n[*] Goodbye! Thanks for playing!")
            sys.exit(0)
        else:
            print("[!] Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main_menu()
