import pygame
import random
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('images/beiliya.png')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width + random.randint(-50,50)
        self.rect.y = self.rect.height + random.randint(-50,50)
    

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # 每个外星人独立的移动方向和下坠标记
        self.direction = random.choice([-1, 1])  # 初始随机方向
        self.edge_hit = False

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right -1 or self.rect.left <= 1:
            return True

    def update(self):
        """向左或右移动外星人"""
        screen_rect = self.screen.get_rect()
        # 横向移动（先移动后修正）
        self.x += self.settings.alien_speed * self.direction
        self.rect.x = self.x
        self.y += self.settings.alien_speed * 0.5

        # 如果碰撞边缘则下移
        if self.check_edges():
            if not self.edge_hit:
                self.direction *= -1
                self.rect.y += self.settings.fleet_drop_speed   # 仅自身下移
                 # 强制修正坐标避免出界
                self.x = max(1,min(self.x,screen_rect.right - self.rect.width - 1))
                self.edge_hit = True    # 防止连续触发
        else:
            self.edge_hit = False

        self.rect.y = self.y

        # 防止移出屏幕底部
        if self.rect.bottom > self.settings.screen_height:
            self.kill()    

