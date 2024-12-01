import pygame
import random
import time

from .preguntas import *
from .votante import Votante
from colores import *

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
        pantalla.fill(COLOR_BLANCO)

        pregunta_texto = fuente.render(pregunta.pregunta, True, COLOR_NEGRO)
        pantalla.blit(pregunta_texto, (35, 35))

        opcion_rojo_texto = fuente.render(pregunta.opciones[0], True, COLOR_ROJO)
        pantalla.blit(opcion_rojo_texto, (65, 115))

        opcion_azul_texto = fuente.render(pregunta.opciones[1], True, COLOR_AZUL)
        pantalla.blit(opcion_azul_texto, (65, 175))

        texto_votacion, texto_porcentaje = self.mostrar_votacion(votos_rojo, votos_azul, porcentaje_rojo, porcentaje_azul)
        
        votacion_texto = fuente.render(texto_votacion, True, COLOR_NEGRO)
        pantalla.blit(votacion_texto, (65, 235))

        porcentaje_texto = fuente.render(texto_porcentaje, True, COLOR_NEGRO)
        pantalla.blit(porcentaje_texto, (65, 265))

        for i, votante in enumerate(self.votantes):
            votante.dibujo_voto(60+ (i * 42), 315)

        tiempo_texto = fuente.render(f"Tiempo: {tiempo_restante}s", True, COLOR_NEGRO)
        pantalla.blit(tiempo_texto, (ANCHO_PANTALLA - 450, 20))

        pygame.display.update()

    def ejecutar_juego():
        juego = Juego()
        run = True
        while run:
            tiempo_arranque = time.time()

            pregunta = juego.elegir_pregunta_random()
            
            while True:
                tiempo_restante = max(0, juego.tiempo_limite - (time.time() - tiempo_arranque ))
                if tiempo_restante == 0:
                    print("Tiempo agotado! Fin del juego")
                    run = False
                    break

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break

                votos_rojo, votos_azul, porcentaje_rojo, porcentaje_azul = juego.calcular_votos

                juego.dibujar_pantalla(pregunta, votos_rojo, votos_azul, porcentaje_rojo, porcentaje_azul)

                if not run:
                    break


