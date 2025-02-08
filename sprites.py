from math import atan2, degrees

from settings import *


# Основной класс для спрайтов, наследующий от pygame.sprite.Sprite
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf  # Установка изображения спрайта
        self.rect = self.image.get_frect(topleft=pos)  # Установка прямоугольника спрайта с заданной позицией
        self.ground = True  # Переменная, указывающая на то, что спрайт находится на земле


# Класс для спрайта, который может сталкиваться с другими спрайтами
class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)  # Инициализация родительского класса с заданными группами
        self.image = surf  # Установка изображения коллайдера
        self.rect = self.image.get_frect(topleft=pos)  # Установка прямоугольника коллайдера с заданной позицией


# Класс для пушки, которую управляет игрок
class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        self.player = player  # Сохранение ссылки на игрока
        self.distance = 140  # Расстояние между игроком и пушкой
        self.player_direction = pygame.Vector2(1, 0)  # Начальное направление пушки (вправо)

        super().__init__(groups)
        self.gun_surf = pygame.image.load(
            join("images", "gun", "gun.png")).convert_alpha()  # Загрузка изображения пушки
        self.image = self.gun_surf  # Установка изображения пушки
        self.rect = self.image.get_frect(
            center=self.player.rect.center + self.player_direction * self.distance)  # Установка позиции пушки

    def get_direction(self):
        # Получение направления пушки по позиции курсора относительно центра окна
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()  # Нормализация вектора направления

    def rotate_gun(self):
        # Вращение пушки в зависимости от направления
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90  # Вычисление угла
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)  # Поворот изображения пушки
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle),
                                                   1)  # Поворот изображения пушки в другую сторону
            self.image = pygame.transform.flip(self.image, False, True)  # Отзеркаливание изображения пушки

    def update(self, _):
        # Обновление пушки на каждом кадре
        self.get_direction()  # Получение направления пушки
        self.rotate_gun()  # Поворот пушки
        self.rect.center = self.player.rect.center + self.player_direction * self.distance  # Установка позиции пушки


# Класс для пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf  # Установка изображения пули
        self.rect = self.image.get_frect(center=pos)  # Установка позиции пули
        self.spawn_time = pygame.time.get_ticks()  # Время появления пули
        self.lifetime = 500  # Длительность жизни пули в миллисекундах

        self.direction = direction  # Установка направления пули
        self.speed = 1200  # Скорость пули

    def update(self, dt):
        # Обновление позиции пули на каждом кадре
        self.rect.center += self.direction * self.speed * dt  # Перемещение пули

        # Удаление пули после истечения времени жизни
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()  # Уничтожение пули


# Класс для врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites, mode):
        super().__init__(groups)
        self.player = player  # Сохранение ссылки на игрока

        self.frames, self.frame_index = frames, 0  # Установка кадров для анимации врага и индекса кадров
        self.image = self.frames[self.frame_index]  # Установка текущего изображения врага
        self.animation_speed = 6  # Скорость анимации

        self.rect = self.image.get_frect(center=pos)  # Установка позиции врага
        self.hitbox_rect = self.rect.inflate(-20, -40)  # Установка коллайдера врага
        self.collision_sprites = collision_sprites  # Группа спрайтов для проверки коллизий
        self.direction = pygame.Vector2()  # Вектор направления врага
        if mode == 1:
            self.speed = 100  # Скорость врага
        elif mode == 2:
            self.speed = 200
        else:
            self.speed = 300

        self.death_time = 0  # Время смерти врага
        self.death_duration = 200  # Длительность смерти в миллисекундах

    def animate(self, dt):
        """ Обновление анимации врага """
        self.frame_index += self.animation_speed * dt  # Увеличение индекса кадра
        self.image = self.frames[
            int(self.frame_index) % len(self.frames)]  # Установка текущего изображения в зависимости от индекса

    def move(self, dt):
        """ Перемещение врага к игроку """
        player_pos = pygame.Vector2(self.player.rect.center)  # Позиция игрока
        enemy_pos = pygame.Vector2(self.rect.center)  # Позиция врага
        self.direction = (player_pos - enemy_pos).normalize()  # Обновление направления движения

        self.hitbox_rect.x += self.direction.x * self.speed * dt  # Перемещение врага по x
        self.collision("horizontal")  # Проверка коллизий по горизонтали
        self.hitbox_rect.y += self.direction.y * self.speed * dt  # Перемещение врага по y
        self.collision("vertical")  # Проверка коллизий по вертикали
        self.rect.center = self.hitbox_rect.center  # Обновление позиции врага

    def collision(self, direction):
        """ Метод для обработки коллизий врага """
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

    def destroy(self):
        """ Уничтожение врага """
        self.death_time = pygame.time.get_ticks()  # Запоминаем время смерти

        # Создание "маски" для эффекта уничтожения
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey("black")  # Установка черного цвета как прозрачного
        self.image = surf  # Обновление изображения врага

    def death_timer(self):
        """ Удаление врага после истечения времени смерти """
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()  # Уничтожение врага

    def update(self, dt):
        """ Метод, вызываемый каждый кадр для обновления состояния врага """
        if self.death_time == 0:
            self.move(dt)  # Перемещение врага
            self.animate(dt)  # Анимация врага
        else:
            self.death_timer()  # Проверка времени смерти врага
