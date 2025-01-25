from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()  # Загрузка изображений для анимации игрока
        self.state, self.frame_index = "down", 0  # Изначальное состояние и индекс кадра
        self.image = pygame.image.load(
            join('images', 'player', 'down', '0.png')).convert_alpha()  # Загрузка стартового изображения игрока
        self.rect = self.image.get_frect(center=pos)  # Установка прямоугольника изображения с заданным центром
        self.hitbox_rect = self.rect.inflate(-60, -90)  # Установка коллайдера, меньшего по размеру чем прямоугольник

        # movement
        self.direction = pygame.Vector2()  # Вектор направления движения
        self.speed = 500  # Скорость игрока
        self.collision_sprites = collision_sprites  # Группа спрайтов для проверки коллизий

    def load_images(self):
        """ Метод для загрузки изображений для анимации в зависимости от направления """
        self.frames = {
            "left": [],
            "right": [],
            "up": [],
            "down": [],
        }

        # Загрузка всех изображений для каждого состояния/направления
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join("images", "player", state)):
                if file_names:  # Если в папке есть файлы
                    for file_name in sorted(file_names, key=lambda x: int(x.split(".")[0])):
                        full_path = join(folder_path, file_name)  # Полный путь к изображению
                        surf = pygame.image.load(
                            full_path).convert_alpha()  # Загрузка изображения с поддержкой прозрачности
                        self.frames[state].append(surf)  # Добавление изображения в соответствующий список кадров

    def input(self):
        """ Метод для обработки ввода с клавиатуры """
        keys = pygame.key.get_pressed()  # Получение текущего состояния клавиш
        # Обновление направления движения в зависимости от нажатых клавиш
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        # Нормализация вектора направления (иправление скорости при диагональном движении)
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        """ Метод для перемещения игрока """
        self.hitbox_rect.x += self.direction.x * self.speed * dt  # Обновление положения по оси x
        self.collision("horizontal")  # Проверка коллизий по горизонтали
        self.hitbox_rect.y += self.direction.y * self.speed * dt  # Обновление положения по оси y
        self.collision("vertical")  # Проверка коллизий по вертикали
        self.rect.center = self.hitbox_rect.center  # Обновление RectИгрока к месту Collider

    def collision(self, direction):
        """ Метод для обработки коллизий с другими спрайтами """
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):  # Если есть коллизия с коллайдером
                if direction == "horizontal":  # Обработка столкновения по горизонтали
                    if self.direction.x > 0:  # Движение вправо
                        self.hitbox_rect.right = sprite.rect.left  # Обновление коллайдера
                    if self.direction.x < 0:  # Движение влево
                        self.hitbox_rect.left = sprite.rect.right  # Обновление коллайдера
                else:  # Обработка столкновения по вертикали
                    if self.direction.y < 0:  # Движение вверх
                        self.hitbox_rect.top = sprite.rect.bottom  # Обновление коллайдера
                    if self.direction.y > 0:  # Движение вниз
                        self.hitbox_rect.bottom = sprite.rect.top  # Обновление коллайдера

    def animate(self, dt):
        """ Метод для анимации игрока """
        if self.direction.x != 0:  # Если движется влево или вправо
            self.state = "right" if self.direction.x > 0 else "left"
        if self.direction.y != 0:  # Если движется вверх или вниз
            self.state = "down" if self.direction.y > 0 else "up"

        # Обновление индекса кадра для анимации
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        # Установка текущего изображения в зависимости от состояния и индекса кадра
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        """ Метод, вызываемый каждый кадр для обновления состояния игрока """
        self.input()  # Обработка ввода
        self.move(dt)  # Перемещение игрока
        self.animate(dt)  # Анимация
