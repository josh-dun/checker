# init some game fuction
# i code those functions in a seperate file because it is long 
# but not very difficult to understand

from settings import * 
from sprites import Checker

def draw_board(win):
	colors = {BROWN: WHITE, WHITE: BROWN}

	color = WHITE
	for row in range(8):
		for col  in range(8):
			pygame.draw.rect(win, color, (row * BLOCK_SIZE + OFFSET_X , col * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

			if col != 7:
				color = colors[color]


def generate_pos():
	all_pos = {}
	color = 0 # white

	for row in range(3):
		for col in range(8):
			if color == 1:
				all_pos[(row, col)] = Checker(col, row, BLUE)

			if col != 7:
				color = (color + 1) % 2 

	color = 1
	for row in range(5, 8):
		for col in range(8):
			if color == 1:
				all_pos[(row, col)] = Checker(col, row, RED)

			if col != 7:
				color = (color + 1) % 2 


	return all_pos


def display_points(win, points):
	font = pygame.font.SysFont("comicsans", 30)
	text = font.render(str(points[BLUE]), True, BLUE)
	pygame.draw.circle(win, WHITE, (25, BLOCK_SIZE / 2 * 5), 25)
	pygame.draw.circle(win, "black", (25, BLOCK_SIZE / 2 * 5), 25, 2)
	win.blit(text, (25 - text.get_width() / 2, BLOCK_SIZE / 2 * 5 - 1 - text.get_height()/2))

	text2 = font.render(str(points[RED]), True, RED)
	pygame.draw.circle(win, WHITE, (25, BLOCK_SIZE / 2 * 11), 25)
	pygame.draw.circle(win, "black", (25, BLOCK_SIZE / 2 * 11), 25, 2)
	win.blit(text2, (25 - text2.get_width() / 2, BLOCK_SIZE / 2 * 11 - 1 - text2.get_height() / 2))