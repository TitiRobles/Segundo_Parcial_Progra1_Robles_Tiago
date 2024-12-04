import pygame
import random
import time

from models.preguntas import *
from models.votante import Votante
from models.gameover import GameOver
from models.menu import Menu
from colores import *
from auxiliares import achicar_imagen, sonido_click

menu = Menu()

pygame.init()

ANCHO_PANTALLA, ALTO_PANTALLA = 800, 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("This or That")

fuente = pygame.font.SysFont("Arial", 30)

class Juego:
    """Clase principal que maneja el juego
    """
    def __init__(self):
        self.preguntas = Pregunta.cargar_las_preguntas()
        self.votantes = [Votante(id_votante) for id_votante in range(5)]
        self.pregunta_actual = None
        self.puntaje = 0
        self.valor_puntos_pregunta = 50
        self.tiempo_limite = 15
        self.imagen_next = achicar_imagen("C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/img/next.png", 11)
        self.rect_next = self.imagen_next.get_rect()
        self.rect_next.topleft = (30, 200)
        self.imagen_refresh = achicar_imagen("C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/img/refresh.png", 11)
        self.rect_refresh = self.imagen_refresh.get_rect()
        self.rect_refresh.topleft = (30, 250)

    def elegir_pregunta_random(self):
        """Selecciona de la lista una pregunta random y la elimina para
        que no se vuelva a repetir en el juego
        """
        if not self.preguntas:
            return None
        pregunta = random.choice(self.preguntas)
        self.preguntas.remove(pregunta)
        return pregunta
    
    def calcular_votos(self):
        """Calcula los votos y porcentajes para las dos opciones"""
        votos_rojo = 0
        votos_azul = 0
        
        for votante in self.votantes:
            if votante.voto == "Rojo":
                votos_rojo += 1
            elif votante.voto == "Azul":
                votos_azul += 1

        porcentaje_rojo = (votos_rojo / 5) * 100
        porcentaje_azul = (votos_azul / 5) * 100
        return votos_rojo, votos_azul, porcentaje_rojo, porcentaje_azul
    
    def mostrar_votacion(self, votos_rojo, votos_azul,porcentaje_rojo, porcentaje_azul):
        """Devuelve el texto con el porcentaje de los votos"""
        texto_votos = f"Votacion: Rojo: {votos_rojo} votos, Azul: {votos_azul} votos"
        texto_porcentaje = f"Rojo: {porcentaje_rojo:.1f}%, Azul: {porcentaje_azul:.1f}%"
        return texto_votos, texto_porcentaje
    
    def dibujar_pantalla(self, pregunta, votos_rojo, votos_azul, porcentaje_rojo, porcentaje_azul, tiempo_restante):
        """Dibuja todo lo que necesita el juego en pantalla"""
        pantalla.fill(COLOR_BLANCO) #Relleno pantalla de blanco

        pregunta_texto = fuente.render(pregunta.pregunta, True, COLOR_NEGRO)
        ancho_pregunta = pregunta_texto.get_width()
        alto_pregunta = pregunta_texto.get_height()
        x = (ANCHO_PANTALLA - ancho_pregunta) // 2
        y = (ALTO_PANTALLA - alto_pregunta) // 2 
        pantalla.blit(pregunta_texto, (x, y - 140)) # Muestro la pregunta en pantalla

        opcion_rojo_texto = fuente.render(pregunta.opciones[0], True, COLOR_ROJO)
        opcion_rojo_rect = opcion_rojo_texto.get_rect(topleft=(220, 260))
        pygame.draw.rect(pantalla, COLOR_ROJO, opcion_rojo_rect.inflate(20, 20), 5)
        pantalla.blit(opcion_rojo_texto, opcion_rojo_rect) # Muestro opcion roja en pantalla

        opcion_azul_texto = fuente.render(pregunta.opciones[1], True, COLOR_AZUL)
        opcion_azul_rect = opcion_azul_texto.get_rect(topleft=(460, 260))
        pygame.draw.rect(pantalla, COLOR_AZUL, opcion_azul_rect.inflate(20,20), 5)
        pantalla.blit(opcion_azul_texto, opcion_azul_rect) # Muestro opcion azul en pantalla

        texto_votacion, texto_porcentaje = self.mostrar_votacion(votos_rojo, votos_azul, porcentaje_rojo, porcentaje_azul)
        
        votacion_texto = fuente.render(texto_votacion, True, COLOR_NEGRO)
        pantalla.blit(votacion_texto, (65, 400))

        porcentaje_texto = fuente.render(texto_porcentaje, True, COLOR_NEGRO)
        pantalla.blit(porcentaje_texto, (65, 450)) # Muestro votacion y porcentajes

        for i, votante in enumerate(self.votantes):
            votante.dibujo_voto(60 + (i * 100), 500) # Dibujo votantes con sus respectivos votos

        tiempo_texto = fuente.render(f"TIEMPO: {int(tiempo_restante)}s", True, COLOR_NEGRO)
        pantalla.blit(tiempo_texto, (ANCHO_PANTALLA - 150, 20)) # Muestro el tiempo restante en pantalla

        puntaje_texto = fuente.render(f"PUNTOS: {self.puntaje}", True, COLOR_NEGRO)
        pantalla.blit(puntaje_texto, (20, 20)) # Muestro el puntaje en pantalla

        pantalla.blit(self.imagen_next, self.rect_next)
        pantalla.blit(self.imagen_refresh, self.rect_refresh) # Muestro los comodines

        pygame.display.update()

    def ejecutar_juego(self):
        juego = Juego()
        run = True

        
        while run:
            tiempo_arranque = time.time()
            votos_rojo = 0
            votos_azul = 0
            porcentaje_rojo = 0.0
            porcentaje_azul = 0.0 # Reinicio los votos a 0 cada vez que arranca una pregunta
            
            pregunta = juego.elegir_pregunta_random() # Selecciono una pregunta random

            if pregunta is None:
                print("No hay más preguntas. Fin del juego.")
                run = False
                break

            if pregunta is not None:
                opcion_rojo_texto = fuente.render(pregunta.opciones[0], True, COLOR_ROJO)
                opcion_rojo_rect = opcion_rojo_texto.get_rect(topleft=(220, 260))
                opcion_azul_texto = fuente.render(pregunta.opciones[1], True, COLOR_AZUL)
                opcion_azul_rect = opcion_azul_texto.get_rect(topleft=(460, 260)) # Actualizo las opciones de la pregunta actual

            for votante in self.votantes:
                votante.voto = "Gris" # Reinicio los votantes a gris antes de que el jugador conteste

            while pregunta:
                tiempo_restante = max(0, juego.tiempo_limite - (time.time() - tiempo_arranque )) # Inicio el tiempo 
                if tiempo_restante == 0:
                    print("Tiempo agotado! Fin del juego")
                    run = False
                    break
                
                eventos = pygame.event.get()
                for event in eventos:
                    if event.type == pygame.QUIT:
                        run = False
                        break
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if self.rect_next.collidepoint(mouse_x, mouse_y):
                            self.puntaje += self.valor_puntos_pregunta
                            self.valor_puntos_pregunta += self.valor_puntos_pregunta
                            pygame.time.wait(1000)
                            self.rect_next.topleft = (1000, 1000)
                            pregunta = None
                            break # Si da click en el next, pasa a la siguiente pregunta como la hubiese respondido bien

                        if self.rect_refresh.collidepoint(mouse_x, mouse_y):
                            pygame.time.wait(1000)
                            self.rect_refresh.topleft = (1000, 1000)
                            pregunta = None
                            break # Si da click en refresh, pasa de pregunta, sin sumar puntos

                        if opcion_rojo_rect.collidepoint(mouse_x, mouse_y) or opcion_azul_rect.collidepoint(mouse_x, mouse_y):
                            sonido_click.play()
                            for votante in self.votantes:
                                votante.elegir_voto() # Si se da click en alguna opcion, los votantes elijen su voto de forma random
                            

                            votos_rojo, votos_azul, porcentaje_rojo, porcentaje_azul = self.calcular_votos() # Calculo votos
                            if votos_rojo > votos_azul and opcion_rojo_rect.collidepoint(mouse_x, mouse_y):
                                self.dibujar_pantalla(pregunta, votos_rojo, votos_azul, porcentaje_rojo, porcentaje_azul, tiempo_restante)
                                self.puntaje += self.valor_puntos_pregunta
                                self.valor_puntos_pregunta += self.valor_puntos_pregunta
                                pygame.time.wait(2000)
                                pregunta = None
                                break
                            elif votos_azul > votos_rojo and opcion_azul_rect.collidepoint(mouse_x, mouse_y):
                                self.dibujar_pantalla(pregunta, votos_rojo, votos_azul, porcentaje_rojo, porcentaje_azul, tiempo_restante)
                                self.puntaje += self.valor_puntos_pregunta
                                self.valor_puntos_pregunta += self.valor_puntos_pregunta
                                pygame.time.wait(2000)
                                pregunta = None
                                break # Si es correcta, sumo puntos, duplico el valor de la pregunta, y paso a la siguiente
                            else:
                                self.dibujar_pantalla(pregunta, votos_rojo, votos_azul, porcentaje_rojo, porcentaje_azul, tiempo_restante)
                                pygame.time.wait(2000)
                                run = False
                                break # Si perdio, el run pasa a falso

                if pregunta is not None:
                    self.dibujar_pantalla(pregunta, votos_rojo, votos_azul, porcentaje_rojo, porcentaje_azul, tiempo_restante)
                
                
                if not run:
                    game_over = GameOver(self.puntaje)
                    game_over.mostrar_game_over()
                    break # Si perdio se muestra el game over
                    
            
