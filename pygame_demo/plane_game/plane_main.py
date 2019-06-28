# -*- coding: utf-8 -*-
import pygame
import io
import sys
# 改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

from plane_sprites import *


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化...")
        # 1. 游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. 时钟
        self.clock = pygame.time.Clock()
        self.__create_sprites()

        # 4. 定时器：创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def start_game(self):
        print("游戏开始...")
        while True:
            # 1. 设置刷新频率
            self.clock.tick(FRAME_PER_SEC)
            # 2. 事件监听
            self.__event_handler()
            # 3. 碰撞检测
            self.__check_collide()
            # 4. 更新/绘制精灵级
            self.__update_sprites()
            # 5. 更新显示
            pygame.display.update()

    def __create_sprites(self):
        """创建精灵和精灵组"""
        # 背景
        bg1 = BackGround()
        bg2 = BackGround(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        # 敌机
        self.enemy_group = pygame.sprite.Group()
        # 英雄
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                print("敌机出场...")
                enemy = Enemy()

                # 添加敌机
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            # elif event.type == pygame.KEYDOWN and event.tick == pygame.K_RIGHT:
            #     print("向右移动...")

        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(
            self.hero.bullets, self.enemy_group, True, True)
        # 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(
            self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            PlaneGame.__game_over()

    @staticmethod
    def __game_over():
        print("英雄阵亡...")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()

# # 初始化模块
# pygame.init()

# screen = pygame.display.set_mode((480, 700))

# # 绘制背景图片
# bg = pygame.image.load("./images/background.png")
# screen.blit(bg, (0, 0))

# # 绘制英雄
# hero = pygame.image.load("./images/me1.png")
# # screen.blit(hero, (200, 500))
# # pygame.display.update()


# # 1. 记录飞机初始位置
# hero_rect = pygame.Rect(200, 500, 102, 126)

# # 游戏循环
# while True:
#     clock.tick(60)
#     # 事件监听
#     event_list = pygame.event.get()
#     for event in event_list:
#         if event.type == pygame.QUIT:
#             print("退出游戏...")
#             # 卸载所有模块
#             pygame.quit()
#             exit()

#     # 2. 修改飞机位置pygame.quit()
#     hero_rect.y -= 1
#     # 判断飞机位置
#     if (hero_rect.y <= 0):
#         hero_rect.y = 700

#     # 3. 绘制图像
#     screen.blit(bg, (0, 0))
#     screen.blit(hero, hero_rect)
#     pygame.display.update()
