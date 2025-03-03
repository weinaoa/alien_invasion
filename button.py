import pygame.font

class Button(object):
    def __init__(self,ai_game,msg):
        """初始化按钮的属性"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.visible = True

        # 设置按钮的尺寸和其他游戏
        self.width,self.height = 200,50
        self.button_color = (255,0,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签秩序创建一次
        self._prep_msg(msg)
    
    def _prep_msg(self,msg):
        """将msg渲染为图像，并将其在按钮上居中"""
        self.msg_image = self.font.render(msg,True,self.text_color,
                                          None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制圆角按钮"""
        if self.visible:
            # 绘制圆角矩形
            pygame.draw.rect(
                self.screen, 
                self.button_color, 
                self.rect, 
                border_radius=15
            )
            # 精确居中文本
            text_x = self.rect.x + (self.width - self.msg_image.get_width()) // 2
            text_y = self.rect.y + (self.height - self.msg_image.get_height()) // 2
            self.screen.blit(self.msg_image, (text_x, text_y))