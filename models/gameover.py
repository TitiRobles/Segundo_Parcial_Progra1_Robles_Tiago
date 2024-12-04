import pygame
from colores import *
from auxiliares import achicar_imagen
import csv
import time

ANCHO_PANTALLA = 800
ALTURA_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTURA_PANTALLA))

class GameOver:
    def __init__(self, puntaje):
        self.puntaje = puntaje
        self.imagen = achicar_imagen('C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/img/descarga.jpg', 3)
        self.rect_imagen = self.imagen.get_rect()
        self.rect_imagen.topleft = (270, 350)
        self.fuente = pygame.font.SysFont("Arial", 30)
        self.fuente_titulo = pygame.font.Font('C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/fonts/VarsityTeam-Bold.otf', 60)

    def mostrar_input(self):
        """Genera el input para que el jugador puede ingresar su
        nombre cuando pierda"""
        texto_ingreso = self.fuente.render("INGRESA TU NOMBRE: ", True, COLOR_NEGRO)
        pantalla.fill(COLOR_MARRON)
        pantalla.blit(texto_ingreso, (ANCHO_PANTALLA // 3, ALTURA_PANTALLA // 3 - 50))

        input_box = pygame.Rect(ANCHO_PANTALLA // 3, ALTURA_PANTALLA // 3, 200, 50)
        pygame.draw.rect(pantalla, COLOR_NEGRO, input_box, 2) # Creo la caja para el input

        nombre = ""
        texto_nombre = self.fuente.render(nombre, True, COLOR_NEGRO)
        pantalla.blit(texto_nombre, (input_box.x + 5, input_box.y + 10)) # Inicio el nombre dentro del input box

        pygame.display.update()

        return self.obtener_nombre(input_box, nombre)
    
    def obtener_nombre(self, input_box, nombre):
        """Obtiene el nombre escrito por el jugador"""
        activo = True
        while activo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Cuando presiona enter confirma el nombre
                        activo = False
                        break
                    elif event.key == pygame.K_BACKSPACE:  # Eliminar un caracter
                        nombre = nombre[:-1]
                    else:  #Añade caracteres
                        nombre += event.unicode

            # Actualizar el nombre en pantalla
            pantalla.fill(COLOR_MARRON)
            texto_game_over = self.fuente_titulo.render("GAME OVER", True, COLOR_BLANCO)
            texto_puntos = self.fuente.render(f"Tu puntaje es: {self.puntaje}", True, COLOR_BLANCO)
            pantalla.blit(texto_game_over, (ANCHO_PANTALLA // 3, 10))
            pantalla.blit(texto_puntos, (ANCHO_PANTALLA // 3, 100))
            texto_ingreso = self.fuente.render("Ingresa tu nombre:", True, COLOR_BLANCO)
            pantalla.blit(texto_ingreso, (ANCHO_PANTALLA // 3, ALTURA_PANTALLA // 3 - 50))
            pygame.draw.rect(pantalla, COLOR_BLANCO, input_box, 3)
            texto_nombre = self.fuente.render(nombre, True, COLOR_BLANCO)
            pantalla.blit(texto_nombre, (input_box.x + 5, input_box.y + 10))
            pantalla.blit(self.imagen, self.rect_imagen)
            pygame.display.update()

        return nombre
    
    def guardar_nombre(self, nombre):
        """Guarda el nombre y su puntaje en archivo CSV"""
        with open("C:/Users/julia/OneDrive/Escritorio/this_or_that/ranking.csv", "a", newline="") as archivo:
            añadir_nombre = csv.writer(archivo)
            añadir_nombre.writerow([nombre, self.puntaje])

    def mostrar_game_over(self):
        """Muestra el game over con los puntos y la opcion de que
        el jugador ingrese su nombre"""
        nombre = self.mostrar_input()
        if nombre:
            self.guardar_nombre(nombre)

        pygame.time.wait(1000)




