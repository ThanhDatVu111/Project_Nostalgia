import pygame
from colors import Colors

class Grid:
	def __init__(self):
		self.num_rows = 23 #690/30 = 23
		self.num_cols = 12 #360/30 = 12
		self.cell_size = 30
		self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)] # 0 is placed for j and one iteration of colum loop is placed for i
		self.colors_list = Colors.get_cell_colors()

	def is_inside(self, row, column):
		if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
			return True
		return False
	
	def is_empty(self,row,column):
		if self.grid[row][column] == 0:
			return True
		return False
	
	def is_row_full(self, row):
		for column in range(self.num_cols):
			if self.grid[row][column] == 0:
				return False
		return True
	
	def clear_row(self, row):
		for column in range(self.num_cols):
			self.grid[row][column] = 0

	def move_row_down(self, row, completed_num_rows):
		for column in range(self.num_cols):
			self.grid[row + completed_num_rows][column] = self.grid[row][column]
			self.grid[row][column] = 0

	def clear_full_rows(self):
		completed = 0
		for row in range(self.num_rows - 1, 0, -1): #last row going up to first row (22 - 1 until 0 and -1 for every iteration)
			if self.is_row_full(row):
				self.clear_row(row)
				completed += 1
			elif completed > 0:
				self.move_row_down(row, completed)
		return completed

	def draw(self, screen):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				cell_value = self.grid[row][column]
				cell_rect = pygame.Rect(column*self.cell_size + 1, row*self.cell_size + 1, self.cell_size - 1, self.cell_size - 1) #x, y, height, width
				pygame.draw.rect(screen, self.colors_list[cell_value], cell_rect)
	
	def reset(self):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				self.grid[row][column] = 0
