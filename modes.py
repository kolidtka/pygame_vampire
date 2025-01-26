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
easy_mode_button = pygame.Rect(440, 200, 400, 70)
medium_mode_button = pygame.Rect(440, 300, 400, 70)
hard_mode_button = pygame.Rect(440, 400, 400, 70)
menu_button = pygame.Rect(300, 500, 680, 70)


def draw_mode_menu():
    """Отрисовка экрана выбора режима"""
    screen.fill(GREEN)  # Заливаем экран зеленым цветом
    title_surface = font.render("Выберите режим", True, WHITE)  # Заголовок
    screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 120))  # Размещаем заголовок

    # Кнопка выбора "Легкого" режима
    pygame.draw.rect(screen, WHITE, easy_mode_button)
    easy_mode_text = button_font.render("Легкий", True, GREEN)
    screen.blit(easy_mode_text,
                (easy_mode_button.x + easy_mode_button.width // 2 - easy_mode_text.get_width() // 2,
                 easy_mode_button.y + easy_mode_button.height // 2 - easy_mode_text.get_height() // 2))

    # Кнопка выбора "Среднего" режима
    pygame.draw.rect(screen, WHITE, medium_mode_button)
    medium_mode_text = button_font.render("Средний", True, GREEN)
    screen.blit(medium_mode_text,
                (medium_mode_button.x + medium_mode_button.width // 2 - medium_mode_text.get_width() // 2,
                 medium_mode_button.y + medium_mode_button.height // 2 - medium_mode_text.get_height() // 2))

    # Кнопка выбора "Тяжёлого" режима
    pygame.draw.rect(screen, WHITE, hard_mode_button)
    hard_mode_text = button_font.render("Сложный", True, GREEN)
    screen.blit(hard_mode_text,
                (hard_mode_button.x + hard_mode_button.width // 2 - hard_mode_text.get_width() // 2,
                 hard_mode_button.y + hard_mode_button.height // 2 - hard_mode_text.get_height() // 2))

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
                if easy_mode_button.collidepoint(event.pos):
                    from main import Game
                    game = Game()
                    game.run(1)
                    break
                elif medium_mode_button.collidepoint(event.pos):
                    from main import Game
                    game = Game()
                    game.run(2)
                    break
                elif hard_mode_button.collidepoint(event.pos):
                    from main import Game
                    game = Game()
                    game.run(3)
                    break
                elif menu_button.collidepoint(event.pos):
                    import start_game
                    start_game.main()

        draw_mode_menu()
