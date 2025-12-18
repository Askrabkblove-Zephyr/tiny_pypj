"""
MIT License

Copyright (c) 2025 Askrabkblove-Zephyr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import random
import pygame

# 屏幕尺寸常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 敌机生成事件
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """游戏精灵基类"""

    def __init__(self, image_name: str, speed: int = 1):
        """
        初始化精灵

        Args:
            image_name: 图片文件路径
            speed: 移动速度，正数向下，负数向上
        """
        super().__init__()

        # 加载图像
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self) -> None:
        """更新精灵位置 - 垂直移动"""
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt: bool = False):
        """
        初始化背景

        Args:
            is_alt: 是否为第二张背景图（用于实现滚动效果）
        """
        super().__init__("./游戏素材/background.png", speed=1)

        # 如果是第二张背景图，初始位置在屏幕上方
        if is_alt:
            self.rect.bottom = 0

    def update(self) -> None:
        """更新背景位置（实现滚动效果）"""
        # 调用父类方法向下移动
        super().update()

        # 如果背景完全移出屏幕底部，重置到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.bottom = 0


class Enemy(GameSprite):
    """敌机精灵"""

    # 敌机类型配置
    ENEMY_TYPES = [
        {"image": "./游戏素材/enemy1.png", "health": 1},  # 小型敌机
        {"image": "./游戏素材/enemy2.png", "health": 2},  # 中型敌机
        {"image": "./游戏素材/enemy3_n1.png", "health": 3}  # 大型敌机
    ]

    def __init__(self):
        """随机初始化敌机"""
        # 随机选择敌机类型
        enemy_type = random.choice(self.ENEMY_TYPES)
        super().__init__(enemy_type["image"])

        # 敌机属性
        self.health = enemy_type["health"]
        self.speed = random.randint(1, 3)

        # 随机初始位置（水平方向）
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

        # 初始位置在屏幕上方
        self.rect.bottom = 0

    def take_damage(self, damage: int = 1) -> bool:
        """
        敌机受到伤害

        Args:
            damage: 伤害值

        Returns:
            bool: 敌机是否被摧毁
        """
        self.health -= damage
        return self.health <= 0

    def update(self) -> None:
        """更新敌机位置"""
        # 调用父类方法向下移动
        super().update()

        # 移出屏幕底部则销毁
        if self.rect.top >= SCREEN_RECT.height:
            self.kill()


class Hero(GameSprite):
    """英雄飞机精灵"""

    def __init__(self):
        """初始化英雄飞机"""
        super().__init__("./游戏素材/me1.png", speed=0)

        # 初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.height - 10

        # 子弹精灵组
        self.bullets = pygame.sprite.Group()

        # 添加垂直速度
        self.vertical_speed = 0

    def update(self) -> None:
        """更新英雄位置（水平和垂直移动）"""
        # 水平移动
        self.rect.x += self.speed

        # 垂直移动
        self.rect.y += self.vertical_speed

        # 边界检查 - 水平
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_RECT.width:
            self.rect.right = SCREEN_RECT.width

        # 边界检查 - 垂直
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_RECT.height:
            self.rect.bottom = SCREEN_RECT.height

    def fire(self) -> None:
        """发射子弹"""
        bullet = Bullet()

        # 设置子弹位置（从飞机正上方发射）
        bullet.rect.centerx = self.rect.centerx
        bullet.rect.bottom = self.rect.top

        # 添加到子弹组
        self.bullets.add(bullet)

class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):
        """初始化子弹"""
        super().__init__("./游戏素材/bullet1.png", speed=-5)  # 向上移动

    def update(self) -> None:
        """更新子弹位置"""
        super().update()

        # 移出屏幕顶部则销毁
        if self.rect.bottom <= 0:
            self.kill()
