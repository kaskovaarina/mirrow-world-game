import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Зеркальный мир"
GRAVITY = 0.6
JUMP_SPEED = 12
MOVEMENT_SPEED = 5

class MirrorWorldGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.light_world = True
        self.level = 1
        self.score = 0
        self.player_list = arcade.SpriteList()
        self.light_pl= arcade.SpriteList()
        self.dark_pl = arcade.SpriteList()
        self.items_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()

        self.player = None
        self.physics_engine = None
        self.u_text = arcade.Text("", 10, 50, arcade.color.WHITE, 12)
        self.info_text = arcade.Text(
            "пробел - сменить мир, золото видно в темном мире, W/UP - прыжок",
            10, 20, arcade.color.WHITE, 10
        )

    def setup(self):
        self.light_world = True
        self.player_list.clear()
        self.light_pl.clear()
        self.dark_pl.clear()
        self.items_list.clear()
        self.exit_list.clear()

        if self.level == 1:
            light_pl = [(100, 50), (300, 150), (550, 250)]
            dark_pl = [(420, 200), (650, 300)]
            items = [(420, 250)]
            exit_pos = (750, 340)
        elif self.level == 2:
            light_pl = [(100, 50), (400, 200), (700, 400)]
            dark_pl = [(250, 120), (550, 300)]
            items = [(250, 170), (550, 350)]
            exit_pos = (750, 480)
        else:
            self.level = 1
            self.score = 0
            self.setup()
            return
        for x, y in light_pl:
            wall = arcade.SpriteSolidColor(120, 20, color=arcade.color.GREEN)
            wall.center_x, wall.center_y = x, y
            self.light_pl.append(wall)

        for x, y in dark_pl:
            wall = arcade.SpriteSolidColor(120, 20, color=arcade.color.RED)
            wall.center_x, wall.center_y = x, y
            self.dark_pl.append(wall)

        for x, y in items:
            item = arcade.SpriteSolidColor(20, 20, color=arcade.color.GOLD)
            item.center_x, item.center_y = x, y
            self.items_list.append(item)

        door = arcade.SpriteSolidColor(40, 60, color=arcade.color.BROWN)
        door.center_x, door.center_y = exit_pos
        self.exit_list.append(door)
        self.player = arcade.SpriteSolidColor(30, 30, color=arcade.color.WHITE)
        self.player.center_x, self.player.center_y = 100, 100
        self.player_list.append(self.player)
        self.update_physics()

    def update_physics(self):
        active_walls = self.light_pl if self.light_world else self.dark_pl
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, platforms=active_walls, gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()

        if self.light_world:
            self.background_color = arcade.color.SKY_BLUE
            self.light_pl.draw()
        else:
            self.background_color = arcade.color.BLACK
            self.dark_pl.draw()
            self.items_list.draw()

        self.exit_list.draw()
        self.player_list.draw()

        self.u_text.text = f"Уровень: {self.level} | Золото: {self.score}"
        self.u_text.draw()
        self.info_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.light_world = not self.light_world
            self.update_physics()
        elif key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()

        if not self.light_world:
            items_hit = arcade.check_for_collision_with_list(self.player, self.items_list)
            for item in items_hit:
                item.remove_from_sprite_lists()
                self.score += 1
        if arcade.check_for_collision_with_list(self.player, self.exit_list):
            self.level += 1
            self.setup()
        if self.player.center_y < -50:
            self.setup()

if __name__ == "__main__":
    game = MirrorWorldGame()
    game.setup()
    arcade.run()
