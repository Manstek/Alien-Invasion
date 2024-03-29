import sys #бибоиотека отвечающая за завершение игры
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from game_stats import GameStats
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.buttons = pygame.sprite.Group()
        self._create_buttons()



    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()


    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_lvl_buttons(mouse_pos)


    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()


    def _check_keyup_events(self, event):
        """Реагирует на отсспускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    

    def _create_buttons(self):
        """Создаёт игровые кнопки."""
        self.play_button = Button(self, "Play")
        
        screen_rect = self.screen.get_rect()
        self.play_button.rect.center = screen_rect.center
        self.play_button._prep_msg("Play")

        lvl_text = ('Lvl one', 'Lvl two', 'Lvl three')
        indentation = 80
        
        for text in lvl_text:
            button = Button(self, text)

            button.rect.x = self.play_button.rect.x
            button.rect.y = self.play_button.rect.bottom + self.play_button.height + lvl_text.index(text) * indentation

            button._prep_msg(text)
            self.buttons.add(button)


    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self._start_game()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            pygame.mouse.set_visible(False)
    

    def _check_lvl_buttons(self, mouse_pos):
        """Проверяет нажатие кнопок уровня и увеличивает скорость игры."""
        for index, button in enumerate(self.buttons.sprites()):
            buton_clicked = button.rect.collidepoint(mouse_pos)
            if buton_clicked:
                if index == 0:
                    self.settings.initialize_dynamic_settings()
                    self.settings.speedup_scale = 1.5
                    self._start_game()
                elif index == 1:
                    self.settings.initialize_dynamic_settings()
                    self.settings.speedup_scale = 2
                    self._start_game()
                elif index == 2:
                    self.settings.initialize_dynamic_settings()
                    self.settings.speedup_scale = 2.5
                    self._start_game()
            

    def _start_game(self):
        """Сбрасывает статистику, очищает группы пришельцев и патронов, запускает заново игру."""
        self.stats.reset_stats()
        self.stats.game_active = True

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()


    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        self.bullets.update()
            
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов c пришельцами."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        self._check_alien_bottom()
    

    def _create_fleet(self):
        """Создание флота прешельцев."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height + ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    

    def _check_alien_bottom(self):
        """Проверяет, добрались лм пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.sb.show_score()
        if not self.stats.game_active:
            self.screen.fill(self.settings.start_background)
            self.play_button.draw_button()
            for button in self.buttons.sprites():
                button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
