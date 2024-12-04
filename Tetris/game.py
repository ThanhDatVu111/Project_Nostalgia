import pygame
from grid import Grid
from block_types import *
import random

class Game:
	def __init__(self, screen, clock):
		self.grid = Grid()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.game_over = False
		self.screen = screen
		self.score = 0
		self.clock = clock
		self.blink_visible = True #Variable to toggle visibility
		self.blink_timer = 0
		self.blink_interval = 500 #blink img every 500ms
		# Load the sound
		self.clear_sound = pygame.mixer.Sound("/Users/datvu/Desktop/Project/Project_Nostalgia/Tetris/Sound/Sounds_clear.ogg") 
		self.rotates_sound = pygame.mixer.Sound("/Users/datvu/Desktop/Project/Project_Nostalgia/Tetris/Sound/Sounds_rotate.ogg") 

	def update_score(self, lines_cleared, move_down_points):
		if lines_cleared == 1:
			self.clear_sound.play()
			self.score += 100
		elif lines_cleared == 2:
			self.clear_sound.play()
			self.score += 300
		elif lines_cleared == 3:
			self.clear_sound.play()
			self.score += 500
		self.score += move_down_points
	
	def get_random_block(self):
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = random.choice(self.blocks)
		self.blocks.remove(block) #appear one every random cycle
		return block
	
	def move_left(self):
		self.current_block.move(0, -1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, 1)

	def move_right(self):
		self.current_block.move(0, 1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, -1)
		
	def move_down(self):
		self.current_block.move(1, 0)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(-1, 0)
			self.lock_block()

	def block_fits(self):
		tiles_list = self.current_block.get_cell_positions()
		for each_position in tiles_list:
			if self.grid.is_empty(each_position.row, each_position.column) == False: #if that grid position is != 0
				return False
		return True

	def lock_block(self):
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id #marking a specific position on the grid as occupied by the current block, using the block's id
		self.current_block = self.next_block #spawn new bock
		self.next_block = self.get_random_block() #set up next block for next iteration
		rows_cleared = self.grid.clear_full_rows()
		self.update_score(rows_cleared, 0)
		if self.block_fits() == False: #checking the new spawn current block
			self.game_over = True

	def rotate(self):
		self.current_block.rotate()
		self.rotates_sound.play()
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.undo_rotate()
		
	def block_inside(self):
		moved_tiles_list = self.current_block.get_cell_positions()
		for i in moved_tiles_list:
			if self.grid.is_inside(i.row, i.column) == False:
				return False
		return True
	
	def draw(self, screen):
		self.grid.draw(screen)
		self.current_block.draw(screen, 0, 0)
		if self.next_block.id == 3:
			self.next_block.draw(screen, 285, 360)
		elif self.next_block.id == 4:
			self.next_block.draw(screen, 285, 340)
		elif self.next_block.id == 5:
			self.next_block.draw(screen, 270, 340)
		else:
			self.next_block.draw(screen, 300, 340)

	def blink_effect(self):
		self.blink_timer += self.clock.get_time()
		if self.blink_timer >= self.blink_interval:
			self.blink_timer = 0
			self.blink_visible = not self.blink_visible #reverse boolean variable to toggle
		return self.blink_visible

	def reset(self):
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.score = 0