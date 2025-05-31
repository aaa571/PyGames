import random
choices = ["R", "P", "S"]


print("Choice your hand: R, P, S")

while True:
    player_choice = input().strip().upper()
    cp_choice = random.choice(choices)
    # wrong input
    if player_choice not in choices:
        print("Invalid choice. Please choose R, P, or S.")
        continue
    # tie
    elif player_choice == cp_choice:
        print(f"You chose: {player_choice}")
        print(f"Computer chose: {cp_choice}")
        print("It's a tie!")
        print("Next hand: R, P, S")
        continue
    else :
        break


print(f"You chose: {player_choice}")
# win
if choices[(choices.index(cp_choice) + 1) % len(choices)] == player_choice:
    print(f"Computer chose: {cp_choice}")
    print("You win!")
# lose
else:
    print(f"Computer chose: {cp_choice}")
    print("You lose!")