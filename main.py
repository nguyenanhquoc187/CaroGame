import pygame
from GameSettings.DefaultSettings import *
from Menu.MainMenu import Menu

pygame.init()
pygame.display.set_caption('Trò chơi cờ caro')

if __name__ == "__main__":
    menu = Menu(screen)
    menu.run()

