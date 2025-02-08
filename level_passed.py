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
first_map_button = pygame.Rect(300, 200, 680, 70)
second_map_button = pygame.Rect(300, 300, 680, 70)
menu_button = pygame.Rect(300, 400, 680, 70)


def draw_mode_menu(mode):
    """Отрисовка экрана выбора режима"""
    screen.fill(GREEN)  # Заливаем экран зеленым цветом
    if mode == 1:
        title_surface = font.render("Вы победили! Хотите перейти на следующий уровень?", True, WHITE)  # Заголовок
        screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 120))  # Размещаем заголовок
    else:
        title_surface = font.render("Вы победили! Хотите перейти в свободный режим?", True, WHITE)  # Заголовок
        screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 120))  # Размещаем заголовок

    # Кнопка выбора следующего уровня/свободного режима
    pygame.draw.rect(screen, WHITE, first_map_button)
    first_map_text = button_font.render("Да", True, GREEN)
    screen.blit(first_map_text,
                (first_map_button.x + first_map_button.width // 2 - first_map_text.get_width() // 2,
                 first_map_button.y + first_map_button.height // 2 - first_map_text.get_height() // 2))

    # Кнопка выбора того же уровня/режима, на котором мы сейчас находимся
    pygame.draw.rect(screen, WHITE, second_map_button)
    second_map_text = button_font.render("Нет", True, GREEN)
    screen.blit(second_map_text,
                (second_map_button.x + second_map_button.width // 2 - second_map_text.get_width() // 2,
                 second_map_button.y + second_map_button.height // 2 - second_map_text.get_height() // 2))

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
                if first_map_button.collidepoint(event.pos):
                    from main import Game
                    game = Game(min(3, mode + 1))
                    game.run()
                    break
                elif second_map_button.collidepoint(event.pos):
                    if mode == 1:
                        from main import Game
                        game = Game(min(3, mode))
                        game.run()
                        break
                    else:
                        import levels
                        levels.main()
                elif menu_button.collidepoint(event.pos):
                    import start_game
                    start_game.main()

        draw_mode_menu(mode)
