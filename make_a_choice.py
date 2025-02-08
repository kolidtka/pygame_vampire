import sys

from sprites import *

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Выбор карты")

# Определение цветов
GREEN = (154, 205, 50)
WHITE = (255, 255, 255)

# Шрифты
font = pygame.font.Font(None, 62)
button_font = pygame.font.Font(None, 50)

# Определяем кнопки
first_map_button = pygame.Rect(300, 200, 680, 70)
second_map_button = pygame.Rect(300, 300, 680, 70)
menu_button = pygame.Rect(300, 400, 680, 70)


def draw_mode_menu():
    """Отрисовка экрана выбора режима"""
    screen.fill(GREEN)  # Заливаем экран зеленым цветом
    title_surface = font.render("Выберите карту:", True, WHITE)  # Заголовок
    screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 120))  # Размещаем заголовок

    # Кнопка выбора карты первого уровня
    pygame.draw.rect(screen, WHITE, first_map_button)
    first_map_text = button_font.render("Карта первого уровня", True, GREEN)
    screen.blit(first_map_text,
                (first_map_button.x + first_map_button.width // 2 - first_map_text.get_width() // 2,
                 first_map_button.y + first_map_button.height // 2 - first_map_text.get_height() // 2))

    # Кнопка выбора карты второго уровня
    pygame.draw.rect(screen, WHITE, second_map_button)
    second_map_text = button_font.render("Карта второго уровня", True, GREEN)
    screen.blit(second_map_text,
                (second_map_button.x + second_map_button.width // 2 - second_map_text.get_width() // 2,
                 second_map_button.y + second_map_button.height // 2 - second_map_text.get_height() // 2))

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
                if first_map_button.collidepoint(event.pos):
                    from main import Game
                    game = Game(31)
                    game.run()
                    break
                elif second_map_button.collidepoint(event.pos):
                    from main import Game
                    game = Game(32)
                    game.run()
                    break
                elif menu_button.collidepoint(event.pos):
                    import start_game
                    start_game.main()

        draw_mode_menu()
