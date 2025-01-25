from sprites import *
import sys

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Выбор уровня")

# Определение цветов
BLACK = (154, 205, 50)
WHITE = (255, 255, 255)

# Шрифты
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Определяем кнопки
first_level_button = pygame.Rect(440, 200, 400, 70)
second_level_button = pygame.Rect(440, 300, 400, 70)
third_level_button = pygame.Rect(440, 400, 400, 70)
menu_button = pygame.Rect(300, 500, 680, 70)


def draw_start_menu():
    screen.fill(BLACK)  # Заливаем экран черным цветом
    title_surface = font.render("Выберите режим", True, WHITE)  # Заголовок
    screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 120))  # Размещаем заголовок

    # Кнопка "Начать игру"
    pygame.draw.rect(screen, WHITE, first_level_button)
    first_level_text = button_font.render("Легкий", True, BLACK)
    screen.blit(first_level_text,
                (first_level_button.x + first_level_button.width // 2 - first_level_text.get_width() // 2,
                 first_level_button.y + first_level_button.height // 2 - first_level_text.get_height() // 2))

    # Кнопка "Рейтинг"
    pygame.draw.rect(screen, WHITE, second_level_button)
    second_level_text = button_font.render("Средний", True, BLACK)
    screen.blit(second_level_text,
                (second_level_button.x + second_level_button.width // 2 - second_level_text.get_width() // 2,
                 second_level_button.y + second_level_button.height // 2 - second_level_text.get_height() // 2))

    pygame.draw.rect(screen, WHITE, third_level_button)
    third_level_text = button_font.render("Сложный", True, BLACK)
    screen.blit(third_level_text,
                (third_level_button.x + third_level_button.width // 2 - third_level_text.get_width() // 2,
                 third_level_button.y + third_level_button.height // 2 - third_level_text.get_height() // 2))

    pygame.draw.rect(screen, WHITE, menu_button)
    menu_button_text = button_font.render("Меню", True, BLACK)
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
                    game = Game()
                    game.run(1)
                    break
                elif second_level_button.collidepoint(event.pos):
                    from main import Game
                    game = Game()
                    game.run(2)
                    break
                elif third_level_button.collidepoint(event.pos):
                    from main import Game
                    game = Game()
                    game.run(3)
                    break
                elif menu_button.collidepoint(event.pos):
                    import start_game
                    start_game.main()

        draw_start_menu()
