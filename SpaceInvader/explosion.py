import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(explosion_self, x, y, size):
        super().__init__()
        explosion_self.images = [] #list to hold explosion image
        for i in range(1, 6): # 1 to 5
            org_img = pygame.image.load(f"/Users/datvu/Documents/Project_Nostalgia/SpaceInvader/Graphic/exp{i}.png")
            if size == 1:
                explosion_img = pygame.transform.scale(org_img, (20, 20))
            if size == 2:
                explosion_img = pygame.transform.scale(org_img, (50, 50))
            if size == 3:
                explosion_img = pygame.transform.scale(org_img, (140, 140))
            explosion_self.images.append(explosion_img) #add the image to the list
        explosion_self.index = 0
        explosion_self.image = explosion_self.images[explosion_self.index]
        explosion_self.rect = explosion_self.image.get_rect(center = [x, y]) #get image rect and position the image also position the rect
        explosion_self.counter = 0


    def update(explosion_self):
        explosion_loop_duration = 5
        #update explosion animation
        explosion_self.counter += 1
        if explosion_self.counter >= explosion_loop_duration and explosion_self.index <= len(explosion_self.images) - 1:
            #if exceed the loop duration(3) and make sure the index <= 4 (0-4) so it's not traverse out side of the list (index error)
            explosion_self.counter = 0
            explosion_self.index += 1
            explosion_self.image = explosion_self.images[explosion_self.index]

        if explosion_self.index >= len(explosion_self.images) - 1 and explosion_self.index == len(explosion_self.images) - 1: 
            #if it's go over the loop duration and need to change the image and it reach the last image in the image list
            explosion_self.kill()