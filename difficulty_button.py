import pygame.font
from pygame.sprite import Sprite
class DifficultyButton(Sprite):
    def __init__(self,ai_game,text,difficulty_level,offset):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.text = text
        self.difficulty_level = difficulty_level
        self.offset = offset

        # 按钮尺寸和颜色
        self.width,self.height = 200,50
        self.button_color = (70,130,100)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)

        # 创建按钮的rect对象（先临时初始化）
        self.rect = pygame.Rect(0,0,self.width,self.height)

        # 文本渲染
        self._prep_text(text)
                                      
        # 设置按钮最终位置
        self._apply_offset()

    def _prep_text(self,text):
        self.image = self.font.render(text,True,self.text_color,self.button_color)  
        # 根据文本图像更新rect尺寸
        self.rect = self.image.get_rect()

    def _apply_offset(self):     
        screen_center = self.screen.get_rect().center
        self.rect.center = (
            screen_center[0] + self.offset[0],  # 横向偏移
            screen_center[1] + self.offset[1]   # 纵向偏移
        )

    def check_click(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def set_difficulty(self):
        self.settings.initialize_difficulty(self.difficulty_level)

    def draw(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.image,self.text_rect)