import pygame
import random
from os import walk

class Car(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.name = "car"

        # animations
        self.animations = [] # list of surfaces
        self.import_assets()

        # const and rect
        self.image = random.choice(self.animations)
        self.rect = self.image.get_rect(center = pos)

        # reducing the rect size for better looking collisions
        self.hitbox = self.rect.inflate(0,-self.rect.height / 2)

        # float based movement
        self.pos = pygame.math.Vector2(pos)

        if pos[0] < 200: # if x < 200
            self.direction = pygame.math.Vector2((1, 0))
        else:
            self.direction = pygame.math.Vector2((-1,0)) # set dir to left and flip the car
            self.image = pygame.transform.flip(self.image,True,False) # True,False -> flip x and don't flip y

        self.speed = 300

    def import_assets(self):
        path = r"C:\Users\mendy\OneDrive\שולחן העבודה\משחק 2\progress\project_1 - setup\graphics\cars"
        colors = [frame[2][i] for frame in walk(path) for i in range(len(frame[2]))]
        for color in colors:
            surf = pygame.image.load(path + "/" + color).convert_alpha()
            self.animations.append(surf)

    def update(self,dt):
        self.pos += self.direction * self.speed * dt
        self.hitbox.center = (round(self.pos.x),round(self.pos.y))
        self.rect.center = self.hitbox.center
        if not -200 < self.pos.x < 3400:
            self.kill()

