#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pygame
import math
from scipy.spatial import distance
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding A_Algo")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def closedNode(self):
		return self.color == RED

	def openNode(self):
		return self.color == GREEN

	def barrier(self):
		return self.color == BLACK

	def startingNode(self):
		return self.color == ORANGE

	def endingNode(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def selectStart(self):
		self.color = ORANGE

	def visited(self):
		self.color = RED

	def openedNode(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def endNode(self):
		self.color = TURQUOISE

	def drawPath(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def markNeighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])
               
		if self.row > 0 and not grid[self.row - 1][self.col].barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1]) 
             

	def __lt__(self, other):
		return False


def heuristic(p1, p2):          #heuristic function to calculate distance
	#x1, y1 = p1
	#x2, y2 = p2
	return distance.euclidean(p1, p2)


def reconstruct_path(start, current, draw):
	while current in start:
		current = start[current]
		current.drawPath()
		draw()


def A_Algo(draw, grid, start, end):
	count = 0
	opened = PriorityQueue()
	opened.put((0, count, start))
	previous = {}
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = heuristic(start.get_pos(), end.get_pos())

	opened_hash = {start}

	while not opened.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = opened.get()[2]
		opened_hash.remove(current)

		if current == end:
			reconstruct_path(previous, end, draw)
			end.endNode()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				previous[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
				if neighbor not in opened_hash:
					count += 1
					opened.put((f_score[neighbor], count, neighbor))
					opened_hash.add(neighbor)
					neighbor.openedNode()

		draw()

		if current != start:
			current.visited()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			n = node(i, j, gap, rows)
			grid[i].append(n)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for nod in row:
			nod.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def clickedPos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def Run(win, width):
	ROWS = 30
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = clickedPos(pos, ROWS, width)
				node = grid[row][col]
				if not start and node != end:
					start = node
					start.selectStart()

				elif not end and node != start:
					end = node
					end.endNode()

				elif node != end and node != start:
					node.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = clickedPos(pos, ROWS, width)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.markNeighbors(grid)

					A_Algo(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()



Run(WIN, WIDTH)


# In[ ]:





# In[ ]:




