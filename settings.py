class Settings():
    """Класс для хранения всех настроек игры."""

    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (230,230,230) # Lavender

        self.start_background = (0 ,0, 0) # Black
        
        self.ship_limit = 2

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    
    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.3

        self.fleet_direction = 1 # 1 right, -1 left

        self.alien_points = 50
    

    def increase_speed(self):
        """Увеличивает настройки скорости."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
