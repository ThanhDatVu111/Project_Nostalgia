from colors import Colors
from position import Position
import pygame

class Block:
	def __init__(self, id):
		self.id = id
		self.cells = {} #each cell have 4 tiles
		self.cell_size = 30
		self.rotation_state = 0
		self.row_offset = 0
		self.column_offset = 0
		self.colors = Colors.get_cell_colors() #returns a list of colors.
	
	def move(self, rows, columns):
		self.row_offset += rows
		self.column_offset += columns

	def rotate(self):
		self.rotation_state += 1
		if self.rotation_state == len(self.cells): #only 0,1,2,3 tiles in the dictionary cell 
			self.rotation_state = 0

	def undo_rotate(self):
		self.rotation_state -= 1
		if self.rotation_state == -1:
			self.rotation_state = len(self.cells) - 1 #= 3
		
	def get_cell_positions(self):
		tiles = self.cells[self.rotation_state]
		moved_tiles_list = []
		for i in tiles: #i refers to each Position object in the list.
			new_position = Position(i.row + self.row_offset, i.column + self.column_offset)
			moved_tiles_list.append(new_position)
		return moved_tiles_list
	
	def draw(self, screen, offset_x, offset_y):
		moved_tiles_list = self.get_cell_positions()
		for each_position in moved_tiles_list:
			tile_rect = pygame.Rect(offset_x + each_position.column * self.cell_size, offset_y + each_position.row * self.cell_size, self.cell_size -1, self.cell_size -1)
			pygame.draw.rect(screen, self.colors[self.id], tile_rect)