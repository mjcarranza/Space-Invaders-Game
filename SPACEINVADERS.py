import pygame, sys
from pygame.locals import *
from Main import *
import os
import threading
import random
import csv
pygame.init()

# clase principal del juego
class NuevoJuego(object):
    # parametros que recibe la clase NuevoJueo
    def __init__(self, rangoDisparo, velAlien, username, velocidadDisparo, rangoMeteoro, nivel):
        self.rangoDisparo = rangoDisparo
        self.rangoMeteoro = rangoMeteoro
        self.velocidadDisparo = velocidadDisparo
        self.velAlien = velAlien
        self.alto = 600
        self.ancho = 900
        self.puntos = 0
        self.puntuacionAlta = 0
        self.username = username
        self.nivel = nivel
    # funcion para guardar las puntuaciones de los jugadores
    def SaveScores(self, sc, hs, user):
        self.user = user
        self.sc = sc
        self.hs = hs
        self.lista = []
        with open("statsPlayer.csv", newline='') as File:  
            reader = csv.reader(File)
            self.lista.append([self.user, self.hs, self.sc])
            for row in reader:
                if len(row) > 0:
                    if self.user != row[0]:
                        self.lista.append(row)
        writer = csv.writer(open('statsPlayer.csv', 'w'), delimiter = ",")
        writer.writerows(self.lista)
    # funcion para cargar los puntajes más altos de los jugadores
    def LoadScores(self, user):
        self.user = user
        with open("statsPlayer.csv", newline='') as File:  
            reader = csv.reader(File)
            for row in reader:
                if len(row) > 0:
                    if self.user == row[0]:
                        self.puntuacionAlta = int(row[1])
                        self.puntos = int(row[2])
                        if self.nivel == 1:
                            self.puntos = 0
                        else:
                            self.puntos = int(row[2])    
    # clase para la nave defensora
    class naveEspacial(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            #dimensiones de la vetana donde se va a dibujar la nave
            self.alto2 = 600
            self.ancho2 = 900
            self.ventana = pygame.display.set_mode((self.ancho2, self.alto2))  
            # se carga la imagen de la nave
            self.imagenNave = pygame.image.load("Imagenes/shipPro.png")
            # se obtiene el rectanulo de la nave y su centro
            self.rectNave = self.imagenNave.get_rect()
            self.rectNave.centerx = self.ancho2/2-4
            self.rectNave.centery = self.alto2-100
            self.superficie = self.ventana
            # velocidad a la que se mueve la nave          
            self.velocidad = 5
            # lista para controlar los disparos de la nave
            self.listaDisparo = []
            # se valida la vida de la nave
            self.vida = True
            # se carga el sonido para cada disparo de la nave
            self.sonidoDisparo = pygame.mixer.Sound("sonidos/sonidoDisparo.wav")
            
        # función para dibujar la imagen de la nave en la pantalla
        def dibujarNave(self, superficie):
            self.superficie.blit(self.imagenNave, self.rectNave) 
    # función para los disparos de la nave y los aliens
    class proyectil(pygame.sprite.Sprite):
        def __init__(self, posx, posy, ruta, personaje, velocidadDisparo):
            pygame.sprite.Sprite.__init__(self)
            # dimensiones de la ventana donde se dibuja el proyectil dibujar el proyectil
            self.alto = 600
            self.ancho = 900 
            # se carga la imagen del proyectil
            self.imagenProyectil = pygame.image.load(ruta)
            self.ventana = pygame.display.set_mode((self.ancho, self.alto))
            # se obtiene el rectangulo de la imagen del proyectil
            self.rect = self.imagenProyectil.get_rect() 
            # definicion de variable para velocidad de disparo
            self.velocidadDisparo = velocidadDisparo
            # se obtienen las posiciones en (x,y) de la imagen del proyectil
            self.rect.top = posy
            self.rect.left = posx
            # superficie donde se dibuja la imagen del proyectil
            self.superficie = self.ventana
            self.disparoPersonaje = personaje

        # funcion define la trayectoria de los proyectiles de la nave y enemigos
        def trayectoria(self):
            # si es True, el disparo es de la nave espacial, de lo contrario es de un enemigo
            if self.disparoPersonaje == True:
                self.rect.top = self.rect.top - self.velocidadDisparo
            else:
                self.rect.top = self.rect.top + self.velocidadDisparo
        # funcion dibuja el disparo o proyectil en la ventana
        def dibujarDisparo(self, superficie):
            self.superficie.blit(self.imagenProyectil, self.rect) 
    # clase para los enemigos
    class enemigo(pygame.sprite.Sprite):
        def __init__(self, ventana, rangoDisparo, velAlien):
            pygame.sprite.Sprite.__init__(self)
            # cargar imagenes de los enemigos y sus explosiones
            self.ventana = ventana
            self.alienA = pygame.image.load("Imagenes/enemy2_1.png")
            self.explosionA = pygame.image.load("Imagenes/explosionblue.png")

            self.alienB = pygame.image.load("Imagenes/enemy1_2.png")
            self.explosionB = pygame.image.load("Imagenes/explosionpurple.png")

            self.alienC = pygame.image.load("Imagenes/enemy3_1.png")
            self.explosionC = pygame.image.load("Imagenes/explosiongreen.png")
            
            # variables para los enemigos
            self.posAlienx = 0
            self.listaDisparo = []
            self.listaAlien = []
            self.listaExplosion = []
            # estas variables ayudana a saber si se le ha disparado a un enemigo o no, y si es así, se elimina de la lista
            self.Visible = True
            self.Visible2 = True
            
        # funcion para controlar la lista de los enemigos.
        def listaDeEnemigo(self):
                self.posAlienx = 0
                contador = 0
                for numAlien in range(10):
                    self.rectA = self.alienA.get_rect()
                    self.posA = [self.alienA, self.rectA, self.posAlienx+contador, 185, self.Visible]
                    self.expA = [self.explosionA, self.Visible2]
                    self.listaAlien.append(self.posA)
                    self.listaExplosion.append(self.expA)
                    contador = contador + 70
                self.posAlienx = 0
                contador = 0
                for numAlien in range(10):
                    self.rectB = self.alienA.get_rect()
                    self.posB = [self.alienB, self.rectB, self.posAlienx+contador, 130, self.Visible]
                    self.listaAlien.append(self.posB)
                    self.expB = [self.explosionB, self.Visible2]
                    self.listaExplosion.append(self.expB)
                    contador = contador + 70
                self.posAlienx = 0
                contador = 0
                for numAlien in range(10):
                    self.rectC = self.alienA.get_rect()
                    self.posC = [self.alienC, self.rectC, self.posAlienx+contador, 85, self.Visible]
                    self.listaAlien.append(self.posC)
                    self.expC = [self.explosionC, self.Visible2]
                    self.listaExplosion.append(self.expC)
                    contador = contador + 70
        # funcion para dibujar enemigos en la ventana. controlado por matriz    
        def dibujar(self, superficie):
            for i in range (30):
                self.invasor = self.listaAlien[i][0]
                self.invasorRect = self.listaAlien[i][1]
                self.invasorX = self.listaAlien[i][2]
                self.invasorY = self.listaAlien[i][3]
                self.listaAlien[i][1].top = self.invasorY
                self.listaAlien[i][1].left = self.invasorX
                self.invasorbool = self.listaAlien[i][4]
                self.exp = self.listaExplosion[i][0]
                # condicion para controlar si se eliminan o no los enemigos
                if self.invasorbool:
                    superficie.blit(self.invasor, (self.invasorX, self.invasorY))
                elif self.listaExplosion[i][1]:
                    superficie.blit(self.exp, (self.invasorX, self.invasorY))
                    self.listaExplosion[i][1] = False
                    
    # funcion para el disparo de los enemigos  
    def disparoEnemy(self, Enemigo):
        for c in range(30):
            if Enemigo.listaAlien[c][4]: 
                # se usan numeros aleatorios para que los enemigos no disparen al mismo tiempo, sino tratar de que sea uno por uno
                if (random.randint(0, 100)<self.rangoDisparo):
                    h, k = Enemigo.listaAlien[c][1].center
                    # dibujar proyectil enemigo
                    proyectilEnemigo = self.proyectil(h, k, "Imagenes/proyectilEnemigo.png", False, self.velocidadDisparo)
                    Enemigo.listaDisparo.append(proyectilEnemigo)
    # funcion para el mensaje de felicitación al completar el juego
    def congrats(self):
        #se carga imagen del mensaje
        ventFel = pygame.display.set_mode((self.ancho, self.alto), pygame.NOFRAME)
        fondoFel = pygame.image.load("Imagenes/EndScreen.jpg")
        #se dibuja en ventana
        while True:
            ventFel.blit(fondoFel, (0, 0))

        
    #funcion principal de ejecucion del juego
    def CrearVentana(self):
        # se centra la ventana en el centro de la pantalla del computador
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # se inicializa pygame
        pygame.init()
        # se crea la ventana del juego (dimensiones)
        ventana = pygame.display.set_mode((self.ancho, self.alto), pygame.NOFRAME)
        pygame.display.set_caption("SPACE INVADERS")

        # cargar imagen para el fondo de panatalla del juego
        fondo = pygame.image.load("Imagenes/space2.png")
        
        # cargar musica de fondo y efectos de sonido
        pygame.mixer.music.load("sonidos/GameMusic.mid")
        pygame.mixer.music.play(1000)
        sonidoGameOver = pygame.mixer.Sound("sonidos/SonidoGameOver.wav")
        sonidoExplosion = pygame.mixer.Sound("sonidos/explosion.wav")
        sonidoWinner = pygame.mixer.Sound("sonidos/winner.wav")
        
        # tipo de fuente para el juego y mensajes a imprimir
        font = pygame.font.match_font("OCR A Extended")
        score = pygame.font.Font.render((pygame.font.Font(font, 20)), "SCORE:", 0, (255, 255, 255))
        hscore = pygame.font.Font.render((pygame.font.Font(font, 20)), "HI-SCORE:", 0, (255, 255, 255))
        nivel = pygame.font.Font.render((pygame.font.Font(font, 20)), "NIVEL:", 0, (255, 255, 255))
        numeroNivel = pygame.font.Font.render((pygame.font.Font(font, 20)), str(self.nivel), 0, (255, 255, 255))
        # llamada a la funcion LoadScores para cargar puntajes de jugadores
        self.LoadScores(self.username)

        # variables para la ejecuciuon del juego
        jugador = self.naveEspacial()
        Enemigo = self.enemigo(ventana, self.rangoDisparo, self.velAlien)
        detener = True
        enJuego = True
        fin = True
        movimientoEnemigo = True
        nextLevel = False
        meteorito = []
        # ciclo de ejecución
        while True:
            # se dibuja la imagen de fondo en la ventana
            ventana.blit(fondo, (0, 0))
            # se imprime el texto en la ventana
            ventana.blit(score,(20,0))
            ventana.blit(hscore,(650,0))
            ventana.blit(nivel, (320,0))
            ventana.blit(numeroNivel, (420,0))
            # se imprime en pantalla los puntajes 
            scor = pygame.font.Font.render((pygame.font.Font(font, 20)), str(self.puntos), 0, (255, 255, 255))
            ventana.blit(scor,(110,0))
            if self.puntos >= self.puntuacionAlta:
                hscor = pygame.font.Font.render((pygame.font.Font(font, 20)), str(self.puntos), 0, (255, 255, 255))
                self.SaveScores(self.puntos, self.puntos, self.username)
            else:
                hscor = pygame.font.Font.render((pygame.font.Font(font, 20)), str(self.puntuacionAlta), 0, (255, 255, 255))
                self.SaveScores(self.puntos, self.puntuacionAlta, self.username)
            # imprimir puntaje mas alto
            ventana.blit(hscor,(790,0))
            # llamada a clase enemigo para dibujarlos en ventana
            Enemigo.listaDeEnemigo()
            Enemigo.dibujar(ventana)
            # ciclo para cerrar los modulos de pygame al salir del juego
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # definicion del movimiento de la nave
            if enJuego == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        if jugador.rectNave.left > 10:
                            jugador.rectNave.left -= jugador.velocidad
                    elif event.key == K_RIGHT:
                        if jugador.rectNave.left < 850:
                            jugador.rectNave.right += jugador.velocidad
                    elif event.key == K_UP:
                        if jugador.rectNave.top > 30:
                            jugador.rectNave.top -= jugador.velocidad
                    elif event.key == K_DOWN:
                        if jugador.rectNave.top < 550:
                            jugador.rectNave.top += jugador.velocidad
                    # definicion de tecla para disparos de la nave
                    elif event.key == K_SPACE:            
                        x = jugador.rectNave.centerx - 10
                        y = jugador.rectNave.centery - 40
                        self.miProyectil = self.proyectil(x, y, "Imagenes/proyectil.png", True, self.velocidadDisparo)
                        jugador.listaDisparo.append(self.miProyectil)
                        # reproducir efecto de sonido para el disparo de la nave
                        jugador.sonidoDisparo.play()
                        
                # definicion del movimiento de los enemigos
                if movimientoEnemigo == True:
                    for i in range (30):
                        if Enemigo.listaAlien[i][2] < 850:
                            Enemigo.listaAlien[i][2] += self.velAlien
                        else:
                            movimientoEnemigo = False
                else:
                    for j in range (30):
                        if Enemigo.listaAlien[j][2] > 5:
                            Enemigo.listaAlien[j][2] -= self.velAlien
                        else:
                            movimientoEnemigo = True
            # condicion para el comportamiento de los meteoritos
            if detener:               
                if random.randint(0, 100) < self.rangoMeteoro:
                    metX = random.randint(30, 850)
                    metY = -30
                    self.meteoro = self.proyectil(metX, metY, "Imagenes/roca.png", False, self.velocidadDisparo)
                    meteorito.append(self.meteoro)
            # se dibuja la nave espacial en ventana
            jugador.dibujarNave(ventana)
            # condicion para el disparo aleatorio de los enemigos
            if (random.randint(0, 100)<self.rangoDisparo):
                if detener:
                    self.disparoEnemy(Enemigo)

            # condición para dibujar los disparos de la nave
            if len(jugador.listaDisparo) > 0:
                eliminado = False
                for disparoNave in jugador.listaDisparo:
                    disparoNave.dibujarDisparo(ventana)
                    disparoNave.trayectoria()
                    # condicion para validar si un enemigo es eliminado por el disparo de la nave
                    if len(Enemigo.listaAlien) > 0:
                        for s in range(30):
                            if disparoNave.rect.colliderect(Enemigo.listaAlien[s][1]):
                                if Enemigo.listaAlien[s][4]:
                                    self.puntos = self.puntos + 1
                                    sonidoExplosion.play()
                                    Enemigo.listaAlien[s][4] = False
                                    eliminado = True
                        # condición para eliminar disparo de la nave si el jugador pierde
                        if eliminado:
                            jugador.listaDisparo.remove(disparoNave)
            # condicion valida si el disparo de la nave destruye un meteorito al colicionar
            if len(jugador.listaDisparo) > 0:
                for disparoNave in jugador.listaDisparo:
                    if len(meteorito) > 0:
                        for mete in meteorito:
                            if disparoNave.rect.colliderect(mete.rect):
                                jugador.listaDisparo.remove(disparoNave)
                                meteorito.remove(mete)
                                self.puntos = self.puntos + 1
                            if mete.rect.top > 750:
                                meteorito.remove(mete)
            # valida si el disparo ha sobrepasado las dimensiones de la ventana, si es así, se elimina de la lista de disparo
            if len(jugador.listaDisparo) > 0:
                for disparoNave in jugador.listaDisparo:
                    if disparoNave.rect.top < 50:
                        jugador.listaDisparo.remove(disparoNave)
            # valida si la nave colisiona con un enemigo, si es así, vuelve a empezar
            if len(Enemigo.listaAlien) > 0:
                for s in range(30):
                    if Enemigo.listaAlien[s][4]:
                        if jugador.rectNave.colliderect(Enemigo.listaAlien[s][1]):
                            self.gameOver()
            # se dibujan los meteoritos que estan dentro de la lista de meteoritos
            if len(meteorito) > 0:
                for met in meteorito:
                    met.dibujarDisparo(ventana)
                    met.trayectoria()
                    # el meteorito se elimina de la lista una vez que sobrerpasa las dimensiones de la ventana
                    if met.rect.top > 600:
                        meteorito.remove(met)
                    # valida si un meteorito colisiona con la nave, si es así, vuelve a empezar
                    if met.rect.colliderect(jugador.rectNave):
                        jugador.velocidad = 0
                        Enemigo.velAlien = 0
                        meteorito = []
                        detener = False
                        Enemigo.listaDisparo = []
                        jugador.listaDisparo = []
                        enJuego = False
                        pygame.mixer.music.stop()
                        sonidoGameOver.play()
                        self.gameOver()

            # condicion para el disparo de los enemigos
            if len(Enemigo.listaDisparo) > 0:
                for disparoAlien in Enemigo.listaDisparo:
                    disparoAlien.dibujarDisparo(ventana)
                    disparoAlien.trayectoria()
                    # valida si el disparo sobrepasa las dimensiones de la ventana
                    if disparoAlien.rect.top > 600:
                        Enemigo.listaDisparo.remove(disparoAlien)
                    # valida si el enemigo colisiona con la nave, si es así, vuelve a empezar de nuevo
                    if disparoAlien.rect.colliderect(jugador.rectNave):
                        jugador.velocidad = 0
                        Enemigo.velAlien = 0
                        meteorito = []
                        detener = False
                        jugador.listaDisparo = []
                        Enemigo.listaDisparo = []
                        enJuego = False
                        pygame.mixer.music.stop()
                        sonidoGameOver.play()
                        self.gameOver()
                    # valida si el disparo de la nave colisiona con el de un enemigo, entonces que se eliminen ambos
                    for disparoNave in jugador.listaDisparo:
                        if disparoNave.rect.colliderect(disparoAlien.rect):
                            Enemigo.listaDisparo.remove(disparoAlien)
                            jugador.listaDisparo.remove(disparoNave)
            # validacion para pasar al siguente nivel
            for Total in range(30):
                if Enemigo.listaAlien[Total][4]:
                    nextLevel = False
                    break
                else:
                    nextLevel = True
            if nextLevel:
                CrearNuevoNivel(fin)

            
                            
            # funcion para crear nuevos niveles de dificultad
            def CrearNuevoNivel(fin):
                self.fin = fin
                fondoFel = pygame.image.load("Imagenes/EndScreen.jpg") 
                self.nivel = self.nivel + 1
                # niveles de dificultad
                if self.nivel == 1:
                    self.sigNivel = NuevoJuego(1, 1.5, self.user, 5, 0.5, self.nivel)
                    self.sigNivel.CrearVentana()
                elif self.nivel == 2: 
                    self.sigNivel = NuevoJuego(3, 2.5, self.user, 8, 1, self.nivel)
                    self.sigNivel.CrearVentana()
                elif self.nivel == 3:
                    self.sigNivel = NuevoJuego(5, 3.5, self.user, 11, 2, self.nivel)
                    self.sigNivel.CrearVentana()
                # valida si el jugador a completado el juego con exito, si es así se imprime ´pantalla de felicitación
                else:
                    ventana.blit(fondoFel, (0,0))
                    jugador.velocidad = 0
                    Enemigo.velAlien = 0
                    meteorito = []
                    detener = False
                    Enemigo.listaDisparo = []
                    jugador.listaDisparo = []
                    enJuego = False
                    pygame.mixer.music.stop()
                    if self.fin:
                        sonidoWinner.play()
                        self.fin = False
            # se actualiza la pantalla
            pygame.display.update()
    # si el jugador pierde entonces vuelve al nivel 1
    def gameOver(self):
        self.nivel = 1
        self.sigNivel = NuevoJuego(1, 1.5, self.user, 5, 0.5, self.nivel)
        self.sigNivel.CrearVentana()