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

import pygame
from plane_sprites import SCREEN_RECT, CREATE_ENEMY_EVENT, HERO_FIRE_EVENT
from plane_sprites import Background, Enemy, Hero


class PlaneGame:
    """飞机大战游戏主类"""

    def __init__(self):
        """初始化游戏"""
        print("🚀 游戏初始化中...")

        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        pygame.display.set_caption("飞机大战")

        # 游戏时钟
        self.clock = pygame.time.Clock()

        # 游戏状态
        self.game_over = False

        # 初始化精灵组
        self.__create_sprites()

        # 设置定时器
        self.__setup_timers()

        print("✅ 游戏初始化完成!")

    def __create_sprites(self) -> None:
        """创建游戏精灵和精灵组"""
        # 背景精灵（用于实现滚动效果）
        bg1 = Background()
        bg2 = Background(is_alt=True)

        # 英雄飞机
        self.hero = Hero()

        # 精灵组
        self.background_group = pygame.sprite.Group(bg1, bg2)
        self.hero_group = pygame.sprite.Group(self.hero)
        self.enemy_group = pygame.sprite.Group()

    def __setup_timers(self) -> None:
        """设置游戏定时器"""
        # 每隔1秒生成敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        # 每隔0.3秒发射子弹（更快的射速）
        pygame.time.set_timer(HERO_FIRE_EVENT, 300)

    def start_game(self) -> None:
        """启动游戏主循环"""
        print("🎮 游戏开始!")

        while not self.game_over:
            # 控制帧率
            self.clock.tick(60)

            # 游戏逻辑处理
            self.__handle_events()
            self.__check_collisions()
            self.__update_sprites()

            # 刷新显示
            pygame.display.flip()

        # 游戏结束处理
        self.__game_over()

    def __handle_events(self) -> None:
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                return

            elif event.type == CREATE_ENEMY_EVENT:
                self.__spawn_enemy()

            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # 键盘持续按键检测
        self.__handle_keyboard()

    def __handle_keyboard(self) -> None:
        """处理键盘输入"""
        keys = pygame.key.get_pressed()

        # === 水平移动控制 ===
        # 右箭头 或 D 键：向右移动
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.hero.speed = 5
        # 左箭头 或 A 键：向左移动
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.hero.speed = -5
        # 未按左右键：停止水平移动
        else:
            self.hero.speed = 0

        # === 垂直移动控制（新增）===
        # 上箭头 或 W 键：向上移动
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.hero.vertical_speed = -5  # 负数是向上
        # 下箭头 或 S 键：向下移动
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.hero.vertical_speed = 5  # 正数是向下
        # 未按上下键：停止垂直移动
        else:
            self.hero.vertical_speed = 0

        # === 其他控制 ===
        # 空格键：发射子弹
        if keys[pygame.K_SPACE]:
            self.hero.fire()

    def __spawn_enemy(self) -> None:
        """生成敌机"""
        enemy = Enemy()
        self.enemy_group.add(enemy)

    def __check_collisions(self) -> None:
        """检测碰撞"""
        # 子弹与敌机碰撞
        collisions = pygame.sprite.groupcollide(
            self.enemy_group,
            self.hero.bullets,  # 注意：这里使用修改后的属性名
            False,  # 不立即销毁敌机
            True  # 销毁子弹
        )

        # 处理被击中的敌机
        for enemy in collisions:
            # 每颗子弹造成1点伤害
            if enemy.take_damage(1):
                enemy.kill()  # 生命值为0时销毁

        # 英雄与敌机碰撞（游戏结束）
        if pygame.sprite.spritecollideany(self.hero, self.enemy_group):
            print("💥 英雄飞机被击中!")
            self.game_over = True

    def __update_sprites(self) -> None:
        """更新所有精灵"""
        # 绘制背景
        self.background_group.update()
        self.background_group.draw(self.screen)

        # 绘制敌机
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        # 绘制英雄
        self.hero_group.update()
        self.hero_group.draw(self.screen)

        # 绘制子弹
        self.hero.bullets.update()  # 注意：这里使用修改后的属性名
        self.hero.bullets.draw(self.screen)

    def __game_over(self) -> None:
        """游戏结束处理"""
        print("🎯 游戏结束!")
        print(f"最终击落敌机数: {len(self.enemy_group.sprites())}")

        # 显示结束信息
        font = pygame.font.Font("myfont.ttf", 24)
        game_over_text = font.render('游戏结束', True, (255, 50, 50))
        # screen.blit(game_over_text, ((SCREEN_RECT.width // 2, SCREEN_RECT.height // 2 - 30))
        score_text = font.render(f"击落敌机: {len(self.enemy_group.sprites())}", True, (255, 255, 0))

        text_rect = game_over_text.get_rect(center=(SCREEN_RECT.width // 2, SCREEN_RECT.height // 2 - 30))
        score_rect = score_text.get_rect(center=(SCREEN_RECT.width // 2, SCREEN_RECT.height // 2 + 30))

        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(score_text, score_rect)
        pygame.display.flip()

        pygame.quit()
        exit()


def main():
    """游戏入口函数"""
    try:
        # 初始化Pygame
        pygame.init()

        # 创建并运行游戏
        game = PlaneGame()
        game.start_game()

    except pygame.error as e:
        print(f"❌ Pygame错误: {e}")
    except Exception as e:
        print(f"❌ 游戏运行错误: {e}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()