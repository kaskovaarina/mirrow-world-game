import arcade
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Зеркальный мир: Рекорды и 15 уровней"

GRAVITY = 0.6
JUMP_SPEED = 12
MOVEMENT_SPEED = 5
SAVE_FILE = "save.txt"

COLOR_BG_LIGHT = arcade.color.SKY_BLUE
COLOR_BG_DARK = arcade.color.BLACK

COLOR_PLATFORM_LIGHT = arcade.color.LIGHT_GREEN
COLOR_PLATFORM_DARK = arcade.color.MAGENTA

COLOR_ITEM = arcade.color.GOLD
COLOR_DOOR = arcade.color.CYAN

COLOR_TEXT_LIGHT = arcade.color.BLACK
COLOR_TEXT_DARK = arcade.color.WHITE

COLOR_PLAYER_LIGHT = arcade.color.WHITE
COLOR_PLAYER_DARK = arcade.color.VIOLET

# 15 уровней
LEVEL_DATA = [
    {"light": [(100, 50), (300, 150), (550, 250)], "dark": [(420, 200), (650, 300)], "items": [(420, 250)],
     "exit": (750, 340)},
    {"light": [(100, 50), (400, 200), (700, 400)], "dark": [(250, 120), (550, 300)], "items": [(250, 170), (550, 350)],
     "exit": (750, 480)},
    {"light": [(100, 50), (100, 250), (100, 450)], "dark": [(250, 150), (250, 350), (250, 550)],
     "items": [(250, 200), (100, 300)],
     "exit": (100, 530)},
    {"light": [(100, 50), (400, 200), (700, 350)], "dark": [(250, 125), (550, 275)], "items": [(250, 170)],
     "exit": (750, 450)},
    {"light": [(100, 50), (300, 150), (400, 250), (200, 350), (650, 460)], "dark": [(200, 100), (400, 200), (375, 400)],
     "items": [(400, 250)],
     "exit": (750, 550)},
    {"light": [(100, 50), (300, 50), (500, 50)], "dark": [(200, 150), (400, 150), (600, 150)], "items": [(400, 200)],
     "exit": (700, 200)},
    {"light": [(100, 50), (250, 200), (100, 350)], "dark": [(380, 125), (360, 275), (400, 425)], "items": [(365, 320)],
     "exit": (100, 500)},

    {"light": [(100, 50), (300, 100), (500, 100)], "dark": [(200, 150), (400, 250), (600, 350)], "items": [(600, 400)],
     "exit": (750, 450)},
    {"light": [(100, 50), (500, 50), (700, 200)], "dark": [(300, 50), (600, 120)], "items": [(300, 100)],
     "exit": (750, 300)},
    {"light": [(100, 50), (300, 250)], "dark": [(200, 150), (400, 350)], "items": [(400, 400)],
     "exit": (500, 450)},
    {"light": [(100, 50), (400, 100), (700, 100)], "dark": [(250, 180), (550, 250)], "items": [(550, 300)],
     "exit": (750, 350)},
    {"light": [(100, 50), (200, 150), (350, 250)], "dark": [(150, 100), (250, 200), (450, 300)], "items": [(350, 350)],
     "exit": (550, 350)},
    {"light": [(100, 50), (500, 400)], "dark": [(200, 150), (300, 250), (400, 350)], "items": [(300, 300)],
     "exit": (600, 450)},
    {"light": [(100, 50), (300, 100), (100, 200), (300, 300)], "dark": [(200, 150), (400, 250), (200, 350)],
     "items": [(400, 300)],
     "exit": (500, 400)},
    {"light": [(100, 50), (400, 250), (700, 450)], "dark": [(250, 150), (550, 350)], "items": [(600, 500)],
     "exit": (750, 550)}
]


def load_best_score():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return int(f.read().strip())
        except Exception:
            return 0
    return 0


def save_best_score(score: int):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        f.write(str(score))


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("ЗЕРКАЛЬНЫЙ МИР", SCREEN_WIDTH / 2, 450, arcade.color.WHITE, 40, anchor_x="center")
        arcade.draw_text("ENTER - начать | ESC - выход", SCREEN_WIDTH / 2, 320, arcade.color.WHITE, 18,
                         anchor_x="center")
        arcade.draw_text("Собери золото в тёмном мире и дойди до двери!", SCREEN_WIDTH / 2, 260,
                         arcade.color.LIGHT_GRAY, 14, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game = GameView()
            game.setup()
            self.window.show_view(game)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


class GameOverView(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score
        self.best = load_best_score()
        if self.score > self.best:
            save_best_score(self.score)
            self.best = self.score

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("ФИНАЛ ИГРЫ", SCREEN_WIDTH / 2, 420, arcade.color.WHITE, 30, anchor_x="center")
        arcade.draw_text(f"Ваш счет: {self.score}", SCREEN_WIDTH / 2, 320, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text(f"Лучший счет: {self.best}", SCREEN_WIDTH / 2, 280, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("ENTER - в меню", SCREEN_WIDTH / 2, 210, arcade.color.LIGHT_GRAY, 16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(MenuView())


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.light_world = True
        self.level = 1
        self.score = 0

        self.player_list = arcade.SpriteList()
        self.light_pl = arcade.SpriteList()
        self.dark_pl = arcade.SpriteList()
        self.items_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()

        self.player = None
        self.physics_engine = None

        self.text_score = arcade.Text("", 10, 10, arcade.color.WHITE, 14)

        try:
            self.collect_sound = arcade.load_sound(":resources:sounds/coin1.wav")
            self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        except Exception:
            self.collect_sound = None
            self.jump_sound = None


        self.player_textures_light = [
            arcade.make_soft_square_texture(30, COLOR_PLAYER_LIGHT, 255),
            arcade.make_soft_square_texture(30, arcade.color.LIGHT_SKY_BLUE, 255),
        ]
        self.player_textures_dark = [
            arcade.make_soft_square_texture(30, COLOR_PLAYER_DARK, 255),
            arcade.make_soft_square_texture(30, arcade.color.MEDIUM_PURPLE, 255),
        ]
        self.anim_timer = 0

    def setup(self):
        self.light_world = True
        self.anim_timer = 0

        self.player_list.clear()
        self.light_pl.clear()
        self.dark_pl.clear()
        self.items_list.clear()
        self.exit_list.clear()

        if self.level > len(LEVEL_DATA):
            self.window.show_view(GameOverView(self.score))
            return

        data = LEVEL_DATA[self.level - 1]

        for x, y in data["light"]:
            self.light_pl.append(arcade.SpriteSolidColor(120, 20, color=COLOR_PLATFORM_LIGHT, center_x=x, center_y=y))
        for x, y in data["dark"]:
            self.dark_pl.append(arcade.SpriteSolidColor(120, 20, color=COLOR_PLATFORM_DARK, center_x=x, center_y=y))
        for x, y in data["items"]:
            self.items_list.append(arcade.SpriteSolidColor(20, 20, color=COLOR_ITEM, center_x=x, center_y=y))

        ex, ey = data["exit"]
        door = arcade.SpriteSolidColor(40, 60, color=COLOR_DOOR, center_x=ex, center_y=ey)
        self.exit_list.append(door)

        self.player = arcade.Sprite()
        self.player.texture = self.player_textures_light[0]
        self.player.center_x, self.player.center_y = 100, 100
        self.player.change_x = 0
        self.player.change_y = 0
        self.player_list.append(self.player)

        self.update_physics()

    def update_physics(self):
        active_walls = self.light_pl if self.light_world else self.dark_pl
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, active_walls, GRAVITY)

    def on_draw(self):
        self.clear()

        if self.light_world:
            arcade.set_background_color(COLOR_BG_LIGHT)
            self.light_pl.draw()
            self.text_score.color = COLOR_TEXT_LIGHT
        else:
            arcade.set_background_color(COLOR_BG_DARK)
            self.dark_pl.draw()
            self.items_list.draw()
            self.text_score.color = COLOR_TEXT_DARK

        self.exit_list.draw()
        self.player_list.draw()

        self.text_score.text = f"Уровень: {self.level}/15 | Золото: {self.score}"
        self.text_score.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.light_world = not self.light_world
            self.update_physics()
            self.anim_timer = 0
            #сразу меняем цвет игрока основываясь на том, в каком мире он находится
            if self.light_world:
                self.player.texture = self.player_textures_light[0]
            else:
                self.player.texture = self.player_textures_dark[0]

        elif key in (arcade.key.W, arcade.key.UP) and self.physics_engine.can_jump():
            self.player.change_y = JUMP_SPEED
            if self.jump_sound:
                arcade.play_sound(self.jump_sound)

        elif key in (arcade.key.A, arcade.key.LEFT):
            self.player.change_x = -MOVEMENT_SPEED

        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.player.change_x = MOVEMENT_SPEED

        elif key == arcade.key.ESCAPE:
            self.window.show_view(MenuView())

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()

        #анимация игрока
        self.anim_timer += 1
        if self.anim_timer % 20 == 0:
            if self.light_world:
                self.player.texture = self.player_textures_light[(self.anim_timer // 20) % 2]
            else:
                self.player.texture = self.player_textures_dark[(self.anim_timer // 20) % 2]

        # сбор золота
        if not self.light_world:
            hits = arcade.check_for_collision_with_list(self.player, self.items_list)
            for item in hits:
                item.remove_from_sprite_lists()
                self.score += 1
                if self.collect_sound:
                    arcade.play_sound(self.collect_sound)

        # переход на следующий уровень
        if arcade.check_for_collision_with_list(self.player, self.exit_list):
            self.level += 1
            self.setup()

        # поражение, падение вниз
        if self.player.center_y < -50:
            self.score = max(0, self.score - 1)
            self.setup()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()