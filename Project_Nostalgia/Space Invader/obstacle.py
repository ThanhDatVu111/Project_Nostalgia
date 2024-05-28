import pygame

class Block(pygame.sprite.Sprite):
	def __init__(block_self, x, y):
		super().__init__() #help to inherits from pygame.sprite.Sprite
		block_self.image = pygame.Surface((3,3)) #create a dimension for the block 3*3
		block_self.image.fill((128, 100, 162)) #color the block
		block_self.rect = block_self.image.get_rect(topleft = (x,y)) #create the rect and pos for block
		
grid = [[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
        [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
        [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]]

class Obstacle:
	def __init__(obs_self,x,y):
		obs_self.blocks_group = pygame.sprite.Group() #create group for block
		for row in range(len(grid)): # 13 row in total, loop from 0 - 12
			for column in range(len(grid[0])): # total size in grid[0] is 23, => colum loop from 0 - 22 for every row
				if grid[row][column] == 1:
					pos_x = x + column * 3 #since we created dimension for block as 3 x 3 so, 
					                       #we *3 to spacing each block and +x or y to custom the position
					pos_y = y + row * 3
					block = Block(pos_x, pos_y) #create a block using block class
					obs_self.blocks_group.add(block) #add into blocks_group, so when we create obs object
													 #from Obstacle class, it will have whatever obs_self have.
