import pygame
import sys
import random


class Apple():
    def __init__(self, img):
        self.position = (0, 0)
        self.image = pygame.image.load(img)
        self.randomize_position()
        self.name = img
    def randomize_position(self):
        self.position = (random.randint(0, SCREEN_SIZE[0] - self.image.get_width()), -50)  # Fix y-coordinate, randomize only x
    def move(self):
        self.position = (self.position[0], self.position[1] + 5)
    def draw(self):
        screen.blit(self.image, self.position)

class Eater:
    def __init__(self):
        self.image = pygame.image.load("Eater.png")
        self.image_rect = self.image.get_rect()
        self.image_rect.centery = (SCREEN_SIZE[1] - (self.image.get_height() // 2))  # Place at the bottom center of the screen
    def move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse pointer position
        self.image_rect.centerx = mouse_x  # Follow the mouse's x-coordinate
        screen.fill((255, 255, 255))  # Fill the screen to reset
    def draw(self):
        screen.blit(self.image, self.image_rect)

def game_over(text, score):
    print(f"{text}!\nScore: {score}")
    text_3 = font.render(f"{text}! Score: {score}", True, (80, 80, 80))
    screen.blit(text_3, (SCREEN_SIZE[0] // 2 - text_3.get_width() // 2, SCREEN_SIZE[1] // 2 - text_3.get_height() // 2))
    pygame.display.update()  # Update the display


SCREEN_SIZE = (600, 700)
pygame.init()  # Initialization
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill((255, 255, 255))  # Background color
pygame.display.set_caption("Apple Eater")  # Title
font = pygame.font.Font(None, 36)  # Font
clock = pygame.time.Clock()


def main():
    eater = Eater()
    time_out = 30
    past_time = 0
    score = 0
    apple_score = 10
    good_apple_score = 30
    poison_apple_score = -5
    damage = 30
    recovery = 10  # Recovery amount
    hp_max = 100
    hp = hp_max
    apple_list = ["Apple.png", "Good_Apple.png", "Poison_Apple.png"]  # Types of apples
    weights = [0.5, 0.05, 0.45]  # Probability of each apple appearing
    generation_time = 3.5  # Interval for generating apples (seconds)
    apples = []
    
    while True:
        clock.tick(60)  # FPS
        
        eater.move()
        eater.draw()  # Draw the Apple Eater

        current_time = pygame.time.get_ticks()  # Get the current time
        if current_time >= time_out * 1000:
            game_over("Time is up", score)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
        if (current_time - past_time) / 100 >= generation_time :  # 1000 clock = 1 second
            apple = Apple(random.choices(apple_list, weights, k=1)[0])  # Generate a random apple
            apple.randomize_position()
            past_time = current_time  # Update the last generation time
            apples.append(apple)  # Add the generated apple to the list
            
        for apple in apples:  # Draw the apples
            apple.move()
            apple.draw()
        
        for apple in reversed(apples):  # Iterate in reverse to safely modify the list
            if apple.position[1] > SCREEN_SIZE[1]:  # If the apple goes off-screen, remove it
                del apples[apples.index(apple)]
                
            if eater.image_rect.colliderect(pygame.Rect(apple.position, (apple.image.get_width(), apple.image.get_height()))):
                if "Poison" in apple.name:  # If the apple is a poison apple, take damage
                    hp -= damage
                    score += poison_apple_score
                    del apples[apples.index(apple)]
                    if hp <= 0:
                        game_over("Game Over", score)
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                elif "Good" in apple.name:  # If the apple is a good apple, recover HP
                    if hp + recovery > hp_max:
                        hp = hp_max
                    else:
                        hp += recovery
                    del apples[apples.index(apple)]
                    score += good_apple_score
                else:
                    del apples[apples.index(apple)]
                    score += apple_score

        text_1 = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(text_1, (15, 15))  # Display score
        
        text_2 = font.render(f"HP: {hp}", True, (0, 100, 100))
        screen.blit(text_2, (15, 45))  # Display HP

        pygame.display.update()  # Update the display
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the window is closed
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()