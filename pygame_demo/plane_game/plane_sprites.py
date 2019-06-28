import random
import pygame

# 屏幕大小
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新频率
FRAME_PER_SEC = 60
# 敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image, speed=1):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在垂直方向上移动
        self.rect.y += self.speed


class BackGround(GameSprite):
    """游戏背景"""

    def __init__(self, is_alt=False):
        super().__init__("./images/background.png")
        # 2. 判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        # 2. 判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机"""

    def __init__(self):
        super().__init__("./images/enemy1.png")
        # 初始速度
        self.speed = random.randint(1, 3)
        # 初始随机位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        # 垂直飞行
        super().update()
        # 是否飞出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            # kill方法可以将精灵从所有精灵组中移出，并自动销毁
            self.kill()
            print("敌机销毁...")

    def __del__(self):
        pass


class Hero(GameSprite):
    """英雄"""

    def __init__(self):
        super().__init__("./images/me1.png", 0)
        # 英雄初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # 子弹
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        # 控制边界
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("发射子弹...")
        for i in range(0, 3):
            bullet = Bullet()
            # 子弹位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx

            self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹"""

    def __init__(self):
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            # 销毁子弹
            self.kill()

    def __del__(self):
        print("子弹被销毁...")
