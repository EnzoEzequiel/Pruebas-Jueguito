import pygame
pygame.init()

screen_width = 800
screen_height = int(screen_width * 0.8)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Metal Slug")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# player action var
moving_left = False
moving_right = False

# define colours
BG = (144, 201, 120)

# Load player images for animation
player_idle = pygame.image.load("assets/img/player/idle.png")
player_walk_1 = pygame.image.load("assets/img/player/walk1.png")
player_walk_2 = pygame.image.load("assets/img/player/walk2.png")

player_idle = pygame.transform.scale(player_idle, (64, 64))
player_walk_1 = pygame.transform.scale(player_walk_1, (64, 64))
player_walk_2 = pygame.transform.scale(player_walk_2, (64, 64))

player_images = [player_idle, player_walk_1, player_walk_2]
player_index = 0
player_image = player_images[player_index]

player_rect = player_image.get_rect()
player_rect.center = (screen_width // 2, screen_height // 2)

# Animation timer
animation_timer = pygame.time.get_ticks()
animation_speed = 200  # Time between each frame (milliseconds)


def draw_bg():
    screen.fill(BG)


run = True
while run:

    clock.tick(FPS)
    draw_bg()

    # Update player animation
    if moving_left or moving_right:
        # Check if enough time has passed to update the animation
        if pygame.time.get_ticks() - animation_timer > animation_speed:
            player_index += 1
            if player_index >= len(player_images):
                player_index = 0
            player_image = player_images[player_index]
            animation_timer = pygame.time.get_ticks()

    screen.blit(player_image, player_rect)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False

        # Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()
