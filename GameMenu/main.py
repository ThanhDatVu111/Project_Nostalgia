from button import Button
import pygame, sys
from subprocess import Popen

# Initialize pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")
bg_image = pygame.image.load("/Users/datvu/Desktop/Project/Project_Nostalgia/GameMenu/Graphic/bg.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("/Users/datvu/Desktop/Project/Project_Nostalgia/GameMenu/Graphic/font.ttf", size)

# Load the sound
pygame.mixer.music.load("/Users/datvu/Desktop/Project/Project_Nostalgia/GameMenu/Sound/bg.mp3")
pygame.mixer.music.play(-1)  # -1 means loop indefinitely
def main_menu():
    while True:
        screen.blit(bg_image, (-95, 0))
        title = get_font(40).render("PROJECT NOSTALGIA", True, "#b68f40")
        title_rect = title.get_rect(center=(405, 100))
        screen.blit(title, title_rect)

        flappy_bird_button = Button(pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-120), text_input = "FLAPPY BIRD", font=get_font(30), base_color = "#b68f40", hovering_color = "#d7fcd4")
        tetris_button = Button(pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-60), text_input = "TETRIS", font=get_font(30), base_color = "#b68f40", hovering_color = "#d7fcd4")
        space_invader_button = Button(pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), text_input = "SPACE INVADER", font=get_font(30), base_color = "#b68f40", hovering_color = "#d7fcd4")
        quit_button = Button(pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+60), text_input = "QUIT", font=get_font(30), base_color = "#b68f40", hovering_color = "#d7fcd4")

        mouse_pos = pygame.mouse.get_pos()
        for button in [flappy_bird_button, tetris_button, space_invader_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flappy_bird_button.checkForInput(mouse_pos):
                    Popen(["python3", "/Users/datvu/Desktop/Project/Project_Nostalgia/FlappyBird/flappy_bird.py"])
                    return
                if tetris_button.checkForInput(mouse_pos):
                    Popen(["python3", "/Users/datvu/Desktop/Project/Project_Nostalgia/Tetris/tetris_main.py"])
                    return
                if space_invader_button.checkForInput(mouse_pos):
                    Popen(["python3", "/Users/datvu/Desktop/Project/Project_Nostalgia/SpaceInvader/spa_inv_main.py"])
                    return
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()           
        pygame.display.update()

if __name__ == "__main__":
    main_menu()