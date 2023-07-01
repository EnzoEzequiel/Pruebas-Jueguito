import pygame
import random
import recorte
import sqlite3


Ancho=800
Alto=480
VERDE=[0,255,0]
AZUL=[0,0,255]
ROJO=[255,0,0]
NEGRO=[0,0,0]
BLANCO=[255,255,255]
DORADO=[255,215,0]
#posicion de la imagen de fondo
fonx=0
fony=220

#lista de listas  con stats de precio vida y costo
stats=[[5,6,4,10,15],[1,2,1,5,8],[18,37,56,200,250]]


class MaCursor(pygame.sprite.Sprite):
    def __init__(self,pont):
        pygame.sprite.Sprite.__init__(self)
        self.image=pont
        self.rect=self.image.get_rect()
        self.rect.x=226
        self.rect.y=90
        self.opu=False # movimiento hacia arriba (up).
        self.opa=False # movimiento hacia abajo

    def update(self):
        """
        Actualiza la posición del cursor en respuesta a los comandos de movimiento.
        """
        if self.opu:
             if self.rect.y==90:
                 self.rect.y=210
                 self.opu=False
             else:
                 self.rect.y-=40
                 self.opu=False
        elif self.opa:
            if self.rect.y==210:
                self.rect.y=90
                self.opa=False
            else:
                self.rect.y+=40
                self.opa=False

class Enemigo (pygame.sprite.Sprite):
    def __init__(self,filas):
        pygame.sprite.Sprite.__init__(self)
        self.filas = filas
        self.id = 0
        self.accion = 1
        self.i = 0
        self.f = self.filas[self.accion]
        self.image = self.f[self.i]
        self.rect = self.image.get_rect()
        self.vida=[5,6,7,4,5,8,50,100]
        self.rect.x,self.rect.y = 10,Alto-190
        self.vel_x = -4
        self.radius = [40,70,80,30,50,50,30,60]
        self.damage=[1,2,1,3,3,5,10,15]
        self.espera=[[0,30],[0,30],[0,15],[0,20],[0,25],[0,30],[0,45],[0,45]]
        self.attack = False
        self.zona_ataque = None
        self.zona_muerte = None

    def update (self):
        """
        Actualiza la posición y el estado del enemigo.
        """
        self.rect.x+= self.vel_x
        self.f = self.filas[self.accion]
        self.i += 1
        if self.i >= len(self.f):
            self.i = 0
            self.attack = False
        self.image = self.f[self.i]


class Aliado (pygame.sprite.Sprite):
    def __init__(self,filas):
        pygame.sprite.Sprite.__init__(self)
        self.filas = filas
        self.accion = 1
        self.i = 0
        self.precio = stats[2]
        self.f = self.filas[self.accion]
        self.image = self.f[self.i]
        self.rect = self.image.get_rect()
        self.vida=[5,6,4,10,20]
        self.rect.x,self.rect.y = 10,Alto-190
        self.vel_x = 4
        self.zona_ataque = None
        self.zona_muerte = None
        self.radius = [40,50,50,20,40]
        self.damage=[1,2,1,5,8]
        #self.damage=[8,8,8,8,8] DAMAGE ALTO PARA PRUEBAS
        self.espera=[[0,30],[0,30],[0,15],[0,30],[0,45]]
        self.attack = False

    def update (self):
        """
        Actualiza la posición y el estado del aliado.
        """
        self.rect.x+= self.vel_x
        self.f = self.filas[self.accion]
        self.i += 1
        if self.i >= len(self.f):
            self.i = 0
            self.attack = False
        self.image = self.f[self.i]

class SelectAliado (pygame.sprite.Sprite):
    def __init__(self,id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40,80])
        self.id = id
        self.click = True
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = 5,Alto-100

class fuerte(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\Fuerte1.png")
        self.vida = 200
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = 0,170

if __name__ == '__main__':
    pygame.init()
    pantalla=pygame.display.set_mode([Ancho,Alto])
    pygame.display.flip()
    #segundos para el timer
    secs = 0
    mins = 0 
    hours = 0
    tiempoMax = ""
    tiempoRecordNivelUno = ""
    tiempoRecordNivelDos = ""
    font = pygame.font.Font(None,32)
    textTime = font.render("{}:{}:{}".format(hours,mins,secs), True, (255,255,255), (0,0,0))
    textTimeRect = textTime.get_rect()
    #centro el tiempo en el centro de la pantalla
    textTimeRect.center = Ancho//2.3, Alto//10

    '''--------------------------globales---------------------------------'''
    entuto = False
    nivel_dos = False
    oleadas = [7,1,5,4,2,3,1,0,5,2,3,4,3,2,1,3,2,1,1,0,0,6,1,5,4,2,3,1,0,5,2,3,4,3,2,1,3,2,1,1,0,0,]
    #oleadas = [7,6,5,4,3,2,1,0] #misma oleada pero mas corta
    #oleadas = [0,1,2,3,4,5,6,7] #arranca cn el boss final
    spawn = 30
    generation = 15
    '''--------------------------conexionBase---------------------------------'''
    conn = sqlite3.connect('BaseMetalSurvival.db')
    cursorBase = conn.cursor()
    '''--------------------------agrego nuevos datos de prueba---------------------------------'''
    # new_record = "01:11:11"  
    # new_record_nivel_dos = "02:22:22"  

    # cursor.execute("INSERT INTO TIEMPOS_RECORD (RECORD_NIVEL_UNO, RECORD_NIVEL_DOS) VALUES (?, ?)", (new_record, new_record_nivel_dos))
    # conn.commit()  # Guarda los cambios en la base de datos

    # cursorBase.execute("SELECT RECORD_NIVEL_UNO, RECORD_NIVEL_DOS FROM TIEMPOS_RECORD WHERE RECORD_NIVEL_UNO IS NOT NULL OR RECORD_NIVEL_DOS IS NOT NULL ORDER BY ID_RECORD DESC LIMIT 1")
    # result = cursorBase.fetchone()

    # Imprime el resultado obtenido
    # if result:
    #     print("Último registro nivel uno:", result)
    
    '''--------------------------globales---------------------------------'''
    fondotutorial=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\fondotutorial.jpeg")
    fuente= pygame.font.Font(None, 30)
    fuente2 = pygame.font.Font(None, 20)
    fondo=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\mapa.png")
    fondomapa=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\fondomapa.png")
    fondo_nivel_dos=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\mapaNivelDos.png")
    fondomapa_nivel_dos=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\fondomapaNivelDos.png")
    gameover=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\gameover.png")
    principal=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\principal.png")
    continuar=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\continuar.png")
    reiniciar=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\reiniciar.png")
    tutorial=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\tutorial.png")
    salir=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\salir.png")
    cursor=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\cursor.png")
    cursor2=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\cursor2.png")
    moneypng=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\Money.png")
    ost=pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\ost.ogg")
    ostgo=pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\GameOver.ogg")
    ostmomias=pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\segundoNivel.ogg")
    #txt_record_actual=fuente.render(tiempoMax, False, (255,255,255))
    txt_record_actual=fuente.render("RECORD Nvl1:", False, (255,255,255))
    txt_record_actual_Nvl2=fuente.render("RECORD Nvl2:", False, (255,255,255))
    cursorBase.execute("SELECT RECORD_NIVEL_UNO FROM TIEMPOS_RECORD WHERE RECORD_NIVEL_UNO IS NOT NULL ORDER BY ID_RECORD DESC LIMIT 1")
    resultUno = cursorBase.fetchone()
    record_actual_nivel_uno=fuente.render(str(resultUno[0]), False, (255,255,255))
    cursorBase.execute("SELECT RECORD_NIVEL_DOS FROM TIEMPOS_RECORD WHERE RECORD_NIVEL_DOS IS NOT NULL ORDER BY ID_RECORD DESC LIMIT 1")
    resultDos = cursorBase.fetchone()
    record_actual_nivel_dos=fuente.render(str(resultDos[0]), False, (255,255,255))
               
    ost.play(-1) #asi se reproduce indefinidamente
    
    infon=fondo.get_rect()
    #ost.set_volume(0.2)   #VOLUMEN
    spritesaliados = []
    '''recortes de todos los sprites aliados en la funcion recorte'''
    spritesaliados.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\marco.png"),[3,8,7,2],8,4))
    spritesaliados.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\ZombieTarma.png"),[12,24,12,11],24,4))
    spritesaliados.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\haduken.png"),[4,13,5,7],13,4))
    spritesaliados.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\tanque1.png"),[4,14,6,4],14,4))
    spritesaliados.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\MetalSlug.png"),[8,21,16],21))

    spritesenemigos = []
    '''-----------recortes de todos los sprites enemigos en la funcion recorte'''
    spritesenemigos.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\arabe.png"),[4,12,8,4],12,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\soldier.png"),[4,12,11],12,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\gunner.png"),[8,16,17,4],17,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\ufo.png"),[8,8,8,7],8,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\alien.png"),[16,16,17,21],21,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\towertank.png"),[2,6,6,6],6,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\cangrejo.png"),[7,12,12,7],12,4))
    spritesenemigos.append(recorte.recorte(pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\metalreal.png"),[5,7,31],31,4))


    sonialiadosatk = []
    '''--------------------Sonidos atauqe------------------------'''
    sonialiadosatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\marcoatk.ogg"))
    sonialiadosatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\zombiedisparo.ogg"))
    sonialiadosatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\ataqueprisionero.ogg"))
    sonialiadosatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\tanque1ataque.ogg"))
    sonialiadosatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\sfx_tanque.ogg"))


    sonialiadosmuerte = []
    '''--------------------Sonidos Muerte------------------------'''
    sonialiadosmuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\muertemarco.ogg"))
    sonialiadosmuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\muertezombie.ogg"))
    sonialiadosmuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\muertearabe.ogg"))
    sonialiadosmuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\tanque1muerte.ogg"))
    sonialiadosmuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\tanquemuerte.ogg"))

    sonienemigoatk = []
    '''--------------------Sonidos atauqe------------------------'''
    sonienemigoatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\arabeatk.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\soldadoatk.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\ataquegunner.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\atqueufo.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\ataquealien.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\towertankatk.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\cangrejoatk.ogg"))
    sonienemigoatk.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\metalrealatk.ogg"))
    


    sonienemigomuerte = []
    '''--------------------Sonidos Muerte------------------------'''
    sonienemigomuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\muertearabe.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\soldadomuerte.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\metralladoramuerte.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\muertealienyufo.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\muertealienyufo.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\towertankmuerte.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\cangrejomuerte.ogg"))
    sonienemigomuerte.append(pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\metalrealmuerte.ogg"))



    txt_salud=fuente.render("Salud", False, ROJO)
    txt_dama=fuente.render("Golpe", False, VERDE)
    txt_costo=fuente.render("Costo", False, DORADO)


    #grupo general
    todos = pygame.sprite.Group()
    aliados = pygame.sprite.Group()
    Selaliados = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    fuerte1 = fuerte()
    todos.add(fuerte1)
    fuerte2 = fuerte()
    fuerte2.image = pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sprites\Fuerte2.png")
    fuerte2.rect.x = 1884
    todos.add(fuerte2)

    #aliados
    for i in range (5):
        b = SelectAliado(i+1)
        b.rect.x = 81*i+150
        b.rect.y = Alto - 70
        b.image = spritesaliados[i][0][0]
        Selaliados.add(b)

    pos_y,pos_x=250,200
    reloj=pygame.time.Clock()
    
    pygame.display.flip()
    fin = False
    pausa = True
    punt1 = MaCursor(cursor)
    punt1.rect.x=8
    punt2 = MaCursor(cursor2)
    punt2.rect.x=162
    menu.add(punt1)
    menu.add(punt2)
    aux = 0
    findg = False #Fin de juego
    findgd = False #Fin de juego derrota
    findgv = True #Fin de juego victoria
    reprod = False
    money = 0
    seteoRecord_nivel_dos = False
    seteoRecord_nivel_uno = False
    
    #############################################################################################
    ####################   INICIO    ###########################################################
    #############################################################################################
    
    while not fin:
        for event in pygame.event.get():
            # Comprobación de eventos
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                # Acciones cuando se presiona una tecla
                if event.key == pygame.K_p:
                    # Pausa el juego o finaliza según la posición del cursor
                    if punt1.rect.y == 90:#continuar
                        start_time = pygame.time.get_ticks()
                        pausa = not pausa
                    elif punt1.rect.y == 210:#salir
                        fin = True
                    elif punt1.rect.y == 170:#tutorial seteo en true
                        entuto = not entuto
                    if punt1.rect.y == 130:#reiniciar
                        # Reinicia el juego eliminando a los aliados y enemigos,
                        # restablece la vida de los fuertes, reinicia variables y oleadas
                        start_time = 0
                        start_time = pygame.time.get_ticks()
                        secs = 0
                        mins = 0 
                        hours = 0
                        for a in aliados:
                            aliados.remove(a)
                            todos.remove(a)
                        for e in enemigos:
                            enemigos.remove(e)
                            todos.remove(e)
                        fuerte1.vida = 500
                        fuerte2.vida = 200
                        entuto = False
                        oleadas = [7,1,5,4,2,3,1,0,5,2,3,4,3,2,1,3,2,1,1,0,0,6,1,5,4,2,3,1,0,5,2,3,4,3,2,1,3,2,1,1,0,0,]
                        #oleadas = [7,6,5,4,3,2,1,0]
                        #oleadas = [0,1,2,3,4,5,6,7]
                        spawn = 30
                        generation = 15
                        money = 0
                        pausa = not pausa
                if event.key == pygame.K_UP:
                    # Mueve hacia arriba los elementos del menú
                    for e in menu:
                        e.opu = True
                if event.key == pygame.K_DOWN:
                    # Mueve hacia abajo los elementos del menú
                    for e in menu:
                        e.opa = True
            if event.type == pygame.KEYUP:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Acciones cuando se presiona un botón del ratón
                pos = pygame.mouse.get_pos()
                for b in Selaliados:
                    if b.rect.collidepoint(pos):
                        # Verifica si se hizo clic en un botón de aliado seleccionado
                        # y agrega el aliado correspondiente si se cumple la condición
                        if b.click and money >= stats[2][b.id-1]:
                            b.click = False
                            ali = Aliado(spritesaliados[b.id-1])
                            ali.damage = ali.damage[b.id-1]
                            ali.espera = ali.espera[b.id-1]
                            ali.vida = ali.vida[b.id-1]
                            ali.radius = ali.radius[b.id-1]
                            ali.precio = ali.precio[b.id-1]
                            ali.zona_ataque = sonialiadosatk[b.id-1]
                            ali.zona_muerte = sonialiadosmuerte[b.id-1]
                            money -= stats[2][b.id-1]
                            if b.id == 4:
                                ali.rect.y = Alto - 210
                            elif b.id == 5:
                                ali.rect.y = ali.rect.y - 10
                            aliados.add(ali)
                            todos.add(ali)
                            ali.rect.x=fonx+50
            if event.type == pygame.MOUSEBUTTONUP:
                # Acciones cuando se suelta un botón del ratón
                for c in enemigos:
                    c.click = False
                for b in Selaliados:
                    b.click = True

#########################################################################################
######################             IN GAME              #################################
#########################################################################################
        if pausa == False:
            current_time = pygame.time.get_ticks() - start_time

            millisecs = current_time // 1000
            secs = millisecs % 60
            mins = (millisecs // 60) % 60
            hours = (millisecs // 3600) % 60

                
            textTime = font.render(f"Tiempo: {hours:02d}:{mins:02d}:{secs:02d}", True, (255,255,255), (0,0,0))
            
            # Limitadores de pantalla en X
            posm = list(pygame.mouse.get_pos())

            # Limitador de desplazamiento hacia la izquierda
            if posm[0] > Ancho - 50:
                if fonx - 5 >= Ancho - infon[2]:
                    fonx -= 10
                    lsmov = todos
                    for e in lsmov:
                        e.rect.x -= 10

            # Limitador de desplazamiento hacia la derecha
            if posm[0] < 50:
                if fonx + 15 <= 0:
                    fonx += 10
                    lsmov = todos
                    for e in lsmov:
                        e.rect.x += 10

            # Incrementar la variable "money" si es menor que 1000
            if money < 100000:
                money += 1

            # Llenar la pantalla con color NEGRO
            pantalla.fill(NEGRO)
            
            if nivel_dos:
                # Dibujar el fondo del mapa
                pantalla.blit(fondomapa_nivel_dos, [0, 0])

                # Dibujar el fondo con desplazamiento en las coordenadas (fonx, fony)
                pantalla.blit(fondo_nivel_dos, [fonx, fony])
            else: 
                # Dibujar el fondo del mapa
                pantalla.blit(fondomapa, [0, 0])

                # Dibujar el fondo con desplazamiento en las coordenadas (fonx, fony)
                pantalla.blit(fondo, [fonx, fony])


            #Generacion de enemigos
            if generation == 0:
                # Si la generación actual es igual a 0
                if len(oleadas) > 0:
                    # Si hay oleadas restantes
                    enemy = oleadas.pop()
                    # Extrae la próxima oleada de la lista de oleadas y la asigna a la variable "enemy"
                    generation = (enemy+1)*spawn
                    # Calcula la generación actual basada en la oleada y el valor de "spawn"
                    c = Enemigo(spritesenemigos[enemy])
                    # Crea un nuevo objeto "Enemigo" con la imagen correspondiente a la oleada actual
                    c.id = enemy
                    c.radius = c.radius[enemy]
                    c.damage = c.damage[enemy]
                    c.espera = c.espera[enemy]
                    c.vida = c.vida[enemy]
                    c.zona_ataque = sonienemigoatk[enemy]
                    c.zona_muerte = sonienemigomuerte[enemy]
                    # Configura las propiedades del enemigo basadas en la oleada actual
                    enemigos.add(c)
                    todos.add(c)
                    c.rect.x, c.rect.bottom = infon[2] + fonx - 100, Alto - 134
                    # Agrega el enemigo a los grupos de sprites y establece su posición en la pantalla
                elif len(oleadas) == 0:
                    # Si no quedan más oleadas
                    findgv = True
                    findg = True
                    pausa = True
                    # Establece las variables para finalizar el juego y pausarlo

            else:
                # Si la generación actual no es 0
                generation -= 1
                # Reduce en 1 el valor de la generación actual


            #Colision enemigo llega a rango aliado
            for e in enemigos:
                for a in aliados:
                    if a.vida > 0 and e.vida > 0:
                        alcance=pygame.sprite.collide_circle(e,a)# si hay colision en un rango circular
                        if alcance:
                            for i9 in range (e.vida):
                                pygame.draw.circle(pantalla, ROJO, [5+e.rect.left+i9*7, e.rect.top-5], 2)
                                #DIBUJA circulos que representen cada punto de vida
                            a.vel_x = 0
                            a.accion = 0
                            if a.attack:
                                a.accion = 2
                            if a.espera[0]<=0:
                                a.i = 0
                                e.vida-=a.damage
                                a.zona_ataque.play()
                                a.attack = True
                                a.espera[0]=a.espera[1]
                            else:
                                a.espera[0]-=1

                #Colision aliado llega a rango enemigo
            for a in aliados:
                for e in enemigos:
                    if a.vida > 0 and e.vida > 0:
                        alcance=pygame.sprite.collide_circle(a,e)
                        if alcance:
                            for i9 in range (a.vida):
                                #DIBUJO LA VIDA DEL aliado CON CIRCULITOS
                                pygame.draw.circle(pantalla, VERDE, [5+a.rect.left+i9*7, a.rect.top-5], 2)
                            e.vel_x = 0
                            e.accion = 0
                            if e.attack:
                                e.accion = 2
                            if e.espera[0]<=0:
                                e.i = 0
                                e.zona_ataque.play()
                                a.vida-=e.damage
                                e.attack = True
                                e.espera[0]=e.espera[1]
                            else:
                                e.espera[0]-=1

            #Colision enemigo llega a fuerte aliado
            for e in enemigos:
                a=fuerte1
                if a.vida > 0 and e.vida > 0:
                    alcance=pygame.sprite.collide_circle(a,e)
                    if alcance:
                        for i in range (a.vida):
                            #DIBUJO LA VIDA DEL FUERTE CON 200 CIRCULITOS
                            pygame.draw.circle(pantalla, ROJO, [a.rect.left+i, a.rect.top-5], 2)
                        e.vel_x = 0
                        e.accion = 0
                        if e.attack:
                            e.accion = 2
                        if e.espera[0]<=0:
                            e.i = 0
                            e.zona_ataque.play()
                            a.vida-=e.damage
                            e.attack = True
                            e.espera[0]=e.espera[1]
                        else:
                            e.espera[0]-=1
                elif a.vida<=0:
                    findg = True
                    findgd = True
                    pausa = True

            for e in aliados:
                a=fuerte2
                if a.vida > 0 and e.vida > 0:
                    alcance=pygame.sprite.collide_circle(a,e)
                    if alcance:
                        for i in range (a.vida):
                            #DIBUJO LA VIDA DEL FUERTE CON 200 CIRCULITOS
                            pygame.draw.circle(pantalla, ROJO, [a.rect.left+i, a.rect.top-5], 2)
                        e.vel_x = 0
                        e.accion = 0
                        if e.attack:
                            e.accion = 2
                        if e.espera[0]<=0:
                            e.i = 0
                            e.zona_ataque.play()
                            a.vida-=e.damage
                            e.attack = True
                            e.espera[0]=e.espera[1]
                        else:
                            e.espera[0]-=1
                #disparo de estados del juego
                elif a.vida<=0:
                    tiempoMax = font.render(f"Tiempo Alcanzado: {hours:02d}:{mins:02d}:{secs:02d}", True, (255,255,255), (0,0,0))
                    tiempoComparativo = f"{hours:02d}:{mins:02d}:{secs:02d}"
                    tiempoMaxRect = tiempoMax.get_rect()
                    #centro el tiempo en el centro de la pantalla
                    tiempoMaxRect.scale_by(2)
                    tiempoMaxRect.center = Ancho//2, Alto//0.5
                    #HORAS MINUTOS Y SEGUNDOS DE TIEMPO COMPARATIVO
                    horaC=(int(tiempoComparativo.split(':')[0]))
                    minC=(int(tiempoComparativo.split(':')[1]))
                    secC=(int(tiempoComparativo.split(':')[2]))
                    
                    
                    #HORAS MINUTOS Y SEGUNDOS DE nivel uno
                    horaR=(int(resultUno[0].split(':')[0]))
                    minR=(int(resultUno[0].split(':')[1]))
                    secR=(int(resultUno[0].split(':')[2]))
                    
                    #HORAS MINUTOS Y SEGUNDOS DE nivel dos
                    horaR2=(int(resultDos[0].split(':')[0]))
                    minR2=(int(resultDos[0].split(':')[1]))
                    secR2=(int(resultDos[0].split(':')[2]))
                    
                    if not seteoRecord_nivel_dos:
                        #---------------------RECORDS------------------------
                        
                        if (horaC < horaR2 or (horaR2 == horaC and  minC < minR2) or ( horaC == horaR2  and minC == minR2 and secC < secR2)) and nivel_dos:
                            print("ENTRO A RECORDS NIVEL DOS!!!!!")
                            print(tiempoComparativo)
                            seteoRecord_nivel_dos = True
                            cursorBase.execute("INSERT INTO TIEMPOS_RECORD (RECORD_NIVEL_UNO, RECORD_NIVEL_DOS) VALUES (?, ?)", (None, tiempoComparativo))
                            conn.commit()  # Guarda los cambios en la base de datos
                    
                    if not seteoRecord_nivel_uno:
                        if horaC < horaR or (horaR == horaC and  minC < minR) or ( horaC == horaR  and minC == minR and secC < secR):
                            print("ENTRO A RECORDS NIVEL UNOOOOOOOOO!!!!!")
                            print(tiempoComparativo)
                            seteoRecord_nivel_uno = True
                            cursorBase.execute("INSERT INTO TIEMPOS_RECORD (RECORD_NIVEL_UNO, RECORD_NIVEL_DOS) VALUES (?, ?)", (tiempoComparativo, None))
                            conn.commit()  # Guarda los cambios en la base de datos
                        
                    findg = True
                    findgv = True
                    pausa = True
            #Eliminacion vida=0
            for a in aliados:
                for e in enemigos:
                    if e.vida <= 0 or a.vida <= 0:
                        for a2 in aliados:
                            a2.vel_x = 4
                            a2.accion = 1
                        for e2 in enemigos:
                            e2.vel_x = -4
                            e2.accion = 1
                        if e.vida<=0:
                            e.zona_muerte.play()
                            enemigos.remove(e)
                            todos.remove(e)
                        if a.vida<=0:
                            a.zona_muerte.play()
                            aliados.remove(a)
                            todos.remove(a)
            #DIBUJO BAJA NEGRA BLITEANDO EL TEXTO DEL COSTO DAÑO Y SALUD 
            pygame.draw.polygon(pantalla, NEGRO, [(0,Alto-120),(0,Alto),(Ancho,Alto),(Ancho,Alto-120)])
            pantalla.blit(txt_salud,[30, Alto-90])
            pantalla.blit(txt_dama,[30, Alto-70])
            pantalla.blit(txt_costo,[30, Alto-50])
            pantalla.blit(moneypng,[600, Alto-90])
            moneytxt = fuente.render(str(money), False, DORADO)
            pantalla.blit(textTime, textTimeRect)
            pantalla.blit(moneytxt,[665, Alto-50])

            for b in Selaliados:
                txt_vsalud = fuente2.render(str(stats[0][b.id-1]), False, ROJO)
                pantalla.blit(txt_vsalud,[b.rect.x+15, b.rect.y-34])
                txt_vdama = fuente2.render(str(stats[1][b.id-1]), False, VERDE)
                pantalla.blit(txt_vdama,[b.rect.x+15, b.rect.y-22])
                txt_vcosto = fuente2.render(str(stats[2][b.id-1]), False, DORADO)
                pantalla.blit(txt_vcosto,[b.rect.x+15, b.rect.y-10]) #mostrar atributos de los seleccionables
            todos.update()
            todos.draw(pantalla)
            enemigos.draw(pantalla)
            aliados.draw(pantalla)
            Selaliados.draw(pantalla)
            pygame.display.flip()
            reloj.tick(15)

        #DIBUJO FONDO DEL TUTORIAL
        elif pausa == True and entuto == True: 
            pantalla.fill(NEGRO) 
            pantalla.blit(fondotutorial,[0,0]) 
            punt1.rect.y = 170 
            pygame.display.flip() 
        #DIBUJO FONDO MENU PRINCIPAL
        elif pausa == True and findg == False:
            pantalla.fill(NEGRO)
            pantalla.blit(principal,[90,27])
            pantalla.blit(continuar,[30,90])
            pantalla.blit(reiniciar,[30,130])
            pantalla.blit(tutorial,[30,170])
            pantalla.blit(salir,[30,210])
            pantalla.blit(txt_record_actual,[30,300])
            pantalla.blit(record_actual_nivel_uno,[30,340])
            pantalla.blit(txt_record_actual_Nvl2,[30,380])
            pantalla.blit(record_actual_nivel_dos,[30,420])
            menu.update()
            menu.draw(pantalla)
            pygame.display.flip()
        #DIBUJO FONDO GAMEOVER
        elif pausa == True and findg == True:
            if findgd == True:
                secs = 0
                mins = 0 
                hours = 0
                pantalla.fill(NEGRO)
                ost.stop()
                pantalla.blit(gameover,[0,0])
                pygame.display.flip()
                if reprod == False:
                    ostgo.play()
                    reprod = True
            #DIBUJO FONDO VICTORIA
            elif findgv == True:
                current_timeV = 0
                current_timeV = pygame.time.get_ticks() 
                
                millisecsV = current_timeV // 1000
                secsV = millisecsV % 60
                print("segundos victoria:")
                print(secsV)
                
                secs = 0
                mins = 0 
                hours = 0
                pantalla.fill(NEGRO)
                ost.stop()
                
                ostvictoria=pygame.mixer.Sound(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Sonidos\Victoria.ogg")
                if nivel_dos == True:
                    ostmomias.stop()
                    victoriaimagen=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\fotovictoria.jpeg")
                    pantalla.blit(victoriaimagen,[0,0])
                    
                    # Cerrar la conexión a la base de datos
                    conn.close()
                else:
                    victoriaimagen=pygame.image.load(r"C:\Users\enzoe\Desktop\Jueguito\Pruebas-Jueguito\Interfaz\fotoPrimeraVictoria.png")
                    pantalla.blit(victoriaimagen,[0,Alto//4])
                
                pantalla.blit(tiempoMax,[Ancho//3,0])
                
                pygame.display.flip()
                if reprod == False:
                    ostvictoria.play()
                    reprod = True
                
                if 40 <= secsV <= 50 and not nivel_dos:
                        # Reinicia el juego eliminando a los aliados y enemigos,
                        # restablece la vida de los fuertes, reinicia variables y oleadas
                        ostmomias.play(-1)
                        nivel_dos = True
                        reprod = False
                        start_time = 0
                        start_time = pygame.time.get_ticks()
                        secs = 0
                        mins = 0 
                        hours = 0
                        for a in aliados:
                            aliados.remove(a)
                            todos.remove(a)
                        for e in enemigos:
                            enemigos.remove(e)
                            todos.remove(e)
                        fuerte1.vida = 500
                        fuerte2.vida = 200
                        entuto = False
                        oleadas = [7,1,5,4,2,3,1,0,5,2,3,4,3,2,1,3,2,1,1,0,0,6,1,5,4,2,3,1,0,5,2,3,4,3,2,1,3,2,1,1,0,0,]
                        #oleadas = [7,6,5,4,3,2,1,0]
                        #oleadas = [0,1,2,3,4,5,6,7]
                        spawn = 30
                        generation = 15
                        money = 0
                        findg = not findg
                        findgv = not findgv
                        pausa = not pausa
                    
