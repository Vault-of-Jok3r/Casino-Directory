import sys
import os
import signal
import sys
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), "games"))

from folder_roulette import main as folder_roulette_main
from roulette_of_fate import main as roulette_of_fate_main
from head_or_tails import main as head_or_tails_main

def clear_console():
    if os.name == 'nt':
        subprocess.call("cls", shell=True)
    else:
        subprocess.call("clear", shell=True)

def disable_exit_signals():
    """
    Intercepte Ctrl+C (SIGINT) et SIGTERM pour empêcher la sortie.
    """
    def handler(signum, frame):
        print("\n[!] You cannot quit with Ctrl + C. Finish the game!")
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

logo = """\033[92m
   █████████                     ███                                                   
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
        print("\nAvailable games:\n")
        print("\033[92m1. Folder Roulette\033[0m")
        print("\033[92m2. Roulette of Fate\033[0m")
        print("\033[92m3. Heads or Tails\033[0m")
        print("\033[92m4. Quit\033[0m\n")

        choice = input("[*] Select a game: ")

        if choice == "1":
            print("\n[+] Launching Folder Roulette...\n")
            clear_console()
            folder_roulette_main()
        elif choice == "2":
            print("\n[+] Launching Roulette of Fate...\n")
            clear_console()
            roulette_of_fate_main()
        elif choice == "3":
            print("\n[+] Launching Heads or Tails...\n")
            clear_console()
            head_or_tails_main()
        elif choice == "4":
            print("\n[*] Goodbye! Thanks for playing!")
            sys.exit(0)
        else:
            print("[!] Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main_menu()
