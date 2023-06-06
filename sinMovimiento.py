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

ultimo_disparo_enemigo = 0
intervalo_disparo_enemigo = 4000

imagen_de_fondo = pygame.image.load(r'C:\Users\enzoe\Pictures\Screenshots\Fondo.png')
imagen_de_fondo = pygame.transform.scale(imagen_de_fondo, (WIDTH, HEIGHT))

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

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
class Player:
    def __init__(self, char_type, x, y, scale, speed):
        # player_image = pygame.image.load(r'C:\Users\enzoe\Pictures\Screenshots\MarcoFirst.png')
        # player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        # self.image = player_image
        # self.rect = self.image.get_rect()
        # self.rect.x = 50
        # self.rect.y = HEIGHT - self.rect.height - 10
        # self.speed = PLAYER_SPEED
        self.lives = 3
        self.is_jumping = False
        self.jump_counter = 0
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False

        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        for i in range(5):
            img = pygame.image.load(
                f'assets/img/{self.char_type}/idle/{i}.png')
            img = pygame.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height()*scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0

        if moving_left:
            dx = - self.speed
            self.flip = True
            self.direction = - 1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # update rect positition
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image on current frame
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)


    def update(self, keys, camera_dx, camera_dy):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and not self.is_jumping:
            self.is_jumping = True
            self.jump_counter = 0

        if self.is_jumping:
            self.rect.y -= GRAVITY
            self.jump_counter += GRAVITY

            if self.jump_counter >= JUMP_HEIGHT:
                self.is_jumping = False

        # Aplicar gravedad
        if not self.is_jumping and self.rect.y < HEIGHT - self.rect.height - 10:
            self.rect.y += GRAVITY

        # Limitar el movimiento del jugador dentro de la pantalla
        if self.rect.left < -camera_dx:
            self.rect.left = -camera_dx
        if self.rect.right > WIDTH - camera_dx:
            self.rect.right = WIDTH - camera_dx

    def draw(self, camera_dx, camera_dy):
        screen.blit(self.image, (self.rect.x + camera_dx, self.rect.y + camera_dy))

# Clase para representar a las balas
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BULLET_WIDTH, BULLET_HEIGHT)
        self.color = RED
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.x += self.speed

    def draw(self, camera_dx, camera_dy):
        pygame.draw.rect(screen, self.color, (self.rect.x + camera_dx, self.rect.y + camera_dy, BULLET_WIDTH, BULLET_HEIGHT))

# Clase para representar a las balas de los enemigos
class EnemyBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BULLET_WIDTH, BULLET_HEIGHT)
        self.color = BLUE
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.x -= self.speed

    def draw(self, camera_dx, camera_dy):
        pygame.draw.rect(screen, self.color, (self.rect.x + camera_dx, self.rect.y + camera_dy, BULLET_WIDTH, BULLET_HEIGHT))

# Clase para representar a los enemigos
class Enemy:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = RED
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.x -= self.speed

    def draw(self, camera_dx, camera_dy):
        pygame.draw.rect(screen, self.color, (self.rect.x + camera_dx, self.rect.y + camera_dy, PLAYER_WIDTH, PLAYER_HEIGHT))

# Listas para almacenar a las balas, enemigos y balas de los enemigos
balas = []
enemigos = []
balas_enemigas = []

# Crear al jugador
jugador = Player('player', 200, 200, 3, 3)

# Posición de la cámara
camera_dx = 0
camera_dy = 0

# Bucle principal del juego
running = True
while running:
    tiempo_actual = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Disparar una bala cuando se presiona la tecla de espacio
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(jugador.rect.centerx, jugador.rect.y)
            balas.append(bullet)

    # Actualizar la posición de la cámara según la posición del jugador
    camera_dx = -(jugador.rect.x - WIDTH/2)

    screen.blit(imagen_de_fondo, (0, 0))

    jugador.update(keys, camera_dx, camera_dy)
    jugador.draw(camera_dx, camera_dy)

    # Actualizar y dibujar las balas del jugador
    for bullet in balas:
        bullet.update()
        bullet.draw(camera_dx, camera_dy)

        # Eliminar las balas que salen de la pantalla
        if bullet.rect.right > WIDTH:
            balas.remove(bullet)

    # Generar nuevos enemigos
    if random.randint(0, 100) < 2:
        enemy = Enemy(WIDTH)
        enemigos.append(enemy)

    # Enemigos disparan balas
    for enemy in enemigos:
        if tiempo_actual - ultimo_disparo_enemigo > intervalo_disparo_enemigo:
            bala_enemiga = EnemyBullet(enemy.rect.centerx, enemy.rect.y)
            balas_enemigas.append(bala_enemiga)
            ultimo_disparo_enemigo = tiempo_actual

    # Actualizar y dibujar las balas disparadas por los enemigos
    for bala_enemiga in balas_enemigas:
        bala_enemiga.update()
        bala_enemiga.draw(camera_dx, camera_dy)

        # Eliminar las balas que salen de la pantalla
        if bala_enemiga.rect.left < 0:
            balas_enemigas.remove(bala_enemiga)

    # Actualizar y dibujar a los enemigos
    for enemy in enemigos:
        enemy.update()
        enemy.draw(camera_dx, camera_dy)

        # Comprobar colisiones entre las balas y los enemigos
        for bullet in balas:
            if bullet.rect.colliderect(enemy.rect):
                balas.remove(bullet)
                enemigos.remove(enemy)
                break

        # Eliminar los enemigos que salen de la pantalla
        if enemy.rect.right < 0:
            enemigos.remove(enemy)

    # Comprobar colisiones entre las balas disparadas por los enemigos y el jugador
    for bala_enemiga in balas_enemigas:
        if bala_enemiga.rect.colliderect(jugador.rect):
            balas_enemigas.remove(bala_enemiga)
            jugador.lives -= 1
            break

    # Comprobar colisiones entre el jugador y los enemigos
    for enemy in enemigos:
        if jugador.rect.colliderect(enemy.rect):
            jugador.lives -= 1
            enemigos.remove(enemy)

    # Comprobar si el jugador ha perdido todas las vidas
    if jugador.lives <= 0:
        game_over()

    # Dibujar el contador de vidas
    font = pygame.font.Font(None, 36)
    text = font.render(f"Lives: {jugador.lives}", True, RED)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
