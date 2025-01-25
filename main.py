import sys
from random import randint, choice
import pygame
from pytmx.util_pygame import load_pygame
from settings import *
from player import Player
from sprites import *
from groups import AllSprites


class Game:
    def __init__(self):
        pygame.init()  # Инициализация Pygame
        self.counter = 0
        # Установка области отображения (размера окна)
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Уцелевший')  # Установка заголовка окна
        self.clock = pygame.time.Clock()  # Установка таймера
        self.running = True  # Флаг для управления циклом игры

        # Группы спрайтов
        self.all_sprites = AllSprites()  # Все спрайты
        self.collision_sprites = pygame.sprite.Group()  # Спрайты для столкновения
        self.bullet_sprites = pygame.sprite.Group()  # Спрайты пуль
        self.enemy_sprites = pygame.sprite.Group()  # Спрайты врагов

        # Таймеры для стрельбы
        self.can_shoot = True  # Флаг, указывающий, может ли игрок стрелять
        self.shoot_time = 0  # Время последнего выстрела
        self.gun_cooldown = 100  # Время перезарядки (в миллисекундах)

        # Таймер для появления врагов
        self.enemy_event = pygame.event.custom_type()  # Создание пользовательского события для появления врагов
        pygame.time.set_timer(self.enemy_event, 500)  # Установка таймера на 500 мс
        self.spawn_positions = []  # Список позиций для появления врагов

        # Загрузка звуков
        self.shoot_sound = pygame.mixer.Sound(join("audio", "shoot.wav"))  # Звук выстрела
        self.shoot_sound.set_volume(0.4)  # Установка громкости
        self.impact_sound = pygame.mixer.Sound(join("audio", "impact.ogg"))  # Звук удара
        self.music = pygame.mixer.Sound(join("audio", "music.wav"))  # Фоновая музыка
        self.music.set_volume(0.3)  # Установка громкости музыки
        self.music.play(loops=-1)  # Включение музыки в бесконечном цикле

        # Загрузка изображений и настройка объектов игры
        self.load_images()  # Загрузка изображений
        self.setup()  # Настройка игры (загрузка карты и объектов)

    def load_images(self):
        # Загрузка изображения пули
        self.bullet_surf = pygame.image.load(join("images", "gun", "bullet.png")).convert_alpha()

        # Загрузка изображений врагов
        folders = list(walk(join("images", "enemies")))[0][1]  # Получение папок с изображениями врагов
        self.enemy_frames = {}  # Словарь для хранения кадров врагов
        for folder in folders:
            for folder_path, _, file_names in walk(join("images", "enemies", folder)):
                self.enemy_frames[folder] = []  # Инициализация списка кадров для врага
                for file_name in sorted(file_names, key=lambda n: int(n.split(".")[0])):
                    full_path = join(folder_path, file_name)  # Полный путь к изображению
                    surf = pygame.image.load(full_path).convert_alpha()  # Загрузка изображения
                    self.enemy_frames[folder].append(surf)  # Добавление изображения в список кадров

    def input(self):
        # Обработка ввода для стрельбы
        if pygame.mouse.get_pressed()[0] and self.can_shoot:  # Если нажата левая кнопка мыши
            self.shoot_sound.play()  # Воспроизведение звука выстрела
            pos = self.gun.rect.center + self.gun.player_direction * 50  # Позиция пули
            Bullet(self.bullet_surf, pos, self.gun.player_direction,
                   (self.all_sprites, self.bullet_sprites))  # Создание пули
            self.can_shoot = False  # Запрещаем стрелять до окончания перезарядки
            self.shoot_time = pygame.time.get_ticks()  # Обновляем время последнего выстрела

    def gun_timer(self):
        # Проверка времени для перезарядки
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()  # Текущее время
            if current_time - self.shoot_time >= self.gun_cooldown:  # Если прошло время перезарядки
                self.can_shoot = True  # Разрешаем стрелять

    def setup(self):
        # Загрузка уровня из TMX карты
        map = load_pygame(join("data", "maps", "world.tmx"))

        # Загрузка плиток земли
        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        # Загрузка объектов
        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        # Загрузка коллайдеров
        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        # Загрузка сущностей (Игрока и врагов)
        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                # Создание объекта игрока
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                # Создание оружия для игрока
                self.gun = Gun(self.player, self.all_sprites)
            else:
                # Сохранение позиций появления врагов
                self.spawn_positions.append((obj.x, obj.y))

    def bullet_collision(self):
        # Проверка столкновения пуль с врагами
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False,
                                                                pygame.sprite.collide_mask)
                if collision_sprites:  # Если есть столкновение
                    self.impact_sound.play()  # Воспроизведение звука удара
                    for sprite in collision_sprites:
                        sprite.destroy()  # Уничтожение врага
                        self.counter += 1
                    bullet.kill()  # Уничтожение пули

    def player_collision(self):
        # Проверка столкновения игрока с врагами
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False  # Остановка игры, если игрок столкнулся с врагом
            self.rating()
            import new_game_or_menu
            new_game_or_menu.main()

    def rating(self):
        with open("ratings.txt", 'a') as f:
            f.write(f"{self.counter}\n")

    def run(self, level):
        # Основной игровой цикл
        while self.running:
            dt = self.clock.tick() / 1000  # dt: время между кадрами

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  # Выход из игры при закрытии окна
                if event.type == self.enemy_event:
                    # Создание врага в случайной позиции из списка
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())),
                          (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites, level)

            # Обновление состояния игры
            self.gun_timer()  # Проверка времени для стрельбы
            self.input()  # Обработка ввода
            self.all_sprites.update(dt)  # Обновление всех спрайтов
            self.bullet_collision()  # Проверка столкновения пуль
            self.player_collision()  # Проверка столкновения игрока

            # Отрисовка на экране
            self.display_surface.fill('black')  # Очистка экрана
            self.all_sprites.draw(self.player.rect.center)  # Отрисовка всех спрайтов
            pygame.display.update()  # Обновление дисплея

        pygame.quit()  # Закрытие Pygame при выходе из игры
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
