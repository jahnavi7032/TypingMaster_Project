import random
import json
import time
import signal
import sys

# Constants
WORD_JSON_FILE = "words.json"
LEADERBOARD_JSON_FILE = "leaderboard.json"
WORD_COUNT = 10


def signal_handler(signal, frame):
    print("You have quit the game.")
    sys.exit(0)


def update_leaderboard(username, category, wpm):
    try:
        with open(LEADERBOARD_JSON_FILE, 'r') as f:
            leaderboard_data = json.load(f)
            leaderboard = leaderboard_data.get("leaderboard", [])
    except FileNotFoundError:
        leaderboard = []

    leaderboard.append({"username": username, "category": category, "wpm": wpm})
    leaderboard = sorted(leaderboard, key=lambda x: x["wpm"], reverse=True)

    leaderboard_data['leaderboard'] = leaderboard

    with open(LEADERBOARD_JSON_FILE, 'w') as f:
        json.dump(leaderboard_data, f, indent=4)


def show_leaderboard():
    try:
        with open(LEADERBOARD_JSON_FILE, 'r') as f:
            leaderboard_data = json.load(f)
            leaderboard = leaderboard_data.get("leaderboard", [])
            print("\nLeaderboard:")
            for i, entry in enumerate(leaderboard):
                print(f"{i + 1}. {entry['username']}: {entry['category']}: {entry['wpm']} WPM")
    except FileNotFoundError:
        print("Leaderboard is empty.")


def load_words_from_json(category):
    try:
        with open(WORD_JSON_FILE, 'r') as f:
            categories = json.load(f)
            return categories.get(category, [])
    except FileNotFoundError:
        return []


def get_user_input(prompt):
    return input(prompt)


def main():
    print("Terminal Typing Master")

    username = get_user_input("Enter your username: ")

    # Register Ctrl + Q as a signal to quit the game
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        print("\nOptions:")
        print("1. Start Typing Test")
        print("2. Show Leaderboard")
        print("3. Exit")

        option = get_user_input("Select an option: ")

        if option == '1':
            category = get_user_input("Enter a category: ")
            words = load_words_from_json(category)
            if not words:
                print("Word list is empty. Please add words to 'words.json'.")
                continue

            input("Press Enter to start the test...")
            start_time = time.time()

            random_words = random.sample(words, WORD_COUNT)
            correct_words = 0

            for word in random_words:
                user_input = get_user_input(f"Type '{word}': ")
                if user_input == word:
                    correct_words += 1

            end_time = time.time()
            time_taken = end_time - start_time
            wpm = float(correct_words / (time_taken / 60))
            print(f"Words Typed: {correct_words}/{WORD_COUNT}")
            print(f"Time Taken: {time_taken:.2f} seconds")
            print(f"Words Per Minute (WPM): {wpm}")
            update_leaderboard(username, category, wpm)

        elif option == '2':
            show_leaderboard()

        elif option == '3' or option.lower() == 'quit' or option.lower() == 'exit':
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose a valid option (1, 2, or 3).")


if __name__ == "__main__":
    main()
