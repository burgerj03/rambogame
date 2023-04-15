import pygame


class Bullet():
    def __init__(self, travel_right, x, y):

        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x, self.y, 4, 4)
        self.speed = 30
        self.travel_right = travel_right

        self.bullet_radius_size = 2
        self.bullet_colour = (0, 0, 0)

    def draw(self, win):
        if self.travel_right:
            self.x += self.speed
        else:
            self.x -= self.speed
        self.hitbox = pygame.Rect(self.x, self.y, self.bullet_radius_size * 2, self.bullet_radius_size * 2)
        pygame.draw.circle(win, self.bullet_colour, (self.x, self.y), self.bullet_radius_size)
