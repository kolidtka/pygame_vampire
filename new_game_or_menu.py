import sys

from sprites import *

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Окно проигрыша")

# Определение цветов
GREEN = (154, 205, 50)
WHITE = (255, 255, 255)

# Шрифты
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Определяем кнопки
new_game_button = pygame.Rect(300, 200, 670, 70)
menu_button = pygame.Rect(300, 300, 670, 70)


def draw_start_menu():
    screen.fill(GREEN)  # Заливаем экран зеленым цветом
    title_surface = font.render("Вы проиграли!(", True, WHITE)  # Заголовок
    screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 120))  # Размещаем заголовок

    # Кнопка "Начать новую игру"
    pygame.draw.rect(screen, WHITE, new_game_button)
    new_game_text = button_font.render("Начать новую игру", True, GREEN)
    screen.blit(new_game_text, (new_game_button.x + new_game_button.width // 2 - new_game_text.get_width() // 2,
                                new_game_button.y + new_game_button.height // 2 - new_game_text.get_height() // 2))

    # Кнопка "Меню"
    pygame.draw.rect(screen, WHITE, menu_button)
    menu_text = button_font.render("Меню", True, GREEN)
    screen.blit(menu_text, (menu_button.x + menu_button.width // 2 - menu_text.get_width() // 2,
                            menu_button.y + menu_button.height // 2 - menu_text.get_height() // 2))

    pygame.display.flip()  # Обновляем экран


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    import levels
                    modes.main()
                    break
                elif menu_button.collidepoint(event.pos):
                    import start_game
                    start_game.main()

        draw_start_menu()
