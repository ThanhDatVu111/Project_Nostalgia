import pygame

class Lazer(pygame.sprite.Sprite):
    def __init__(lazer_self, postition, speed, screen_height):
        super().__init__() #invoke the constructor of the parent class.
        original_image = pygame.image.load("/Users/datvu/Desktop/Project/Project_Nostalgia/SpaceInvader/Graphic/laser.png").convert_alpha()
        new_size = (20, 20)  #Adjust the size
        lazer_self.image = pygame.transform.scale(original_image, new_size) # Scale the original image to the new size
        lazer_self.rect = lazer_self.image.get_rect(center = postition)
        lazer_self.speed = speed
        lazer_self.screen_height = screen_height

    def update(lazer_self):
        lazer_self.rect.y -= lazer_self.speed
        if lazer_self.rect.y > lazer_self.screen_height + 35 or lazer_self.rect.y < -35:
            lazer_self.kill()