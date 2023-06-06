import pygame
import random

# Dimensiones de la ventana del juego
WIDTH = 800
HEIGHT = 600

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Tamaño del jugador
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 80

# Tamaño de la bala
BULLET_WIDTH = 10
BULLET_HEIGHT = 20

# Velocidad del jugador
PLAYER_SPEED = 8
JUMP_HEIGHT = 150
GRAVITY = 5

# Velocidad de la bala
BULLET_SPEED = 10

# Velocidad del enemigo
ENEMY_SPEED = 5

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Cargar imágenes
player_image = pygame.image.load('assets/img/player/idle.png')
background_image = pygame.image.load('assets/img/background.png')

# Escalar imágenes
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Función para mostrar el mensaje de fin de juego
def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("FIN DEL JUEGO", True, RED)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    reset_game()

def reset_game():
    jugador.lives = 3
    balas.clear()
    enemigos.clear()
    balas_enemigas.clear()
    jugador.rect.x = 50
    jugador.rect.y = HEIGHT - jugador.rect.height - 10

# Clase para representar al jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.lives = 3
        self.is_jumping = False
        self.jump_counter = 0

        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        for i in range(5):
            img = pygame.image.load(f'assets/img/player/idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        # Actualizar animación
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

    def update(self, keys):
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP] and not self.is_jumping:
            self.is_jumping = True
            self.jump_counter = 0

        if self.is_jumping:
            dy = -GRAVITY * self.jump_counter
            self.jump_counter += 1
            if self.jump_counter == JUMP_HEIGHT:
                self.is_jumping = False
                self.jump_counter = 0

        # Actualizar posición del jugador
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.is_jumping = False
            self.jump_counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

# Clase para representar las balas del jugador
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)

# Clase para representar los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed = -self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

# Crear jugador
jugador = Player(50, HEIGHT - PLAYER_HEIGHT - 10, 0.3, PLAYER_SPEED)

# Crear grupos de sprites
balas = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas_enemigas = pygame.sprite.Group()

# Generar enemigos aleatorios
for _ in range(5):
    x = random.randint(100, WIDTH - 100)
    y = random.randint(50, HEIGHT - 200)
    enemigo = Enemy(x, y, ENEMY_SPEED)
    enemigos.add(enemigo)

# Game Loop
running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(balas) < 5:
                bala = Bullet(jugador.rect.centerx, jugador.rect.top, BULLET_SPEED)
                balas.add(bala)

    keys = pygame.key.get_pressed()
    jugador.update(keys)
    jugador.update_animation()
    jugador.draw()

    for bala in balas:
        bala.update()
        bala.draw()

        if pygame.sprite.spritecollide(bala, enemigos, True):
            balas.remove(bala)

        if bala.rect.bottom < 0:
            balas.remove(bala)

    for enemigo in enemigos:
        enemigo.update()
        enemigo.draw()

        if pygame.sprite.spritecollide(jugador, enemigos, True):
            jugador.lives -= 1
            if jugador.lives == 0:
                game_over()

    pygame.display.update()
    clock.tick(60)

# Salir del juego
pygame.quit()
