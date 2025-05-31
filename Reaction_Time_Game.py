import time
import random

def reaction_time_game():
    print("This is Reaction Time Game!   Press Enter as fast as you can!")
    input("Press Enter to start...")
    
    # Wait for a random time
    wait_time = random.uniform(2, 10)  # 2 ~ 10 seconds
    time.sleep(wait_time)
    print("Now!")
    
    start_time = time.time()
    
    input()  # Wait for user to press Enter
    end_time = time.time()
    print("Enter pressed.\n")
    
    reaction_time = end_time - start_time
    print(f"Your reaction time is: {reaction_time:.3f} seconds")
    
    if reaction_time < 0.3:
        print("Amazing!!! You are super fast!")
    elif reaction_time < 0.4:
        print("Excellent!! You are very quick!")
    elif reaction_time < 0.5:
        print("Good job! You can do better!")
    elif reaction_time < 0.6:
        print("Not bad. You can improve!")
    else:
        print("Oh no! You are too slow. Let's try again!")
    
if __name__ == "__main__":
    reaction_time_game()