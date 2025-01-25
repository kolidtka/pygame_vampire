import pygame
from sprites import *
import sys

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Окно проигрыша")

# Определение цветов
BLACK = (154, 205, 50)
WHITE = (255, 255, 255)

# Шрифты
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Определяем кнопки
new_game_button = pygame.Rect(300, 200, 670, 70)
menu_button = pygame.Rect(300, 300, 670, 70)


def draw_start_menu():
    screen.fill(BLACK)  # Заливаем экран черным цветом
    title_surface = font.render("Вы проиграли!(", True, WHITE)  # Заголовок
    screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 70))  # Размещаем заголовок

    # Кнопка "Начать игру"
    pygame.draw.rect(screen, WHITE, new_game_button)
    start_text = button_font.render("Начать новую игру", True, BLACK)
    screen.blit(start_text, (new_game_button.x + new_game_button.width // 2 - start_text.get_width() // 2,
                             new_game_button.y + new_game_button.height // 2 - start_text.get_height() // 2))

    # Кнопка "Рейтинг"
    pygame.draw.rect(screen, WHITE, menu_button)
    rating_text = button_font.render("Меню", True, BLACK)
    screen.blit(rating_text, (menu_button.x + menu_button.width // 2 - rating_text.get_width() // 2,
                              menu_button.y + menu_button.height // 2 - rating_text.get_height() // 2))

    pygame.display.flip()  # Обновляем экран


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    from main import Game
                    game = Game()
                    game.run()
                    break
                elif menu_button.collidepoint(event.pos):
                    import start_game
                    start_game.main_loop()

        draw_start_menu()


if __name__ == "__main__":
    main_loop()
