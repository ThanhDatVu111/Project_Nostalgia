from subprocess import Popen
import sys,pygame
from game import Game
from button import Button
from colors import Colors

pygame.init() 
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("/Users/datvu/Documents/Project_Nostalgia/Tetris/Graphic/font.ttf", size)

title_surface = get_font(30).render("Tetris", True, Colors.white)
next_surface = get_font(20).render("Next", True, Colors.white)
score_surface = get_font(20).render("Score", True, Colors.white)

score_rect = pygame.Rect(376, 130, 170, 60)
next_rect = pygame.Rect(376, 280, 170, 180)

#set up screen
screen = pygame.display.set_mode((560, 690)) #start at 360
pygame.display.set_caption("Tetris")

# Load the image
image_side = pygame.image.load('/Users/datvu/Documents/Project_Nostalgia/Tetris/Graphic/tetris_bg.png')
new_size = (370, 220)  #Adjust the size
game_over_image = pygame.image.load('/Users/datvu/Documents/Project_Nostalgia/Tetris/Graphic/over.png')
new_size = (250, 250)  #Adjust the size
game_over_image = pygame.transform.scale(game_over_image, new_size)


#set up frame rate
clock = pygame.time.Clock() 
fps = 60

game = Game(screen, clock)

GAME_UPDATE = pygame.USEREVENT #custom event
pygame.time.set_timer(GAME_UPDATE, 250)

#set up music 
pygame.mixer.music.load("/Users/datvu/Documents/Project_Nostalgia/Tetris/Sound/bg_music.mp3")
pygame.mixer.music.play(-1)

while True:
    for event in pygame.event.get(): #loop in the event loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
    #Drawing
    score_value_surface = get_font(20).render(str(game.score), True, Colors.white)        

    screen.fill((0, 100, 0))
    screen.blit(image_side, (361, 0))
    screen.blit(title_surface, (370, 30, 50, 50))
    screen.blit(score_surface, (410, 100, 50, 50))
    screen.blit(next_surface, (420, 240, 50, 50))
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery)) #despite the score change, this function make sure it always in the center of the score box
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    if game.game_over == True:
        if game.blink_effect() == True:
            screen.blit(game_over_image, (335, 450))
        restart_button = Button(screen, (360/2) - 55, (690/2) - 100, "restart1") #create restart button with pos x, y for rect
        exit_button = Button(screen, (360/2) - 55, (690/2) - 30, "exit1")
        if restart_button.button_pressed_draw() == True:
            game.game_over = False
            game.run = True
            game.reset()
        if exit_button.button_pressed_draw() == True:
            Popen(["python3", "/Users/datvu/Documents/Project_Nostalgia/GameMenu/main.py"])
            pygame.quit()

    pygame.display.update()
    clock.tick(fps)
