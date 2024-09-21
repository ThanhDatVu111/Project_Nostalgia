import pygame, random

class Alien(pygame.sprite.Sprite):
    def __init__(alien_self, alien_type, x, y):
        super().__init__() 
        alien_self.type = alien_type #use type tribute for graphic and score
        path = f"/Users/datvu/Documents/Project_Nostalgia/SpaceInvader/Graphic/alien_{alien_self.type}.png"
        alien_self.image = pygame.image.load(path).convert_alpha()
        alien_self.rect = alien_self.image.get_rect(topleft = (x, y))

    def update(alien_self, aliens_direction):
        alien_self.rect.x += aliens_direction

class MysteryShip(pygame.sprite.Sprite):
    def __init__(ms_self, screen_width, offset):
        super().__init__() 
        ms_self.screen_width = screen_width
        ms_self.offset = offset 
        original_image = pygame.image.load("/Users/datvu/Documents/Project_Nostalgia/SpaceInvader/Graphic/mystery.png").convert_alpha()
        new_size = (90, 90)  #Adjust the size
        ms_self.image = pygame.transform.scale(original_image, new_size)
        x = random.choice([ms_self.offset/2, ms_self.screen_width + ms_self.offset - ms_self.image.get_width()]) #random in list for position at offset/2 or 
                                                                                                                 #the position of the picture nearest to the right border
        if x == ms_self.offset/2: #at the start
            ms_self.speed = 3
        else: #or the end 
            ms_self.speed = -3
        ms_self.rect = ms_self.image.get_rect(topleft = (x, 80))

    def update(ms_self):
        ms_self.rect.x += ms_self.speed
        if ms_self.rect.right > ms_self.screen_width + ms_self.offset/2:
            ms_self.kill()
        elif ms_self.rect.left < ms_self.offset/2:
            ms_self.kill()
