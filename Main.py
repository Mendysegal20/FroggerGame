import pygame
from car import Car
from paths import *
from settings import *
from random import choice
from player import Player
from random import randint
from sprite import SimpleSprite, LongSprite


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2((0,0)) # default is 0 vector
        self.background = pygame.image.load(bg_path).convert()
        self.forground = pygame.image.load(fg_path).convert_alpha()

    def customize_draw(self):

        # create the camera. change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # blit the bg
        display_surface.blit(self.background,-self.offset)

        # sort the y values of the sprites, so is sprite1.y > sprite2.y, sp2 will be blited on top of sp1 (after him)
        for sprite in sorted(self.sprites(),key = lambda sprite:sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image,offset_pos)

        display_surface.blit(self.forground,-self.offset)


pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()

# sprites
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

# player
player = Player((2062,3274),all_sprites,obstacle_sprites)


# timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer,50)
pos_list = []

# sprite setup
for file_name,pos_list in SIMPLE_OBJECTS.items():
    surf = pygame.image.load(simple_objects_path + "/" + file_name + ".png").convert_alpha()
    for pos in pos_list:
        SimpleSprite(surf,pos,[all_sprites,obstacle_sprites])

# long objects
for file_name,pos_list in LONG_OBJECTS.items():
    surf = pygame.image.load(long_objects_path + "/" + file_name + ".png").convert_alpha()
    for pos in pos_list:
        LongSprite(surf,pos,[all_sprites,obstacle_sprites])

# font
screen_color = "black"
font = pygame.font.Font(None,50)
text_surf = font.render("You Won!!!",True,"white")
text_rect = text_surf.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))


# music
game_sound = pygame.mixer.Sound(music_path)
game_sound.play(loops=1)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == car_timer:
            random_pos = choice(CAR_START_POSITIONS)
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                pos = (random_pos[0],random_pos[1] + randint(-8,8))
                Car(pos,[all_sprites,obstacle_sprites])
            if len(pos_list) > 5:
                del pos_list[0]

    # delta time
    dt = clock.tick() / 1000
    
    # screen color
    display_surface.fill(screen_color)

    # limit the areas for the player to go to
    if player.pos.y >= 1180:

        # update
        all_sprites.update(dt)

        # draw
        all_sprites.customize_draw()

    # the player won the game
    else:
        display_surface.blit(text_surf,text_rect)
        screen_color = "teal"

    # update the changes -> draw the frame
    pygame.display.update()




