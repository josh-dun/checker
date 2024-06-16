from settings import * 

class Checker:
    def __init__(self, x, y, color):
        self.x = x 
        self.y = y 
        self.radius = 20
        self.color = color
        self.clicked = False
        self.next_moves = set()
        self.is_king = False
        self.must_be_moved = False 
        self.outline = 5 

        self.dy = [1] if self.color == BLUE else [-1]
        self.king_y_pos = 7 if self.color == BLUE else 0

        self.x_pos = OFFSET_X + self.x * BLOCK_SIZE + BLOCK_SIZE / 2
        self.y_pos = self.y * BLOCK_SIZE + BLOCK_SIZE / 2
        
        self.move_direction = pygame.Vector2()
        self.speed = 4

    def draw(self, win, all_pos):
        # draw shape when it must be moved
        if self.must_be_moved:
            pygame.draw.polygon(win, "black", (
                    (self.x_pos, self.y_pos - BLOCK_SIZE / 2), 
                    (self.x_pos - BLOCK_SIZE / 5, self.y_pos - BLOCK_SIZE / 4), 
                    (self.x_pos - BLOCK_SIZE / 2, self.y_pos),
                    (self.x_pos - BLOCK_SIZE / 5, self.y_pos + BLOCK_SIZE / 4),
                    (self.x_pos, self.y_pos + BLOCK_SIZE / 2),
                    (self.x_pos + BLOCK_SIZE / 5, self.y_pos + BLOCK_SIZE / 4),
                    (self.x_pos + BLOCK_SIZE / 2, self.y_pos),
                    (self.x_pos + BLOCK_SIZE / 5, self.y_pos - BLOCK_SIZE / 4),
                    (self.x_pos, self.y_pos - BLOCK_SIZE / 2), 
                    ))

        # draw the ball
        pygame.draw.circle(win, self.color, (self.x_pos, self.y_pos), self.radius)

        # draw the outline
        pygame.draw.circle(win, "black", (self.x_pos, self.y_pos), self.radius+self.outline, self.outline)


        # draw the crown on the circle if it's a king
        if self.is_king:
            pygame.draw.polygon(win, "black", (
                (self.x_pos - 5, self.y_pos - 10), 
                (self.x_pos, self.y_pos - 3), 
                (self.x_pos + 5, self.y_pos - 10),
                (self.x_pos + 5, self.y_pos + 5),
                (self.x_pos - 5, self.y_pos + 5)))

        
            
    def check_if_clicked(self, point):
        x, y = point

        if (x - self.x_pos) ** 2 + (y - self.y_pos) ** 2 <= (self.radius + self.outline) ** 2:  
            self.clicked = True
            return True 

    def move(self, pos, end_move):
        y, x = pos
        new_x = OFFSET_X + x * BLOCK_SIZE + BLOCK_SIZE / 2
        new_y = y * BLOCK_SIZE + BLOCK_SIZE / 2

        # determine the checker will go up or down, left or right
        if not self.move_direction.x:
            if self.x_pos < new_x:
                self.move_direction.x = self.speed
            else:
                self.move_direction.x = -self.speed


            if self.y_pos < new_y:
                self.move_direction.y = self.speed
            else:
                self.move_direction.y = -self.speed


            self.y, self.x = pos


        # moving the circle
        self.x_pos += self.move_direction.x 
        self.y_pos += self.move_direction.y

        if ((self.y_pos >= new_y and self.move_direction.y > 0) or 
            (self.y_pos <= new_y and self.move_direction.y < 0)):

            self.x_pos = OFFSET_X + self.x * BLOCK_SIZE + BLOCK_SIZE / 2
            self.y_pos = self.y * BLOCK_SIZE + BLOCK_SIZE / 2   
            self.move_direction = pygame.Vector2()
            return True 

        return False



