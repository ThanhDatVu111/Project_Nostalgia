from subprocess import Popen
import pygame, sys, random
from game import Game

pygame.init()
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50
WHITE = (255, 255, 255)

font = pygame.font.Font("/Users/datvu/Documents/Project_Nostalgia/SpaceInvader/Graphic/font.ttf", 20)
level_msg = font.render("LEVEL 1", False, WHITE)
credit_msg = font.render("Creator: Thanh Dat Vu", False, WHITE)
score_msg = font.render("SCORE", False, WHITE)
highscore_msg = font.render("HIGHEST SCORE", False, WHITE)

game_screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET))
pygame.display.set_caption("🚀🛸 SPACE INVADER 🛸🚀")

FPS = 60
game_clock = pygame.time.Clock()
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET, game_clock)
bg = pygame.image.load("/Users/datvu/Documents/Project_Nostalgia/SpaceInvader/Graphic/space_bg.png")

SHOOT_LAZER = pygame.USEREVENT #USEREVENT help me to create my own event in this game
pygame.time.set_timer(SHOOT_LAZER, 300) # trigger this SHOOT_LAZER every 300 milliseconds. 

MYSTERY_SHIP_SPAWN = pygame.USEREVENT + 1 #create a new event ID that is distinct from the one represented by pygame.USEREVENT
pygame.time.set_timer(MYSTERY_SHIP_SPAWN, random.randint(4000,8000)) #trigger ms spawn every 4 to 8 seconds. 

pygame.mixer.music.load("/Users/datvu/Documents/Project_Nostalgia/SpaceInvader/Sound/bg.mp3")
pygame.mixer.music.play(-1)

#game loop
while True:
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() #close window
        if event.type == SHOOT_LAZER and game.run == True:
            game.alien_shoot_lazer()
        if event.type == MYSTERY_SHIP_SPAWN and game.run == True:
            game.create_mystery_ship()

    #updating
    if game.run == True:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lazers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collision()
        game.explosion_group.update()

    #user interface
    game_screen.blit(bg, (0, 0)) #update background
    pygame.draw.rect(game_screen, WHITE, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(game_screen, WHITE, (25, 730), (775, 730), 3)
    if game.run == True:
        game_screen.blit(level_msg, (570, 750, 50, 50))
    else:
        game_screen.blit(credit_msg, (200, 750, 50, 50))

    x = 50
    spaceship_life = pygame.image.load("/Users/datvu/Documents/Project_Nostalgia/SpaceInvader/Graphic/spaceship_life.png").convert_alpha()
    for life in range(game.live_remain):
        game_screen.blit(spaceship_life, (x, 745))
        x += 50

    game_screen.blit(score_msg, (50, 25, 50, 50))
    game_screen.blit(highscore_msg, (500, 25, 50, 50))
    formatted_score = str(game.score).zfill(5) #if the length of the string representation of game.score is less than 5, 
                                               #it will add zeros to the left side of the string to make it 5 characters long
    score_surface = font.render(formatted_score, False, WHITE)
    formatted_highscore = str(game.highscore).zfill(5) 
    highscore_surface = font.render(formatted_highscore, False, WHITE)
    game_screen.blit(score_surface, (50, 50, 50, 50))
    game_screen.blit(highscore_surface, (600, 50, 50, 50))

    game.spaceship_group.draw(game_screen)
    game.spaceship_group.sprite.lazer_group.draw(game_screen)
    game.aliens_group.draw(game_screen)
    game.alien_lazers_group.draw(game_screen)
    game.mystery_ship_group.draw(game_screen)
    game.explosion_group.draw(game_screen)
    for obs in game.obstacles_list: #drawing obstacle by looping through the list that create_obstacle() return
        obs.blocks_group.draw(game_screen)
    
    if game.run == False:
        if game.blink_effect() == True:
            game_screen.blit(game.game_over_img,((SCREEN_WIDTH - 400)/2 + 20, (SCREEN_HEIGHT - 400)/2 - 100)) #blit function handle position
            game_screen.blit(game.restart_button.image,((SCREEN_WIDTH - 120)/2 + 20, SCREEN_HEIGHT - 350))
            game_screen.blit(game.exit_button.image,((SCREEN_WIDTH - 120)/2 + 20, SCREEN_HEIGHT - 280))
        if game.restart_button.button_pressed() == True:
            game.run = True
            game.reset()
        if game.exit_button.button_pressed() == True:
            game.run = False
            Popen(["python3", "/Users/datvu/Documents/Project_Nostalgia/GameMenu/main.py"])
            pygame.quit()

    pygame.display.update()
    game_clock.tick(FPS)
    