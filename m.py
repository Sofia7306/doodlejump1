import os
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Розміри вікна гри
pygame.display.set_caption("Doodle Jump")  # Заголовок вікна

# Функція для перевірки наявності файлів
def file_exists(file_path):
    if not os.path.isfile(file_path):
        print(f"Файл {file_path} не знайдений!")  # Якщо файл не знайдений, виводимо повідомлення
        return False
    return True

# Кольори для графіки
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)  # Колір коричневої платформи

# Завантаження фону та кнопок
background = pygame.image.load('background.png')  # Фонове зображення
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Масштабування фону

# Завантаження кнопок
menu_selected = pygame.image.load('menu_selected.png')  # Кнопка вибору
menu_unselected = pygame.image.load('menu_unselected.png')  # Кнопка не вибору
menu_selected = pygame.transform.scale(menu_selected, (200, 50))  # Масштабування
menu_unselected = pygame.transform.scale(menu_unselected, (200, 50))

# Завантаження зображення пружини
spring_image = pygame.image.load('spring.png')  # Завантаження зображення пружини
spring_image = pygame.transform.scale(spring_image, (40, 40))  # Масштабування пружини

# Клас для платформ (все що стосується платформ)
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, platform_type):
        super().__init__()
        self.image = pygame.image.load(image_path)  # Завантажуємо зображення платформи
        self.image = pygame.transform.scale(self.image, (60, 10))  # Масштабування платформи
        self.rect = self.image.get_rect()  # Отримуємо прямокутник для зіткнень
        self.rect.x = x  # Встановлюємо координати по осі X
        self.rect.y = y  # Встановлюємо координати по осі Y
        self.platform_type = platform_type  # Тип платформи (green, blue, brown)
        self.scored = False  # Позначка для рахунку
        self.broken = False  # Позначка для коричневої платформи (чи зламана)
        self.has_spring = False  # Чи є пружина на платформі
        if platform_type == 'brown' and random.random() < 0.2:  # 20% шанс, що на коричневій платформі буде пружина
            self.has_spring = True
            self.spring_rect = pygame.Rect(self.rect.x + 10, self.rect.y - 20, 40, 40)  # Розміщення пружини на платформі

    def update(self):
        # Видалення платформи, якщо вона вийшла за межі екрану
        if self.rect.top >= HEIGHT:
            self.kill()

# Клас для гравця
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('doodle.png')  # Завантаження зображення гравця
        self.image = pygame.transform.scale(self.image, (30, 30))  # Масштабування
        self.rect = self.image.get_rect()  # Отримуємо прямокутник для зіткнень
        self.rect.center = (WIDTH // 2, HEIGHT - 150)  # Встановлюємо початкову позицію
        self.speed_x = 0  # Початкова швидкість по осі X
        self.speed_y = 0  # Початкова швидкість по осі Y
        self.on_ground = False  # Перевірка, чи на землі
        self.max_jump_height = 15  # Максимальна висота стрибка

    def update(self):
        self.speed_y += 1  # Гравець відчуває гравітацію (постійне збільшення швидкості по Y)
        self.rect.x += self.speed_x  # Оновлюємо координати по X
        self.rect.y += self.speed_y  # Оновлюємо координати по Y

        hit_platforms = pygame.sprite.spritecollide(self, platforms, False)  # Перевірка зіткнень з платформами
        for platform in hit_platforms:
            if self.speed_y > 0 and self.rect.bottom <= platform.rect.top + self.speed_y:
                self.rect.bottom = platform.rect.top  # Встановлюємо гравця на платформу
                self.speed_y = -15  # Стрибок

                # Перевірка для коричневої платформи (якщо вона ще не зламана)
                if platform.platform_type == 'brown' and not platform.broken:
                    platform.broken = True  # Позначка для коричневої платформи, що вона зламана
                    self.speed_y = 5  # Знижуємо швидкість падіння

                # Якщо на платформі є пружина, то стрибок буде вищим
                if platform.has_spring:
                    self.speed_y = -self.speed_y * 1.5  # Збільшуємо висоту стрибка на 50%
                    platform.has_spring = False  # Вилучаємо пружину після використання

                # Збільшення рахунку, якщо платформа не була ще підрахована
                if not platform.scored:
                    global score
                    score += 1  # Збільшуємо рахунок
                    platform.scored = True  # Позначаємо платформу як підраховану

        # Обмеження гравця в межах екрану
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Створення гравця та платформ
player = Player()  # Створюємо гравця
platforms = pygame.sprite.Group()

# Початкова платформа, на якій спавниться персонаж
start_platform = Platform(WIDTH // 2 - 30, HEIGHT - 150, 'greenplatform.png', 'green')
platforms.add(start_platform)  # Додаємо її до групи платформ

# Генерація платформ
platform_count = 20  # Загальна кількість платформ
for _ in range(platform_count):
    x = random.randint(0, WIDTH - 60)  # Випадкова позиція по осі X
    y = random.randint(50, HEIGHT - 20)  # Випадкова позиція по осі Y
    platform_type = random.choices(['green', 'blue', 'brown'], [0.8, 0.1, 0.1], k=1)[0]  # Випадковий тип платформи

    # Створення платформи залежно від її типу
    if platform_type == 'green':
        platform = Platform(x, y, 'greenplatform.png', 'green')
    elif platform_type == 'blue':
        platform = Platform(x, y, 'blueplatform.png', 'blue')
    else:
        platform = Platform(x, y, 'brownplatform.png', 'brown')

    platforms.add(platform)

# Додаємо всі спрайти до основної групи
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(platforms)

score = 0  # Початковий рахунок
font = pygame.font.SysFont(None, 30)  # Шрифт для відображення тексту

# Функція для малювання кнопок
def draw_button(text, x, y, w, h, is_selected):
    if is_selected:
        screen.blit(menu_selected, (x, y))  # Вибрана кнопка
    else:
        screen.blit(menu_unselected, (x, y))  # Не вибрана кнопка
    
    button_text = font.render(text, True, BLACK)  # Текст на кнопці
    text_rect = button_text.get_rect(center=(x + w // 2, y + h // 2))  # Центрування тексту
    screen.blit(button_text, text_rect)

running = True
game_over = False
clock = pygame.time.Clock()  # Таймер для гри

# Основний цикл гри
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Якщо натискається закриття вікна, вийти з гри

        # Якщо гра завершена
        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()  # Позиція миші
                if replay_button.collidepoint(mx, my):  # Якщо натиснули на кнопку "Переграти"
                    player = Player()  # Створити нового гравця
                    platforms.empty()  # Очистити всі платформи
                    all_sprites.empty()  # Очистити всі спрайти
                    all_sprites.add(player)  # Додати нового гравця
                    platforms.add(start_platform)  # Додати початкову платформу
                    for _ in range(platform_count):  # Генерувати нові платформи
                        x = random.randint(0, WIDTH - 60)
                        y = random.randint(50, HEIGHT - 20)
                        platform_type = random.choices(['green', 'blue', 'brown'], [0.8, 0.1, 0.1], k=1)[0]
                        if platform_type == 'green':
                            platform = Platform(x, y, 'greenplatform.png', 'green')
                        elif platform_type == 'blue':
                            platform = Platform(x, y, 'blueplatform.png', 'blue')
                        else:
                            platform = Platform(x, y, 'brownplatform.png', 'brown')
                        platforms.add(platform)
                    all_sprites.add(platforms)  # Додати платформи до всіх спрайтів
                    score = 0  # Скинути рахунок
                    game_over = False  # Поновити гру

                elif exit_button.collidepoint(mx, my):  # Якщо натиснули на кнопку "Вийти"
                    running = False  # Вихід з гри

        # Якщо гра не завершена
        elif not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speed_x = -5  # Рух вліво
                elif event.key == pygame.K_RIGHT:
                    player.speed_x = 5  # Рух вправо
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player.speed_x = 0  # Зупинка гравця

    # Оновлення всіх спрайтів
    if not game_over:
        all_sprites.update()

        if player.rect.top <= HEIGHT // 3:
            offset = abs(player.speed_y)  # Якщо гравець знаходиться високо
            player.rect.y += offset
            for plat in platforms:
                plat.rect.y += offset
                if plat.rect.top >= HEIGHT:
                    if not plat.scored:
                        score += 1  # Збільшення рахунку, якщо платформа знищується
                        plat.scored = True
                    plat.kill()  # Видалити платформу з екрану
                    new_platform = Platform(random.randint(0, WIDTH - 60), random.randint(-100, -10), 'greenplatform.png', 'green')  # Додати нову платформу
                    platforms.add(new_platform)
                    all_sprites.add(new_platform)

        if player.rect.top > HEIGHT:
            game_over = True  # Якщо гравець падає, гра завершується

        screen.blit(background, (0, 0))  # Виведення фону
        all_sprites.draw(screen)  # Виведення всіх спрайтів

        # Малювання пружин на платформі
        for platform in platforms:
            if platform.has_spring:
                screen.blit(spring_image, platform.spring_rect.topleft)  # Малювання пружини на платформі

        # Виведення рахунку на екран
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    else:
        # Якщо гра завершена
        screen.fill(BLACK)  # Чорний фон
        game_over_text = pygame.font.SysFont(None, 60).render(f"Ви програли", True, WHITE)
        score_text = pygame.font.SysFont(None, 40).render(f"Рахунок: {score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

        # Малювання кнопок
        replay_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)
        exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)

        draw_button("Переграти", replay_button.x, replay_button.y, replay_button.width, replay_button.height, True)
        draw_button("Вийти", exit_button.x, exit_button.y, exit_button.width, exit_button.height, False)

    pygame.display.flip()  # Оновлення екрану
    clock.tick(60)  # Обмеження FPS

pygame.quit()  # Завершення роботи гри
