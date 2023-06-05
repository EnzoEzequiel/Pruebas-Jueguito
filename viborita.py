import pygame
import random

# Dimensiones de la ventana del juego
WIDTH = 640
HEIGHT = 480

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Tamaño del cuerpo de la serpiente y velocidad
SEGMENT_SIZE = 20
SPEED = 20

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Función para mostrar el mensaje de fin de juego
def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Clase para representar la serpiente
class Snake:
    def __init__(self):
        self.segments = []
        self.direction = "right"
        self.grow()

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(screen, GREEN, segment)

    def move(self):
        head = self.segments[0].copy()
        if self.direction == "right":
            head.move_ip(SEGMENT_SIZE, 0)
        elif self.direction == "left":
            head.move_ip(-SEGMENT_SIZE, 0)
        elif self.direction == "up":
            head.move_ip(0, -SEGMENT_SIZE)
        elif self.direction == "down":
            head.move_ip(0, SEGMENT_SIZE)
        self.segments.insert(0, head)
        if len(self.segments) > 1:
            self.segments.pop()

    def grow(self):
        x = random.randint(1, (WIDTH-SEGMENT_SIZE)//SEGMENT_SIZE) * SEGMENT_SIZE
        y = random.randint(1, (HEIGHT-SEGMENT_SIZE)//SEGMENT_SIZE) * SEGMENT_SIZE
        self.segments.append(pygame.Rect(x, y, SEGMENT_SIZE, SEGMENT_SIZE))

    def check_collision(self):
        head = self.segments[0]
        if head.left < 0 or head.right > WIDTH or head.top < 0 or head.bottom > HEIGHT:
            return True
        for segment in self.segments[1:]:
            if head.colliderect(segment):
                return True
        return False

# Crear la serpiente
snake = Snake()

# Generar primera pieza de comida
food = pygame.Rect(random.randint(1, (WIDTH-SEGMENT_SIZE)//SEGMENT_SIZE) * SEGMENT_SIZE,
                   random.randint(1, (HEIGHT-SEGMENT_SIZE)//SEGMENT_SIZE) * SEGMENT_SIZE,
                   SEGMENT_SIZE, SEGMENT_SIZE)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.direction != "left":
                snake.direction = "right"
            elif event.key == pygame.K_LEFT and snake.direction != "right":
                snake.direction = "left"
            elif event.key == pygame.K_UP and snake.direction != "down":
                snake.direction = "up"
            elif event.key == pygame.K_DOWN and snake.direction != "up":
                snake.direction = "down"

    screen.fill(BLACK)

    snake.move()
    snake.draw()

    if snake.segments[0].colliderect(food):
        snake.grow()
        food = pygame.Rect(random.randint(1, (WIDTH-SEGMENT_SIZE)//SEGMENT_SIZE) * SEGMENT_SIZE,
                           random.randint(1, (HEIGHT-SEGMENT_SIZE)//SEGMENT_SIZE) * SEGMENT_SIZE,
                           SEGMENT_SIZE, SEGMENT_SIZE)

    pygame.draw.rect(screen, RED, food)

    if snake.check_collision():
        game_over()
        snake = Snake()

    pygame.display.flip()
    clock.tick(SPEED)

pygame.quit()
