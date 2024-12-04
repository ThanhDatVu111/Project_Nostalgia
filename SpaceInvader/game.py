import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from lazer2 import Lazer2
from alien import MysteryShip
from explosion import Explosion
from button import Button

class Game:
    def __init__(game_self, SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET, game_clock): #automatically executed when an instance of that class is created
        game_self.screen_width = SCREEN_WIDTH
        game_self.screen_height = SCREEN_HEIGHT
        game_self.offset = OFFSET
        game_self.game_clock = game_clock
        game_self.spaceship_group = pygame.sprite.GroupSingle()
        game_self.spaceship_group.add(Spaceship(game_self.screen_width, game_self.screen_height, game_self.offset))
        game_self.obstacles_list = game_self.create_obstacles()
        game_self.aliens_group = pygame.sprite.Group()
        game_self.create_alien()
        game_self.aliens_direction = 1
        game_self.alien_lazers_group = pygame.sprite.Group()
        game_self.mystery_ship_group = pygame.sprite.GroupSingle()
        game_self.explosion_group = pygame.sprite.Group()
        game_self.live_remain = 5
        game_self.run = True
        game_self.game_over_img = pygame.image.load("/Users/datvu/Desktop/Project/Project_Nostalgia/SpaceInvader/Graphic/game_over.png").convert_alpha()
        game_self.game_over_img = pygame.transform.scale(game_self.game_over_img, (400,400))
        game_self.restart_button = Button((SCREEN_WIDTH - 120)/2 + 20, SCREEN_HEIGHT - 350, "restart1") #create restart button with pos x, y for rect
        game_self.exit_button = Button((SCREEN_WIDTH - 120)/2 + 20, SCREEN_HEIGHT - 280, "exit1")
        game_self.blink_visible = True #Variable to toggle visibility
        game_self.blink_timer = 0
        game_self.blink_interval = 500 #blink img every 500ms
        game_self.score = 0
        game_self.highscore = 0
        game_self.load_highest_score() #load from high_score.txt file for the last highest score
        game_self.explosion_sound = pygame.mixer.Sound("/Users/datvu/Desktop/Project/Project_Nostalgia/SpaceInvader/Sound/explosion.ogg")
        game_self.hit_sound = pygame.mixer.Sound("/Users/datvu/Desktop/Project/Project_Nostalgia/SpaceInvader/Sound/hit.wav")
        game_self.mshit_sound = pygame.mixer.Sound("/Users/datvu/Desktop/Project/Project_Nostalgia/SpaceInvader/Sound/ms.wav")


    def create_obstacles(game_self):
        obstacle_width = len(grid[0]) * 3 #23 * 3 = 69 , length of one obstacle
        gap = ((game_self.screen_width + game_self.offset) - (4 * obstacle_width))/5
        obstacles_list = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, game_self.screen_height - 175) #create 1 obstacle
            obstacles_list.append(obstacle)
        return obstacles_list #this list will hold 5 obstacles with calculated position

    def create_alien(game_self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + row * 55
                if row == 0:
                    alien_type = 5
                elif row == 1:
                    alien_type = 4
                elif row == 2:
                    alien_type = 3
                elif row == 3:
                    alien_type = 2
                else:
                    alien_type = 1
                alien = Alien(alien_type, x + game_self.offset, y + game_self.offset)
                game_self.aliens_group.add(alien)

    def move_aliens(game_self):
        game_self.aliens_group.update(game_self.aliens_direction)
        aliens_sprite_list = game_self.aliens_group.sprites()
        for alien in aliens_sprite_list: #if the alien at the end or start of the list hit the left or right barrier, 
                                         #it change the direction for all the alien
            if alien.rect.right >= game_self.screen_width + game_self.offset/2:
                game_self.aliens_direction = -1
                game_self.move_aliens_down(2)
            elif alien.rect.left <= game_self.offset/2:
                game_self.aliens_direction = 1
                game_self.move_aliens_down(2)

    def move_aliens_down(game_self, distance):
        aliens_sprite_list = game_self.aliens_group.sprites()
        if aliens_sprite_list:
            for alien in aliens_sprite_list:
                alien.rect.y += distance

    def alien_shoot_lazer(game_self):
        if game_self.aliens_group.sprites():
            random_alien = random.choice(game_self.aliens_group.sprites())
            laser_sprite = Lazer2(random_alien.rect.center, -6, game_self.screen_height)
            game_self.alien_lazers_group.add(laser_sprite)

    def create_mystery_ship(game_self):
         game_self.mystery_ship_group.add(MysteryShip(game_self.screen_width, game_self.offset))

    def check_for_collision(game_self):
        if game_self.spaceship_group.sprite.lazer_group: #if spaceship shoot lazer, lazer exist in the lazer group
            for ship_lazer_sprite in game_self.spaceship_group.sprite.lazer_group:
                alien_hit_list =  pygame.sprite.spritecollide(ship_lazer_sprite, game_self.aliens_group, True)
                if alien_hit_list: #when collide, the third argument set to True mean the laser is been remove
                                   #so inside the list only contain the alian that got collide.
                    for alien in alien_hit_list:
                        game_self.score += alien.type * 100 #adding score for each type of alien
                        game_self.check_highest_score()
                        ship_lazer_sprite.kill()
                        explosion = Explosion(ship_lazer_sprite.rect.centerx, ship_lazer_sprite.rect.centery, 2)
                        game_self.explosion_group.add(explosion)
                        game_self.explosion_sound.play()
                    
                if pygame.sprite.spritecollide(ship_lazer_sprite, game_self.mystery_ship_group, True):
                    game_self.score += 1000
                    ship_lazer_sprite.kill()
                    explosion = Explosion(ship_lazer_sprite.rect.centerx, ship_lazer_sprite.rect.centery, 3)
                    game_self.explosion_group.add(explosion)
                    game_self.mshit_sound.play()

                for obstacle in game_self.obstacles_list:
                    if pygame.sprite.spritecollide(ship_lazer_sprite, obstacle.blocks_group, True):
                        ship_lazer_sprite.kill()
                        explosion = Explosion(ship_lazer_sprite.rect.centerx, ship_lazer_sprite.rect.centery, 1)
                        game_self.explosion_group.add(explosion)

        if game_self.alien_lazers_group: #if alien shoot lazer
            for alien_lazer_sprite in game_self.alien_lazers_group:
                if pygame.sprite.spritecollide(alien_lazer_sprite, game_self.spaceship_group, False):
                    alien_lazer_sprite.kill()
                    explosion = Explosion(alien_lazer_sprite.rect.centerx, alien_lazer_sprite.rect.centery, 1)
                    game_self.explosion_group.add(explosion)
                    game_self.live_remain -= 1
                    game_self.hit_sound.play()
                    if game_self.live_remain == 0:
                        game_self.game_over()

                for obstacle in game_self.obstacles_list:
                    if pygame.sprite.spritecollide(alien_lazer_sprite, obstacle.blocks_group, True):
                        alien_lazer_sprite.kill()
                        explosion = Explosion(alien_lazer_sprite.rect.centerx, alien_lazer_sprite.rect.centery, 1)
                        game_self.explosion_group.add(explosion)

        if game_self.aliens_group: #if alien collide with obstacle or spaceship
            for alien in game_self.aliens_group:
                for obstacle in game_self.obstacles_list:
                    if pygame.sprite.spritecollide(alien, obstacle.blocks_group, True):
                        pass
                if pygame.sprite.spritecollide(alien, game_self.spaceship_group, False):
                    explosion = Explosion(game_self.spaceship_group.rect.centerx, game_self.spaceship_group.rect.centery, 3)
                    game_self.explosion_group.add(explosion)
                    game_self.live_remain -= 1
                    if game_self.live_remain == 0:
                        game_self.game_over()

    def blink_effect(game_self):
        game_self.blink_timer += game_self.game_clock.get_time()
        if game_self.blink_timer >= game_self.blink_interval:
            game_self.blink_timer = 0
            game_self.blink_visible = not game_self.blink_visible #reverse boolean variable to toggle
        return game_self.blink_visible

    def game_over(game_self):
        game_self.run = False

    def reset(game_self): #essentially reconfiguring the existing object to a fresh state, 
                          #but we avoid recreating the entire object from scratch
        game_self.aliens_group.empty()
        game_self.alien_lazers_group.empty()
        game_self.mystery_ship_group.empty()
        game_self.obstacles_list.clear()
        #reset after deleting 
        game_self.run = True
        game_self.live_remain = 5
        game_self.spaceship_group.sprite.reset() #one sprite only(ship), reset location and lazer
        game_self.obstacles_list = game_self.create_obstacles()
        game_self.create_alien()
        game_self.score = 0

    def load_highest_score(game_self):
        try:
            with open("high_score.txt", 'r') as file:
                game_self.highscore = int(file.read())
        except FileNotFoundError: #try and except for only the first time it run.
            game_self.highscore = 0

    def check_highest_score(game_self):
        if (game_self.score > game_self.highscore):
            game_self.highscore = game_self.score
            with open("high_score.txt", 'w') as file: #write mode ('w') will replace the existing content of the file with the new content
                file.write(str(game_self.highscore))