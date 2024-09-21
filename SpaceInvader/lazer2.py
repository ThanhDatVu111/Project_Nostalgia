import pygame

class Lazer2(pygame.sprite.Sprite):
    def __init__(lazer_self2, postition, speed, screen_height):
        super().__init__() #invoke the constructor of the parent class.
        original_image = pygame.image.load("/Users/datvu/Documents/Project_Nostalgia/SpaceInvader/Graphic/laser2.png").convert_alpha()
        new_size = (20, 20)  #Adjust the size
        lazer_self2.image = pygame.transform.scale(original_image, new_size) # Scale the original image to the new size
        lazer_self2.rect = lazer_self2.image.get_rect(center = postition)
        lazer_self2.speed = speed
        lazer_self2.screen_height = screen_height

    def update(lazer_self2):
        lazer_self2.rect.y -= lazer_self2.speed
        if lazer_self2.rect.y > lazer_self2.screen_height + 35 or lazer_self2.rect.y < -35:
            lazer_self2.kill()