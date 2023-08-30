class Settings():
    """Класс для хранения всех настроек игры."""

    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (230,230,230)
        self.ship_speed = 1.5
        self.ship_limit = 3

        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        self.alien_speed = 0.1
        self.fleet_drop_speed = 50
        self.fleet_direction = 1 # 1 - move right ; -1 - move left
