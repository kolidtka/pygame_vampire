from sprites import *
import sys

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Стартовое окно")

# Определение цветов
GREEN = (154, 205, 50)
WHITE = (255, 255, 255)

# Шрифты
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Определяем кнопки
start_button = pygame.Rect(300, 200, 670, 70)
rating_button = pygame.Rect(300, 300, 670, 70)
escape_button = pygame.Rect(300, 400, 670, 70)


def draw_start_menu():
    screen.fill(GREEN)  # Заливаем экран зеленым цветом
    title_surface = font.render("Стартовое окно", True, WHITE)  # Заголовок
    screen.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 120))  # Размещаем заголовок

    # Кнопка "Начать игру"
    pygame.draw.rect(screen, WHITE, start_button)
    start_text = button_font.render("Начать игру", True, GREEN)
    screen.blit(start_text, (start_button.x + start_button.width // 2 - start_text.get_width() // 2,
                             start_button.y + start_button.height // 2 - start_text.get_height() // 2))

    # Кнопка "Рейтинг"
    pygame.draw.rect(screen, WHITE, rating_button)
    rating_text = button_font.render("Рейтинг", True, GREEN)
    screen.blit(rating_text, (rating_button.x + rating_button.width // 2 - rating_text.get_width() // 2,
                              rating_button.y + rating_button.height // 2 - rating_text.get_height() // 2))

    # Кнопка "Выход"
    pygame.draw.rect(screen, WHITE, escape_button)
    escape_text = button_font.render("Выход", True, GREEN)
    screen.blit(escape_text, (escape_button.x + escape_button.width // 2 - escape_text.get_width() // 2,
                              escape_button.y + escape_button.height // 2 - escape_text.get_height() // 2))

    pygame.display.flip()  # Обновляем экран


def show_ranking():
    with open("ratings.txt", "r", encoding="utf-8") as file:
        first_line = file.readline().split("\n")[0]
        print(first_line)
        for cou_enem in file:
            print(int(cou_enem))
    print()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    import levels
                    levels.main()
                    break
                elif rating_button.collidepoint(event.pos):
                    show_ranking()
                elif escape_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        draw_start_menu()


if __name__ == "__main__":
    main()
