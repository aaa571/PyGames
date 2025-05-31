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
        self.position = (random.randint(0, SCREEN_SIZE[0] - self.image.get_width()), -50)  # y座標固定、xのみランダム
    def move(self):
        self.position = (self.position[0], self.position[1] + 5)
    def draw(self):
        screen.blit(self.image, self.position)

class Eater:
    def __init__(self):
        self.image = pygame.image.load("Eater.png")
        self.image_rect = self.image.get_rect()
        self.image_rect.centery = (SCREEN_SIZE[1] - (self.image.get_height() // 2))  # 画面の中央下に配置
    def move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # マウスの位置を取得
        self.image_rect.centerx = mouse_x  # マウスのx座標を追従
        screen.fill((255, 255, 255))  # 画面を塗りつぶしてリセット
    def draw(self):
        screen.blit(self.image, self.image_rect)

def game_over(text, score):
    print(f"{text}!\nScore: {score}")
    text_3 = font.render(f"{text}! Score: {score}", True, (80, 80, 80))
    screen.blit(text_3, (SCREEN_SIZE[0] // 2 - text_3.get_width() // 2, SCREEN_SIZE[1] // 2 - text_3.get_height() // 2))
    pygame.display.update()  # 画面を更新


SCREEN_SIZE = (600, 700)
pygame.init()  # 初期化
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill((255, 255, 255))  # 背景色
pygame.display.set_caption("Apple Eater")  # Title
font = pygame.font.Font(None, 36)  # Font
clock = pygame.time.Clock()


def main():
    eater = Eater()
    time_out = 30  # ゲーム時間
    past_time = 0
    score = 0
    apple_score = 10
    good_apple_score = 30
    poison_apple_score = -5
    damage = 30
    recovery = 10  # 回復量
    hp_max = 100
    hp = hp_max
    apple_list = ["Apple.png", "Good_Apple.png", "Poison_Apple.png"]  # リンゴの種類
    weights = [0.5, 0.05, 0.45]  # 各リンゴの出現確率
    generation_time = 3.5  # リンゴを生成する間隔（秒）
    apples = []
    
    while True:
        clock.tick(60)  # FPS
        
        eater.move()
        eater.draw()  # Apple Eaterを描画

        current_time = pygame.time.get_ticks()  # 現在の時間を取得
        if current_time >= time_out * 1000:
            game_over("Time is up", score)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
        if (current_time - past_time) / 100 >= generation_time :  # 1000 clock = 1 second
            apple = Apple(random.choices(apple_list, weights, k=1)[0])  # ランダムにリンゴを生成
            apple.randomize_position()
            past_time = current_time  # 経過時間を更新
            apples.append(apple)  # 生成したリンゴをリストに追加
            
        for apple in apples:  # リンゴを描画
            apple.move()
            apple.draw()
        
        for apple in reversed(apples):  # リストを安全に更新するため逆順
            if apple.position[1] > SCREEN_SIZE[1]:  # リンゴが画面外に出たら削除
                del apples[apples.index(apple)]
                
            if eater.image_rect.colliderect(pygame.Rect(apple.position, (apple.image.get_width(), apple.image.get_height()))):
                if "Poison" in apple.name:  # 毒リンゴに当たったらダメージ
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

                elif "Good" in apple.name:  # 良いリンゴに当たったら+回復
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
        screen.blit(text_1, (15, 15))  # スコア表示
        
        text_2 = font.render(f"HP: {hp}", True, (0, 100, 100))
        screen.blit(text_2, (15, 45))  # HP表示

        # 画面を更新
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 閉じるボタンで終了
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()