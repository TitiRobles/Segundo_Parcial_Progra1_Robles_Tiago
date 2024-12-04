import pygame
import sys
from auxiliares import cargar_ranking, achicar_imagen
from colores import *
pygame.init()


fuente_titulo = pygame.font.Font('C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/fonts/VarsityTeam-Bold.otf', 70)
fuente_sub_titulo = pygame.font.Font('C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/fonts/VarsityTeam-Bold.otf', 40)
fuente_boton = pygame.font.Font('C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/fonts/VarsityTeam-Bold.otf', 40)
fuente_ranking = pygame.font.Font('C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/fonts/VarsityTeam-Bold.otf', 30)

ANCHO_PANTALLA = 800
ALTURA_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTURA_PANTALLA))

class Menu:
    """Clase que maneja el menu del juego"""
    def __init__(self):
        self.boton_jugar = pygame.Rect((ANCHO_PANTALLA / 2 - 100), (ALTURA_PANTALLA / 2 - 50), 200, 50)
        self.boton_salir = pygame.Rect((ANCHO_PANTALLA / 2 - 100), (ALTURA_PANTALLA / 2 + 150), 200, 50)
        self.boton_ranking = pygame.Rect((ANCHO_PANTALLA / 2 - 100), (ALTURA_PANTALLA / 2 + 50), 200, 50)

        self.imagen_volver = achicar_imagen("C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/img/left-arrow-in-circular-button-black-symbol.png", 10)
        self.rect_volver = self.imagen_volver.get_rect() 
        self.rect_volver.topleft = (10, 10)
        self.imagen_sonido = achicar_imagen("C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/img/mute.png", 11)
        self.rect_sonido = self.imagen_sonido.get_rect()
        self.rect_sonido.topleft = (11, 10)

    def mostrar_menu(self):
        """Dibuja el menu"""
        pantalla.fill(COLOR_MARRON)
        jugar_texto = fuente_boton.render("JUGAR", True, COLOR_NEGRO)
        salir_texto = fuente_boton.render("SALIR", True, COLOR_NEGRO)
        ranking_texto = fuente_boton.render("RANKING", True, COLOR_NEGRO)
        titulo = fuente_titulo.render("This or That", True, COLOR_BLANCO)
        sub_titulo = fuente_sub_titulo.render("Version Futbolera", True, COLOR_BLANCO) #Hago todos los textos que preciso

        pygame.draw.rect(pantalla, COLOR_BLANCO, self.boton_jugar)
        pygame.draw.rect(pantalla, COLOR_BLANCO, self.boton_salir)
        pygame.draw.rect(pantalla, COLOR_BLANCO, self.boton_ranking) # Dibujo los botones

        pantalla.blit(jugar_texto, (self.boton_jugar.x + 34, self.boton_jugar.y + 5))
        pantalla.blit(salir_texto, (self.boton_salir.x + 34, self.boton_salir.y + 5))
        pantalla.blit(ranking_texto, (self.boton_ranking.x + 20, self.boton_ranking.y + 5))
        pantalla.blit(self.imagen_sonido, self.rect_sonido)
        pantalla.blit(titulo, (180, 80))
        pantalla.blit(sub_titulo, (210, 140)) # Dibujo los textos y la imagen de mutuar sonido

        pygame.display.update()

    def ejecutar_menu(self):
        """Se encarga de manejar el menu"""
        correr_menu = True
        musica_pausada = False
        while correr_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if self.boton_jugar.collidepoint(mouse_x, mouse_y):
                        return "JUGAR" #Si clickea jugar, se pasa al evento del juego
                    
                    if self.boton_ranking.collidepoint(mouse_x, mouse_y):
                        return "RANKING" # Si clickea RANKING, se pasa al evento de mostrar ranking
                    
                    if self.rect_volver.collidepoint(mouse_x, mouse_y):
                        self.mostrar_menu() # si clickea el boton volver dentro del ranking, se vuelve al menu

                    if self.rect_sonido.collidepoint(mouse_x, mouse_y):
                        if musica_pausada:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                            musica_pausada = True # Si clickea en el Sound off, se apaga el sonido, si vuelve a clickear, arranca nuevamente

                    if self.boton_salir.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        sys.exit() # Sale del juego

            self.mostrar_menu()

    def mostrar_ranking(self):
        """Muestra el ranking del archivo CSV """
        pantalla.fill(COLOR_MARRON)
        titulo = fuente_titulo.render("TOP 5 RANKING", True, COLOR_BLANCO)
        pantalla.blit(titulo, (ANCHO_PANTALLA / 2 - titulo.get_width() / 2, 50))

        y = 150

        ranking = cargar_ranking()

        for i, jugador in enumerate(ranking):
            texto = fuente_ranking.render(f"{i + 1}. {jugador[0]} - {jugador[1]}pts", True, COLOR_BLANCO)
            pantalla.blit(texto, (ANCHO_PANTALLA / 2 - texto.get_width() / 2, y))
            y += 50

        pantalla.blit(self.imagen_volver, self.rect_volver)


        pygame.display.update()