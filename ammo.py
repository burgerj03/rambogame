import pygame


class Ammo():
    def __init__(self, x, y, capacity):
        self.ammo_sprite = pygame.transform.scale(pygame.image.load('assets/sprites/misc/ammo_box.png'), (50, 50))

        self.capacity = capacity
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x, self.y, 50, 50)

    def draw(self, win):
        # debug
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        win.blit(self.ammo_sprite, (self.x, self.y))

