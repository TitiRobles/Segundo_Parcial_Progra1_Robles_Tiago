from models.juego import Juego
from models.menu import Menu
import pygame
import sys

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("C:/Users/julia/OneDrive/Escritorio/this_or_that/assets/snd/DUKI - Goteo (Instrumental).mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.5)

def correr_juego():
    menu = Menu()
    while True:
        accion = menu.ejecutar_menu()

        if accion == "JUGAR":
            juego = Juego()
            juego.ejecutar_juego()
        elif accion == "RANKING":
            menu.mostrar_ranking()
            volver = False
            while not volver:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        if menu.rect_volver.collidepoint(mouse_x, mouse_y):
                            volver = True
                            menu.mostrar_menu()
                            break
                pygame.display.update()

if __name__ == '__main__':
    correr_juego()

