import arcade
import sqlite3
from datetime import datetime

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Зеркальный мир"

GRAVITY = 0.6
JUMP_SPEED = 12
MOVEMENT_SPEED = 5
DB_FILE = "scores.db"

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
COLOR_HIGHLIGHT = arcade.color.YELLOW

LEVEL_DATA = [
    {"light": [(100, 50), (300, 150), (550, 250)], "dark": [(420, 200), (650, 300)], "items": [(420, 250)], "exit": (750, 340)},
    {"light": [(100, 50), (400, 200), (700, 400)], "dark": [(250, 120), (550, 300)], "items": [(250, 170), (550, 350)], "exit": (750, 480)},
    {"light": [(100, 50), (100, 250), (100, 450)], "dark": [(250, 150), (250, 350), (250, 550)], "items": [(250, 200), (100, 300)], "exit": (100, 530)},
    {"light": [(100, 50), (400, 200), (700, 350)], "dark": [(250, 125), (550, 275)], "items": [(250, 170)], "exit": (750, 450)},
    {"light": [(100, 50), (300, 150), (400, 250), (200, 350), (630, 460)], "dark": [(200, 100), (400, 200), (375, 400)], "items": [(400, 250)], "exit": (750, 550)},
    {"light": [(100, 50), (300, 50), (500, 50)], "dark": [(200, 150), (400, 150), (600, 150)], "items": [(400, 200)], "exit": (700, 200)},
    {"light": [(100, 50), (250, 160), (100, 350)], "dark": [(380, 125), (360, 275), (400, 425)], "items": [(365, 320)], "exit": (100, 500)},
    {"light": [(100, 50), (300, 100), (500, 100)], "dark": [(200, 150), (400, 250), (600, 350)], "items": [(600, 400)], "exit": (750, 450)},
    {"light": [(100, 50), (500, 50), (700, 200)], "dark": [(300, 50), (600, 120)], "items": [(300, 100)], "exit": (750, 300)},
    {"light": [(100, 50), (300, 250)], "dark": [(200, 150), (400, 350)], "items": [(400, 400)], "exit": (500, 450)},
    {"light": [(100, 50), (400, 100), (700, 100)], "dark": [(250, 180), (550, 250)], "items": [(550, 300)], "exit": (750, 350)},
    {"light": [(100, 50), (200, 150), (350, 250)], "dark": [(150, 100), (250, 200), (450, 300)], "items": [(350, 350)], "exit": (550, 350)},
    {"light": [(100, 50), (500, 400)], "dark": [(200, 150), (300, 250), (400, 350)], "items": [(300, 300)], "exit": (600, 450)},
    {"light": [(100, 50), (300, 100), (100, 200), (300, 300)], "dark": [(200, 150), (400, 250), (200, 350)], "items": [(400, 300)], "exit": (500, 400)},
    {"light": [(100, 50), (400, 250), (700, 450)], "dark": [(250, 150), (550, 350)], "items": [(600, 500)], "exit": (750, 550)},
    {"light": [(100, 50), (250, 200), (500, 350)], "dark": [(150, 100), (400, 250), (450, 400)], "items": [(405, 280), (455, 430)], "exit": (750, 450)},
    {"light": [(100, 50), (300, 200), (100, 350), (300, 500)], "dark": [(200, 125), (200, 275), (200, 425)], "items": [(200, 175), (200, 325)], "exit": (200, 550)},
    {"light": [(50, 50), (200, 150), (350, 250), (500, 350), (650, 450)], "dark": [(125, 100), (275, 200), (425, 300), (575, 400)], "items": [(275, 250), (425, 350)], "exit": (750, 500)},
    {"light": [(100, 50), (400, 50), (650, 250)], "dark": [(250, 150), (450, 250), (250, 350)], "items": [(550, 300)], "exit": (700, 400)},
    {"light": [(100, 50), (100, 200), (300, 200), (500, 200), (700, 200)], "dark": [(200, 100), (400, 100), (600, 100), (200, 300), (400, 300)], "items": [(600, 150), (200, 350)], "exit": (600, 400)},
    {"light": [(100, 50), (300, 150), (500, 250), (700, 350)], "dark": [(200, 100), (400, 200), (600, 300)], "items": [(400, 250), (600, 350)], "exit": (750, 450)},
    {"light": [(100, 50), (250, 200), (400, 350), (550, 500)], "dark": [(175, 125), (325, 275), (475, 425)], "items": [(325, 325), (475, 475)], "exit": (650, 550)}
]

def init_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  player_name TEXT NOT NULL,
                  score INTEGER NOT NULL,
                  date TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def save_score(player_name, score):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO scores (player_name, score, date) VALUES (?, ?, ?)", (player_name, score, current_date))
    conn.commit()
    conn.close()

def get_top_scores(limit=10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT player_name, score, date FROM scores ORDER BY score DESC LIMIT ?", (limit,))
    results = c.fetchall()
    conn.close()
    return results

class NameInputView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_name = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        self.error_message = ""

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("ВВЕДИТЕ ВАШЕ ИМЯ", SCREEN_WIDTH / 2, 450, arcade.color.WHITE, 40, anchor_x="center")
        left = SCREEN_WIDTH / 2 - 200
        right = SCREEN_WIDTH / 2 + 200
        bottom = 325
        top = 375
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.DARK_GRAY)
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.WHITE, 2)
        display_text = self.player_name
        if self.cursor_visible and self.cursor_timer < 30:
            display_text += "|"
        arcade.draw_text(display_text, SCREEN_WIDTH / 2, 350, arcade.color.WHITE, 28, anchor_x="center", anchor_y="center")
        arcade.draw_text("ENTER - начать игру", SCREEN_WIDTH / 2, 280, arcade.color.LIGHT_GRAY, 18, anchor_x="center")
        arcade.draw_text("BACKSPACE - удалить символ", SCREEN_WIDTH / 2, 250, arcade.color.LIGHT_GRAY, 16, anchor_x="center")
        arcade.draw_text("ESC - выйти", SCREEN_WIDTH / 2, 220, arcade.color.LIGHT_GRAY, 16, anchor_x="center")
        if self.error_message:
            arcade.draw_text(self.error_message, SCREEN_WIDTH / 2, 180, arcade.color.RED, 16, anchor_x="center")

    def on_update(self, delta_time):
        self.cursor_timer += 1
        if self.cursor_timer >= 60:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            if self.player_name.strip():
                game = GameView(self.player_name.strip())
                game.setup()
                self.window.show_view(game)
            else:
                self.error_message = "Имя не может быть пустым!"
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.BACKSPACE:
            self.player_name = self.player_name[:-1]
            self.error_message = ""
        elif key == arcade.key.SPACE:
            if len(self.player_name) < 20:
                self.player_name += " "
                self.error_message = ""

    def on_key_release(self, symbol: int, modifiers: int):
        if 32 <= symbol <= 126:
            char = chr(symbol)
            if len(self.player_name) < 20:
                self.player_name += char
                self.error_message = ""

class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("ЗЕРКАЛЬНЫЙ МИР", SCREEN_WIDTH / 2, 450, arcade.color.WHITE, 40, anchor_x="center")
        arcade.draw_text("ENTER - начать | TAB - таблица лидеров | ESC - выход", SCREEN_WIDTH / 2, 320, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Собери золото в тёмном мире и дойди до двери!", SCREEN_WIDTH / 2, 260, arcade.color.LIGHT_GRAY, 14, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(NameInputView())
        elif key == arcade.key.TAB:
            self.window.show_view(LeaderboardView())
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class LeaderboardView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("ТАБЛИЦА ЛИДЕРОВ", SCREEN_WIDTH / 2, 550, arcade.color.YELLOW, 40, anchor_x="center")
        top_scores = get_top_scores(10)
        arcade.draw_text("Место", 100, 480, arcade.color.CYAN, 20, anchor_x="center")
        arcade.draw_text("Игрок", 300, 480, arcade.color.CYAN, 20, anchor_x="center")
        arcade.draw_text("Счет", 500, 480, arcade.color.CYAN, 20, anchor_x="center")
        arcade.draw_text("Дата", 700, 480, arcade.color.CYAN, 20, anchor_x="center")
        arcade.draw_line(50, 460, SCREEN_WIDTH - 50, 460, arcade.color.WHITE, 2)
        y_pos = 430
        for i, (name, score, date_str) in enumerate(top_scores, 1):
            place_color = arcade.color.GOLD if i == 1 else arcade.color.SILVER if i == 2 else arcade.color.COPPER if i == 3 else arcade.color.WHITE
            arcade.draw_text(str(i), 100, y_pos, place_color, 18, anchor_x="center")
            arcade.draw_text(name[:15], 300, y_pos, arcade.color.WHITE, 18, anchor_x="center")
            arcade.draw_text(str(score), 500, y_pos, arcade.color.GOLD, 18, anchor_x="center")
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                short_date = date_obj.strftime("%d.%m.%Y")
            except Exception:
                short_date = date_str[:10]
            arcade.draw_text(short_date, 700, y_pos, arcade.color.LIGHT_GRAY, 16, anchor_x="center")
            y_pos -= 35
        if not top_scores:
            arcade.draw_text("Пока нет результатов!", SCREEN_WIDTH / 2, 400, arcade.color.LIGHT_GRAY, 24, anchor_x="center")
        arcade.draw_text("ESC - в меню", SCREEN_WIDTH / 2, 100, arcade.color.LIGHT_GRAY, 16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MenuView())

class GameOverView(arcade.View):
    def __init__(self, player_name, score):
        super().__init__()
        self.player_name = player_name
        self.score = score
        save_score(player_name, score)
        self.top_scores = get_top_scores(10)
        self.player_place = None
        for i, (name, score_val, _) in enumerate(self.top_scores, 1):
            if name == player_name and score_val == score:
                self.player_place = i
                break

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)

    def on_draw(self):
        self.clear()
        panel_w = 620
        panel_h = 460
        panel_left = SCREEN_WIDTH / 2 - panel_w / 2
        panel_right = SCREEN_WIDTH / 2 + panel_w / 2
        panel_bottom = SCREEN_HEIGHT / 2 - panel_h / 2
        panel_top = SCREEN_HEIGHT / 2 + panel_h / 2
        arcade.draw_lrbt_rectangle_filled(
            panel_left + 8, panel_right + 8,
            panel_bottom - 8, panel_top - 8,
            arcade.color.BLACK_OLIVE
        )
        arcade.draw_lrbt_rectangle_filled(
            panel_left, panel_right,
            panel_bottom, panel_top,
            arcade.color.AIR_FORCE_BLUE
        )
        arcade.draw_lrbt_rectangle_outline(
            panel_left, panel_right,
            panel_bottom, panel_top,
            arcade.color.WHITE, 3
        )
        arcade.draw_text(
            "ИГРА ЗАВЕРШЕНА",
            SCREEN_WIDTH / 2, panel_top - 70,
            arcade.color.WHITE, 40,
            anchor_x="center"
        )
        arcade.draw_text(
            f"Игрок: {self.player_name}",
            SCREEN_WIDTH / 2, panel_top - 130,
            arcade.color.CYAN, 24,
            anchor_x="center"
        )
        arcade.draw_text(
            f"Ваш счёт: {self.score}",
            SCREEN_WIDTH / 2, panel_top - 170,
            arcade.color.GOLD, 26,
            anchor_x="center"
        )
        if self.player_place is not None:
            if self.player_place == 1:
                place_color = arcade.color.GOLD
            elif self.player_place == 2:
                place_color = arcade.color.SILVER
            elif self.player_place == 3:
                place_color = arcade.color.COPPER
            else:
                place_color = arcade.color.LIGHT_GREEN
            arcade.draw_text(
                f"Место в таблице лидеров: {self.player_place}",
                SCREEN_WIDTH / 2, panel_top - 210,
                place_color, 20,
                anchor_x="center"
            )
        arcade.draw_line(
            panel_left + 30, panel_top - 240,
            panel_right - 30, panel_top - 240,
            arcade.color.WHITE, 2
        )
        arcade.draw_text(
            "ТОП-5",
            SCREEN_WIDTH / 2, panel_top - 275,
            arcade.color.YELLOW, 24,
            anchor_x="center"
        )
        top5 = self.top_scores[:5]
        start_y = panel_top - 320
        row_h = 38
        for i, (name, score_val, date_str) in enumerate(top5, 1):
            y = start_y - (i - 1) * row_h
            is_me = (name == self.player_name and score_val == self.score)
            row_bg = arcade.color.DARK_SLATE_BLUE if is_me else arcade.color.AIR_FORCE_BLUE
            row_text = arcade.color.YELLOW if is_me else arcade.color.WHITE
            arcade.draw_lrbt_rectangle_filled(
                panel_left + 40, panel_right - 40,
                y - 10, y + 22,
                row_bg
            )
            arcade.draw_lrbt_rectangle_outline(
                panel_left + 40, panel_right - 40,
                y - 10, y + 22,
                arcade.color.WHITE, 1
            )
            arcade.draw_text(
                f"{i}.",
                panel_left + 60, y,
                row_text, 18
            )
            arcade.draw_text(
                f"{name[:18]}",
                panel_left + 95, y,
                row_text, 18
            )
            arcade.draw_text(
                f"{score_val}",
                panel_right - 70, y,
                arcade.color.GOLD, 18,
                anchor_x="right"
            )
        arcade.draw_text(
            "ENTER — в меню    |    TAB — таблица лидеров",
            SCREEN_WIDTH / 2, panel_bottom + 35,
            arcade.color.WHITE_SMOKE, 16,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(MenuView())
        elif key == arcade.key.TAB:
            self.window.show_view(LeaderboardView())

class GameView(arcade.View):
    def __init__(self, player_name):
        super().__init__()
        self.player_name = player_name
        self.light_world = True
        self.level = 1
        self.score = 0
        self.level_start_score = 0
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
        self.level_start_score = self.score
        self.player_list.clear()
        self.light_pl.clear()
        self.dark_pl.clear()
        self.items_list.clear()
        self.exit_list.clear()
        if self.level > len(LEVEL_DATA):
            self.window.show_view(GameOverView(self.player_name, self.score))
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
        self.text_score.text = f"Игрок: {self.player_name} | Уровень: {self.level}/22 | Золото: {self.score}"
        self.text_score.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.light_world = not self.light_world
            self.update_physics()
            self.anim_timer = 0
            self.player.texture = self.player_textures_light[0] if self.light_world else self.player_textures_dark[0]
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
        self.anim_timer += 1
        if self.anim_timer % 20 == 0:
            if self.light_world:
                self.player.texture = self.player_textures_light[(self.anim_timer // 20) % 2]
            else:
                self.player.texture = self.player_textures_dark[(self.anim_timer // 20) % 2]
        if not self.light_world:
            hits = arcade.check_for_collision_with_list(self.player, self.items_list)
            for item in hits:
                item.remove_from_sprite_lists()
                self.score += 1
                if self.collect_sound:
                    arcade.play_sound(self.collect_sound)
        if arcade.check_for_collision_with_list(self.player, self.exit_list):
            self.level += 1
            self.setup()
        if self.player.center_y < -50:
            self.score = self.level_start_score
            self.setup()

def main():
    init_database()
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(MenuView())
    arcade.run()

if __name__ == "__main__":
    main()