import sys

from sprites import *

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Выбор уровня")

# Определение цветов
GREEN = (154, 205, 50)
WHITE = (255, 255, 255)

# Шрифты
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Определяем кнопки
first_level_button = pygame.Rect(300, 200, 670, 70)
second_level_button = pygame.Rect(300, 300, 670, 70)
free_mode_button = pygame.Rect(300, 400, 670, 70)
menu_button = pygame.Rect(300, 500, 670, 70)


def draw_mode_menu():
    """Отрисовка экрана выбора режима"""
    screen.fill(GREEN)  # Заливаем экран зеленым цветом
    title_surface = font.render("Выберите уровень", True, WHITE)  # Заголовок
    screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 120))  # Размещаем заголовок

    # Кнопка выбора первого уровня
    pygame.draw.rect(screen, WHITE, first_level_button)
    first_level_text = button_font.render("Первый", True, GREEN)
    screen.blit(first_level_text,
                (first_level_button.x + first_level_button.width // 2 - first_level_text.get_width() // 2,
                 first_level_button.y + first_level_button.height // 2 - first_level_text.get_height() // 2))

    # Кнопка выбора второго уровня
    pygame.draw.rect(screen, WHITE, second_level_button)
    second_level_text = button_font.render("Второй", True, GREEN)
    screen.blit(second_level_text,
                (second_level_button.x + second_level_button.width // 2 - second_level_text.get_width() // 2,
                 second_level_button.y + second_level_button.height // 2 - second_level_text.get_height() // 2))

    # Кнопка выбора "свободного режима"
    pygame.draw.rect(screen, WHITE, free_mode_button)
    free_mode_text = button_font.render("Свободный режим", True, GREEN)
    screen.blit(free_mode_text,
                (free_mode_button.x + free_mode_button.width // 2 - free_mode_text.get_width() // 2,
                 free_mode_button.y + free_mode_button.height // 2 - free_mode_text.get_height() // 2))

    # Кнопка "Меню" (возвращение к стартовому окну)
    pygame.draw.rect(screen, WHITE, menu_button)
    menu_button_text = button_font.render("Меню", True, GREEN)
    screen.blit(menu_button_text, (menu_button.x + menu_button.width // 2 - menu_button_text.get_width() // 2,
                                   menu_button.y + menu_button.height // 2 - menu_button_text.get_height() // 2))

    pygame.display.flip()  # Обновляем экран


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if first_level_button.collidepoint(event.pos):
                    from main import Game
                    game = Game(1)
                    game.run()
                    break
                elif second_level_button.collidepoint(event.pos):
                    from main import Game
                    game = Game(2)
                    game.run()
                    break
                elif free_mode_button.collidepoint(event.pos):
                    import make_a_choice
                    make_a_choice.main()
                    break
                elif menu_button.collidepoint(event.pos):
                    import start_game
                    start_game.main()

        draw_mode_menu()
