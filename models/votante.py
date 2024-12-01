import random
import pygame

from .juego import pantalla
from colores import (COLOR_AZUL, COLOR_GRIS, COLOR_ROJO)

class Votante:
    """Esta clase representa a un votante
    que elige aleatoriamente entre el color rojo y azul
    """
    def __init__(self, id_votante):
        self.id_votante = id_votante
        self.voto = "Gris"

    def elegir_voto(self):
        """Elige los votos de los votantes de forma random y
        se reinicia con cada pregunta
        """
        self.voto = random.choice(["Rojo", "Azul"])

    def dibujo_voto(self, x, y):
        """Dibuja un cuadrado con el color que corresponde al 
        voto de cada uno de los votantes

        Args:
            x (_type_): Coordenada X del cuadrado
            y (_type_): Coordenada Y del cuadrado
        """
        if self.voto == "Rojo":
            color = COLOR_ROJO
        elif self.voto == "Azul":
            color = COLOR_AZUL
        else:
            color = COLOR_GRIS

        pygame.draw.rect(pantalla, color, (x, y, 40, 40))
