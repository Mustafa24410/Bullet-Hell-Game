import pygame

screen = None
def init(scrn):
    global screen
    screen = scrn

class Player():
    def __init__(self, startx, starty):
        self.rect = pygame.FRect(startx, starty, 20, 20)
        self.rect.center = (startx, starty)
        self.move_vect = pygame.Vector2(0, 0)
        self.speed = 4
    
    def draw(self, color):
        pygame.draw.rect(screen, color, self.rect)