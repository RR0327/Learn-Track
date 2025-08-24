import random

# Option 1: Chosen by computer, guessed by user.
def user_guess():
    print("Option 1: You guess the number")
    computer_number = random.randint(1, 100)
    while True:
        user_input = input("Guess the number (1 to 100): ")
        if not user_input.isdigit() or int(user_input) < 1 or int(user_input) > 100:
            print("Invalid input, Please enter a number between 1 and 100.")
            continue
        guess = int(user_input)
        if guess < computer_number:
            print("Too low!")
        elif guess > computer_number:
            print("Too high!")
        else:
            print(f"Correct! The number was {computer_number}.")
            break

# Option 2: Chosen by user, guessed by computer.
def computer_guess():
        print("Option 2: Computer guesses your number")
        print("Think of a number between 1 to 100 and enter it (for test):")
        user_number = int(input())
        low, high = 1, 100
        attempts = 0
        while True:
            attempts += 1
            guess =(low+high) // 2
            print(f"Computer guesses: {guess}")
            feedback = input("YOur feedback (H/L/C): ")
            if feedback == "H":
                high = guess -1
            elif feedback == "L":
                low = guess + 1
            elif feedback == "C":
                print(f"Computer guessed your number in {attempts} tries!")
                break
            else:
                print("Invalid feedback. Please enter H, L, or C.")

# main function
def main():
    while True:
        print("Choose an option:")
        print("1. You guess the number (computer selects)")
        print("2. Computer guesses your number")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            user_guess()
        elif choice == "2":
            computer_guess()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, Please try again.")

if __name__ == "__main__":
    main()