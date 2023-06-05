import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Movimiento del círculo")

# Definir los colores
black = (0, 0, 0)
white = (255, 255, 255)

# Definir las propiedades del círculo
circle_radius = 50
circle_x = screen_width // 2
circle_y = screen_height // 2

# Definir la velocidad de movimiento
circle_speed = 2

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Obtener el estado de las teclas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and circle_x > circle_radius:
        circle_x -= circle_speed
    if keys[pygame.K_RIGHT] and circle_x < screen_width - circle_radius:
        circle_x += circle_speed
    if keys[pygame.K_UP] and circle_y > circle_radius:
        circle_y -= circle_speed
    if keys[pygame.K_DOWN] and circle_y < screen_height - circle_radius:
        circle_y += circle_speed

    # Comprobar colisiones con los bordes de la ventana
    if circle_x - circle_radius < 0 or circle_x + circle_radius > screen_width:
        circle_speed *= -1
    if circle_y - circle_radius < 0 or circle_y + circle_radius > screen_height:
        circle_speed *= -1

    # Limpiar la pantalla
    screen.fill(black)

    # Dibujar el círculo
    pygame.draw.circle(screen, white, (circle_x, circle_y), circle_radius)

    # Actualizar la pantalla
    pygame.display.flip()
