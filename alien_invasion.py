import sys
# 用于处理程序退出
import pygame
# 用于创建游戏窗口、处理事件、绘制图形等
from time import sleep
import random

from settings import Settings
# 管理游戏的设置
from ship import Ship
# 管理飞船的行为和绘制
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from difficulty_button import DifficultyButton
from scoreboard import ScoreBoard

class AlienInvasion(object):
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源。"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height)
        )
        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_height = self.screen.get_rect().height
        # self.settings.screen_width = self.screen.get_rect().width
        pygame.display.set_caption("Alien Invasion")

        # 创建存储游戏统计信息的实例
        # 并创建记分牌
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        self.ship = Ship(self)  # 这里传入的self就是AlienInvasion对象本身
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建play按钮
        self.play_button = Button(self,'Play')
        self.play_button.visible = True

        self.difficulty_buttons = pygame.sprite.Group()
        self._create_difficulty_buttons()
        self.choosing_difficulty = False

        # 初始化暂停状态
        self.paused = False

    def _create_difficulty_buttons(self):
        # 创建难度选择按钮
        easy = DifficultyButton(self, 'Easy', 1, (0, -100))
        normal = DifficultyButton(self, 'Normal', 2, (0, 0))
        hard = DifficultyButton(self, 'Hard', 3, (0, 100))
        self.difficulty_buttons.add(easy, normal, hard)
    
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active and not self.paused:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            
    def _check_events(self):
        # 监视键盘和鼠标事件。
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # mouse_pos = pygame.mouse.get_pos()
                clicked = False
                if self.choosing_difficulty:    # 新增难度选择处理
                    for button in self.difficulty_buttons:
                        if button.check_click(event.pos):
                            button.set_difficulty()
                            self._start_game()
                            clicked = True
                            break
                else:
                    self._check_play_button(event.pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self,mouse_pos):
        """在玩家单击play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.choosing_difficulty = True
            self.play_button.visible = False
            pygame.mouse.set_visible(True)
            self.sb.prep_score()
            # 重置游戏设置
            # self.settings.initialize_dynamic_settings()
            # self._start_game()

    def _start_game(self):
        # 重置游戏统计信息
        self.stats.reset_stats()
        self.stats.game_active = True
        #清空余下的外星人和子弹
        self.aliens.empty()
        self.bullets.empty()
        # 创建一群新的外星人并让飞船居中
        self._create_fleet()
        self.ship.center_ship()
        # 隐藏鼠标光标
        pygame.mouse.set_visible(False)
        self.choosing_difficulty = False

    def _check_keydown_events(self,event):
        """响应按键"""
        # 按enter开始游戏
        if event.key == pygame.K_RETURN:
            if not self.stats.game_active and not self.choosing_difficulty:
                self.choosing_difficulty = True
                self.play_button.visible = False
        # 向右移动飞船
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        # 向左移动飞船
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        # 向上动飞船
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        # 向下移动飞船
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        # 按q退出游戏
        elif event.key == pygame.K_q:
            sys.exit()
            
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_p:
            self.paused = not self.paused

    def _check_keyup_events(self,event):
        """响应松开"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False 
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False        
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

    def fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                # print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True
        )
        if collisions:
            # 此处用的是高能子弹，如果用普通子弹的话，应该要改成遍历字典的方式
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points*len(aliens)
            self.sb.prep_score()

        if not self.aliens:
            # 删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置"""
        self.aliens.update()    # 每个外星人自己处理移动
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            # print("Ship hit!!!")
            self._ship_hit()
        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        self.stats.ships_left -= 1
        if self.stats.ships_left > 0:
            # 将ships_left减1
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算一行可容纳多少个外星人
        # 外星人的间距为外星人宽度
        alien =Alien(self)
        alien_width,alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (3*alien_width)
        number_aliens_x = available_space_x // (4 * alien_width)
        
        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (4 * alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            # 创建一行外星人
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        # 创建一个外星人并将其加入当前行
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size

        alien.x = alien_width + 2 * alien_width * alien_number + random.randint(-20, 20)
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number + random.randint(-20, 20)

         # 确保外星人不会超出屏幕边界
        if alien.rect.left < 0:
            alien.rect.left = 0
        if alien.rect.right > self.settings.screen_width:
            alien.rect.right = self.settings.screen_width
        if alien.rect.top < 0:
            alien.rect.top = 0
        if alien.rect.bottom > self.settings.screen_height:
            alien.rect.bottom = self.settings.screen_height
        self.aliens.add(alien)
        
    # def _check_fleet_edges(self):
    #     """有外星人到达边缘时采取相应的措施"""
    #     for alien in self.aliens.sprites():
    #         if alien.check_edges():
    #             self._change_fleet_direction(alien)
    #             break

    # def _change_fleet_direction(self,alien):
    #     """将整群外星人下移，并改变他们的方向"""
    #     # for alien in self.aliens.sprites():
    #     alien.rect.y += self.settings.fleet_drop_speed
    #     self.settings.fleet_direction *= -1
    #     self.alien.update()

    def _update_screen(self):
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制Play按钮
        if self.choosing_difficulty:
            self.difficulty_buttons.draw(self.screen)
        elif not self.stats.game_active and self.play_button.visible:
            self.play_button.draw_button()

        # 如果游戏处于暂停状态，显示暂停信息
        if self.paused:
            pause_font = pygame.font.SysFont(None,74)
            pause_text = pause_font.render('PAUSED',True,(255,0,0))
            self.screen.blit(pause_text,(self.settings.screen_width // 2 - 100,
                                         self.settings.screen_height // 2))
        # 让最近绘制的屏幕可见
        pygame.display.flip()

if __name__ == "__main__":
    # 创建游戏实例并运行游戏。
    ai = AlienInvasion()
    ai.run_game()