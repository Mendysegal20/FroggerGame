import pygame
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)

        # animations variables
        self.animations = {}
        self.frame_index = 0
        self.status = "up"

        # const and rect
        self.import_assets()
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2((0,0)) # direction = 0
        self.speed = 250

        # collisions
        self.collision_sprites = collision_sprites

        # reducing the rect size for better looking collisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)

    def collision(self,direction):
        if direction == "horizontal":
            # horizontal collisions
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite,"name") and sprite.name == "car": # if we collide with a car, we end the game
                        pygame.quit()
                        exit()

                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
        else:
            # vertical collisions
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite,"name") and sprite.name == "car": # if we collide with a car, we end the game
                        pygame.quit()
                        exit()

                    if self.direction.y > 0:  # moving right
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    if self.direction.y < 0:  # moving left
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    # changing the position accordingly
    def move(self,dt):
        # normalize the direction in case of diagonal movement
        if self.direction.length() != 0:
            self.direction = self.direction.normalize()

        # horizontal movement + collision
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # vertical movement + collision
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    # import the paths for animations
    def import_assets(self):
        path_player = r"C:\Users\mendy\OneDrive\שולחן העבודה\משחק 2\progress\project_1 - setup\graphics\player"

        for index,folder in enumerate(walk(path_player)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in folder[2]:
                    path = folder[0].replace("\\","/") + "/" + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split("\\")[-1]
                    self.animations[key].append(surf)

    # input from the keyboard
    def input(self):
        keys = pygame.key.get_pressed()

        # horizontal input
        # x movement
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0

        # y movement
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else: self.direction.y = 0

    # animate the scene by moving the character(player) with 16 frames
    def animate(self,dt):
        current_status_list = self.animations[self.status]  # the list of the current status from dict

        if self.direction.magnitude() != 0: # if there is any movement
            self.frame_index += 8 * dt
            if self.frame_index >= len(current_status_list):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_status_list[int(self.frame_index)]

    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640

        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560

        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery

    # the update method
    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.restrict()
