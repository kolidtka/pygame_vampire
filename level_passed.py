import sys

from sprites import *

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Окно выигрыша")

# Определение цветов
GREEN = (154, 205, 50)
WHITE = (255, 255, 255)

# Шрифты
font = pygame.font.Font(None, 62)
button_font = pygame.font.Font(None, 50)

# Определяем кнопки
new_level_button = pygame.Rect(300, 200, 680, 70)
this_level_button = pygame.Rect(300, 300, 680, 70)
menu_button = pygame.Rect(300, 400, 680, 70)


def draw_mode_menu():
    """Отрисовка экрана выбора режима"""
    screen.fill(GREEN)  # Заливаем экран зеленым цветом
    title_surface = font.render("Вы победили! Хотите перейти на следующий уровень?", True, WHITE)  # Заголовок
    screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 120))  # Размещаем заголовок
    
    pygame.draw.rect(screen, WHITE, new_level_button)
    new_level = button_font.render("Да", True, GREEN)
    screen.blit(new_level,
                (new_level_button.x + new_level_button.width // 2 - new_level.get_width() // 2,
                 new_level_button.y + new_level_button.height // 2 - new_level.get_height() // 2))

    # Кнопка выбора "Среднего" режима
    pygame.draw.rect(screen, WHITE, this_level_button)
    this_level = button_font.render("Нет, хочу остаться на этом", True, GREEN)
    screen.blit(this_level,
                (this_level_button.x + this_level_button.width // 2 - this_level.get_width() // 2,
                 this_level_button.y + this_level_button.height // 2 - this_level.get_height() // 2))

    # Кнопка "Меню" (возвращение к стартовому окну)
    pygame.draw.rect(screen, WHITE, menu_button)
    menu_button_text = button_font.render("Меню", True, GREEN)
    screen.blit(menu_button_text, (menu_button.x + menu_button.width // 2 - menu_button_text.get_width() // 2,
                                   menu_button.y + menu_button.height // 2 - menu_button_text.get_height() // 2))

    pygame.display.flip()  # Обновляем экран


def main(mode):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_level_button.collidepoint(event.pos):
                    from main import Game
                    game = Game(min(3, mode + 1))
                    game.run()
                    break
                elif this_level_button.collidepoint(event.pos):
                    from main import Game
                    game = Game(min(3, mode))
                    game.run()
                    break
                elif menu_button.collidepoint(event.pos):
                    import start_game
                    start_game.main()

        draw_mode_menu()
