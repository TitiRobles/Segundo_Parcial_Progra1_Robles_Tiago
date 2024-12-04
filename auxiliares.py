import csv
import pygame

def ordenar_descendente(matriz: list[list]):
    
    for i in range(len(matriz) - 1):
        for j in range(i+1, len(matriz)):
            if int(matriz[i][1]) < int(matriz[j][1]):
                matriz[i], matriz[j] = matriz[j], matriz[i]

def cargar_ranking():
    ranking = []
    with open("C:/Users/julia/OneDrive/Escritorio/this_or_that/ranking.csv", 'r') as rkng:
        lineas = rkng.readlines()
        for linea in lineas:
            linea = linea.strip()
            if linea:
                datos = linea.split(",")
                if len(datos) == 2:
                    nombre = datos[0].strip()
                    puntaje = int(datos[1].strip())
                    ranking.append([nombre, puntaje])

    ordenar_descendente(ranking)
    
    return ranking[:5]

def achicar_imagen(ruta_imagen: str, cantidad: int) -> pygame.Surface:
    imagen_raw = pygame.image.load(ruta_imagen)
    alto = imagen_raw.get_height() // cantidad
    ancho = imagen_raw.get_width() // cantidad
    imagen_final = pygame.transform.scale(imagen_raw, (ancho, alto))
    return imagen_final

sonido_click = pygame.mixer.Sound("C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/snd/select.mp3")

if __name__ == '__main__':
    ranking = cargar_ranking()
    print(ranking)

