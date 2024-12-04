import pygame 
from lazer import Lazer

class Spaceship(pygame.sprite.Sprite):
    def __init__(ship_self, SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET):
        super().__init__() #invoke the constructor of the parent class.
        ship_self.screen_width = SCREEN_WIDTH
        ship_self.screen_height = SCREEN_HEIGHT
        ship_self.offset = OFFSET
        original_image = pygame.image.load("/Users/datvu/Desktop/Project/Project_Nostalgia/SpaceInvader/Graphic/ship_trans.png").convert_alpha()
        new_size = (90, 90)  #Adjust the size
        ship_self.image = pygame.transform.scale(original_image, new_size) # Scale the original image to the new size
        ship_self.rect = ship_self.image.get_rect(midbottom = ((ship_self.screen_width + ship_self.offset)/2, ship_self.screen_height - 20)) 
        #create a rectangle for on the ship image (for collision) and set position
        ship_self.speed = 5.0
        ship_self.lazer_group = pygame.sprite.Group()
        ship_self.lazer_ready = True
        ship_self.lazer_time = 0
        ship_self.lazer_delay = 300
        ship_self.shoot_sound = pygame.mixer.Sound("/Users/datvu/Desktop/Project/Project_Nostalgia/SpaceInvader/Sound/laser.ogg")

    def get_user_input(ship_self):
        key_pressed = pygame.key.get_pressed()     
        if key_pressed[pygame.K_RIGHT]:
            ship_self.rect.x += ship_self.speed
        if key_pressed[pygame.K_LEFT]:
            ship_self.rect.x -= ship_self.speed
        if key_pressed[pygame.K_SPACE] and ship_self.lazer_ready == True:
            lazer = Lazer((ship_self.rect.center[0], ship_self.rect.centery - 40), 5, ship_self.screen_height)
            ship_self.lazer_group.add(lazer)
            ship_self.lazer_time = pygame.time.get_ticks()
            ship_self.lazer_ready = False
            ship_self.shoot_sound.play()

    def constrain_movement(ship_self):
        if ship_self.rect.right > ship_self.screen_width:
            ship_self.rect.right = ship_self.screen_width
        if ship_self.rect.left < ship_self.offset:
            ship_self.rect.left = ship_self.offset

    def recharge_lazer(ship_self):
        if ship_self.lazer_ready == False:
            current_time = pygame.time.get_ticks()
            if current_time - ship_self.lazer_time >= ship_self.lazer_delay:
                ship_self.lazer_ready = True

    def update(ship_self):
        ship_self.get_user_input()
        ship_self.constrain_movement()
        ship_self.lazer_group.update()
        ship_self.recharge_lazer()
    
    def reset(ship_self):
        ship_self.rect = ship_self.image.get_rect(midbottom = ((ship_self.screen_width + ship_self.offset)/2, ship_self.screen_height - 20))
        ship_self.lazer_group.empty()