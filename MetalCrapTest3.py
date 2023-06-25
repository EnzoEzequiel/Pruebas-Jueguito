import pygame
import random

obstacle = pygame.Rect(0, 520, 800, 80)
obstacleA = pygame.Rect(170, 310, 40, 40)
obstacleB = pygame.Rect(190, 340, 40, 40)
obstacleC = pygame.Rect(213, 380, 40, 40)
obstacleD = pygame.Rect(230, 410, 40, 40)
obstacleE = pygame.Rect(245, 440, 40, 40)
obstacleF = pygame.Rect(500, 435, 40, 40)
obstaculo_segundo_piso = pygame.Rect(0, 300, 800, 10)

# Dimensiones de la ventana del juego
WIDTH = 800
HEIGHT = 600

# Tamaño del jugador
PLAYER_WIDTH = 34
PLAYER_HEIGHT = 36

# Tamaño de la bala
BULLET_WIDTH = 10
BULLET_HEIGHT = 20

# Velocidad del jugador
PLAYER_SPEED = 7
JUMP_HEIGHT = 150
GRAVITY = 8

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


########################################################################################
###########################   pruebas  ########################################
#####################################################################################


class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        return image

# Función para mostrar el mensaje de fin de juego
def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("FIN DEL JUEGO", True, (255, 0, 0))
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
    
def prueba_colision(rect,superficies):
    contactos = []
    for superficie in superficies:
        if rect.colliderect(superficie):
            contactos.append(superficie)
    return contactos

def detectar_colision_obstaculo():
    #escalera izquierda
    if obstacleA.colliderect(rectangulo_jugador) or obstacleB.colliderect(rectangulo_jugador) or obstacleC.colliderect(rectangulo_jugador) or obstacleD.colliderect(rectangulo_jugador) or obstacleE.colliderect(rectangulo_jugador):
        # jugador.en_el_suelo = True  # Establecer al jugador en el suelo
        # jugador.rect.y = obstacleA.y - jugador.rect.height  # Ajustar la posición del jugador para que esté justo encima del obstáculo
        print("colision")
    else:
        print("no hay colision")
    
     
    if obstacle.colliderect(rectangulo_jugador):
        jugador.en_el_suelo = True  # Establecer al jugador en el suelo
        jugador.rect.y = obstacle.y - jugador.rect.height  # Ajustar la posición del jugador para que esté justo encima del obstáculo
    else:
        jugador.en_el_suelo = False  # Establecer al jugador en el aire


    
########################################################################################
#######################     JUGADOR     ################################################
########################################################################################

# Clase para representar al jugador
class Jugador:
    
    def __init__(self):
        
        self.muevo_izquierda = False
        self.esta_saltando = False
        self.en_el_suelo = True
        self.muevo_derecha = False
        self.se_mueve = False
        
        # Lista de rutas de imágenes
        rutas_imagenes = [r'C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\assetsSlug\img\player\MarcoAcciones\MarcoDerecho\Pistola\Camina\C0.png', 
                          r'C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\assetsSlug\img\player\MarcoAcciones\MarcoDerecho\Pistola\Camina\C1.png',
                          r'C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\assetsSlug\img\player\MarcoAcciones\MarcoDerecho\Pistola\Camina\C2.png',
                          r'C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\assetsSlug\img\player\MarcoAcciones\MarcoDerecho\Pistola\Camina\C3.png']

        self.caminata_frames = []
        
        # Iterar sobre las rutas de imágenes y cargarlas en la lista
        for ruta in rutas_imagenes:
            imagen_cargada = pygame.image.load(ruta).convert_alpha()
            self.caminata_frames.append(imagen_cargada)
            
        self.caminata_current_frame = 0
        
        torso = pygame.image.load(r'C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\assetsSlug\img\player\general\TorsoMarco.png').convert_alpha()
        piernas = pygame.image.load(r'C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\assetsSlug\img\player\general\piernasMarco.png').convert_alpha()
        salto = pygame.image.load(r'C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\assetsSlug\img\player\MarcoAcciones\MarcoDerecho\Pistola\EnSalto\0.png').convert_alpha()
        
        
        salto_sheet = SpriteSheet(salto)
        self.salto_frames = []
        for frame in range(1):
            image = salto_sheet.get_image(frame, 80, 110, 0.98)
            self.salto_frames.append(image)
        self.salto_current_frame = 0
        
        torso_sheet = SpriteSheet(torso)
        self.torso_frames = []
        for frame in range(4):
            image = torso_sheet.get_image(frame, PLAYER_WIDTH, PLAYER_HEIGHT, 2.5)
            self.torso_frames.append(image)
        self.torso_current_frame = 0

        piernas_sheet = SpriteSheet(piernas)
        self.piernas_frames = []
        for frame in range(1):
            image = piernas_sheet.get_image(frame, PLAYER_WIDTH, PLAYER_HEIGHT, 2.5)
            self.piernas_frames.append(image)
        self.piernas_current_frame = 0

        
        self.rect = self.torso_frames[self.torso_current_frame].get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - self.rect.height - 67
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.is_jumping = False
        self.jump_counter = 0
        self.frame_counter = 0
        self.is_reverse = False
        
########################################################################################
#######################     DIBUJO TECLAS     #########################################
########################################################################################

    def update(self, keys):
        
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.muevo_izquierda = True
            self.muevo_derecha = False
        else:
            self.muevo_derecha = False

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.muevo_izquierda = False
            self.muevo_derecha = True
        else:
            self.muevo_derecha = False
              
        if keys[pygame.K_UP] and self.en_el_suelo:
            self.esta_saltando = True
            self.en_el_suelo = False
            self.muevo_derecha = False
            self.jump_counter = 0

        if self.esta_saltando:
            self.rect.y -= GRAVITY
            self.jump_counter += GRAVITY

            if self.jump_counter >= JUMP_HEIGHT:
                self.esta_saltando = False
                self.en_el_suelo = False
                
        if not self.en_el_suelo:
            self.jump_counter += 1
        if self.en_el_suelo:
            self.jump_counter = 0 
            
        if self.muevo_derecha:
            self.frame_counter += 1
            if self.frame_counter >= 4:
                self.frame_counter = 0
                self.caminata_current_frame = (self.caminata_current_frame + 1) % len(self.caminata_frames)

            
        # Aplicar gravedad
        if not self.esta_saltando and not self.en_el_suelo and self.rect.y < HEIGHT - self.rect.height - 10:
            self.rect.y += GRAVITY
        elif self.rect.y >= HEIGHT - self.rect.height - 10:
            self.en_el_suelo = True

        # Limitar el movimiento del jugador dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # Actualizar animación de torso
        self.frame_counter += 0.50
        if self.frame_counter >= 5:
            self.frame_counter = 0
            if self.is_reverse:
                self.torso_current_frame -= 1
                if self.torso_current_frame < 0:
                    self.torso_current_frame = 1
                    self.is_reverse = False
            else:
                self.torso_current_frame = (self.torso_current_frame + 1) % len(self.torso_frames)
                if self.torso_current_frame == len(self.torso_frames) - 1:
                    self.is_reverse = True


########################################################################################
#######################     DIBUJO VIDAS       #########################################
########################################################################################

    def draw_lives(self):
        font = pygame.font.Font(None, 50)
        text = font.render("Vidas: " + str(self.lives), True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
########################################################################################
#######################     DIBUJO PERSONAJE   #########################################
########################################################################################
        
    def draw(self):
        salto_image = self.salto_frames[self.salto_current_frame]
        
        if self.esta_saltando and not self.en_el_suelo or self.jump_counter > 50:
            screen.blit(salto_image, self.rect)
            
        elif self.esta_saltando and not self.en_el_suelo:
            if self.muevo_izquierda:
                salto_image = pygame.transform.flip(salto_image, True, False)
            screen.blit(salto_image, self.rect)
            
        else:
            if self.muevo_izquierda:
                caminata_image = self.caminata_frames[self.caminata_current_frame]
                caminata_image = pygame.transform.flip(caminata_image, True, False)
                screen.blit(caminata_image, (self.rect.x, self.rect.y - 35))
                self.caminata_current_frame = (self.caminata_current_frame + 1) % len(self.caminata_frames)
                
            elif self.muevo_derecha:
                caminata_image = self.caminata_frames[self.caminata_current_frame]
                screen.blit(caminata_image, (self.rect.x, self.rect.y - 35))
                self.caminata_current_frame = (self.caminata_current_frame + 1) % len(self.caminata_frames)
                
            else:
                torso_image = self.torso_frames[self.torso_current_frame]
                piernas_image = self.piernas_frames[self.piernas_current_frame]
                
                if self.muevo_izquierda:
                    torso_image = pygame.transform.flip(torso_image, True, False)
                    piernas_image = pygame.transform.flip(piernas_image, True, False)
                    
                    screen.blit(piernas_image, self.rect)
                    screen.blit(torso_image, (self.rect.x - 6, self.rect.y + 1 - torso_image.get_height() + 60))
                else:
                    screen.blit(piernas_image, self.rect)
                    screen.blit(torso_image, (self.rect.x + 6, self.rect.y + 1 - torso_image.get_height() + 60))


########################################################################################
#######################     CLASES     #################################################
########################################################################################


# Clase para representar a las balas
class Bala:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BULLET_WIDTH, BULLET_HEIGHT)
        self.color = (255, 0, 0)
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Clase para representar a las balas de los enemigos
class BalaEnemiga:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BULLET_WIDTH, BULLET_HEIGHT)
        self.color = (0, 0, 255)
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Clase para representar a los enemigos

class Enemigo:
    def __init__(self, x, side):
        if side == "left":
            self.rect = pygame.Rect(x, jugador.rect.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        elif side == "right":
            self.rect = pygame.Rect(x, jugador.rect.y, -PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = (255, 0, 0)
        self.speed = ENEMY_SPEED
        self.side = side  

    def update(self):
        if self.side == "left":  
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        
        
########################################################################################
#######################     MAIN     #################################################
########################################################################################


# Listas para almacenar a las balas, enemigos y balas de los enemigos
balas = []
enemigos = []
balas_enemigas = []
# Crear al jugador
jugador = Jugador()

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
            bullet = Bala(jugador.rect.centerx, jugador.rect.y)
            balas.append(bullet)

    # Dibujar el fondo
    screen.fill((0, 0, 0))
    screen.blit(imagen_de_fondo, (0, 0))
    
    #dibujos de prueba
    pygame.draw.rect(screen, (255,0,0), obstacleA, 4)
    pygame.draw.rect(screen, (255,0,0), obstacleB, 4)
    pygame.draw.rect(screen, (255,0,0), obstacleC, 4)
    pygame.draw.rect(screen, (255,0,0), obstacleD, 4)
    pygame.draw.rect(screen, (255,0,0), obstacleE, 4)
    pygame.draw.rect(screen, (255,0,0), obstacleF, 4)
    pygame.draw.rect(screen, (0,0,255), obstaculo_segundo_piso, 4)
    
    
    rectangulo_jugador = jugador.rect.copy()  # Copiar el rectángulo del jugador
    rectangulo_jugador.y += jugador.speed  # Mover el rectángulo del jugador hacia abajo según su velocidad

    detectar_colision_obstaculo()
    
    jugador.update(keys)
    jugador.draw()
    jugador.draw_lives()
    
    # Actualizar y dibujar las balas del jugador
    for bullet in balas:
        bullet.update()
        bullet.draw()

        # Eliminar las balas que salen de la pantalla
        if bullet.rect.right > WIDTH:
            balas.remove(bullet)

    
    # Generar nuevos enemigos
    if random.randint(0, 100) < 1:
        side = random.choice(["left", "right"])
        if side == "left":
            x = 0
        elif side == "right":
            x = WIDTH - PLAYER_WIDTH
        enemigo = Enemigo(x, side)
        enemigos.append(enemigo)


    # Actualizar y dibujar los enemigos
    for enemigo in enemigos:
        enemigo.update()
        enemigo.draw()

        # Eliminar los enemigos que salen de la pantalla
        if enemigo.rect.right < 0:
            enemigos.remove(enemigo)

    # Actualizar y dibujar las balas de los enemigos
    for bullet in balas_enemigas:
        bullet.update()
        bullet.draw()

        # Eliminar las balas de los enemigos que salen de la pantalla
        if bullet.rect.right < 0 or bullet.rect.left > WIDTH:
            balas_enemigas.remove(bullet)

    # Comprobar colisiones entre balas del jugador y enemigos
    for bullet in balas:
        for enemigo in enemigos:
            if bullet.rect.colliderect(enemigo.rect):
                balas.remove(bullet)
                enemigos.remove(enemigo)

    # Comprobar colisiones entre balas de los enemigos y el jugador
    for bullet in balas_enemigas:
        if bullet.rect.colliderect(jugador.rect):
            jugador.lives -= 1
            balas_enemigas.remove(bullet)
            if jugador.lives == 0:
                game_over()

    # Disparar balas de los enemigos cada cierto tiempo
    if tiempo_actual - ultimo_disparo_enemigo > intervalo_disparo_enemigo:
        for enemigo in enemigos:
            bullet = BalaEnemiga(enemigo.rect.centerx, enemigo.rect.y)
            balas_enemigas.append(bullet)
        ultimo_disparo_enemigo = tiempo_actual

    pygame.display.flip()
    clock.tick(60)

# Cerrar Pygame al salir del juego
pygame.quit()
