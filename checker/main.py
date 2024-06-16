from settings import *
from sprites import Checker
from other import draw_board, generate_pos, display_points
import random

pygame.init()

class Game:
    def __init__(self):
        self.gameVariables()

    def gameVariables(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.all_pos = generate_pos()
        self.checking = None
        self.next_moves = set()
        self.must_select = {}
        self.turns = {RED: BLUE, BLUE: RED}
        self.turn = random.choice([RED, BLUE])
        self.winner = None  

        self.points = {RED: 12, BLUE: 12}
        self.moving = ()


    def resetGame(self):
        self.gameVariables()


    def check_winner(self):
        if self.points[self.turn] == 0:
            self.winner = self.turns[self.turn] 
            return


        if self.points[self.turn] <= 6 and not self.must_select:
            for pos in self.all_pos:
                if self.all_pos[pos].color == self.turn:
                    next_moves = set() 
                    checking = pos 
                    self.hint_of_next_move(next_moves, checking)

                    if next_moves:
                        break

            if not next_moves:
                self.winner = self.turns[self.turn]


    def check_eat_move(self, checker):
        # check if there a checker that must be selected
        # to eat the enemies checker 

        if checker.color == self.turn:
            for dy in checker.dy:
                left = (checker.y + dy, checker.x - 1) if (checker.x > 0 and 0 <= checker.y + dy <= 7 ) else (0, 0)
                right = (checker.y + dy, checker.x + 1) if (checker.x < 7 and 0 <= checker.y + dy <= 7) else (0, 0)

                if left in self.all_pos:
                    if (self.all_pos[left].color != checker.color):
                        far_left = (checker.y + dy * 2 , checker.x - 2) if (checker.x >= 2 and 0 <= checker.y + dy * 2 <= 7) else (0, 0)

                        if far_left not in self.all_pos and far_left != (0, 0): 
                            self.must_select[(checker.y, checker.x)] = {}
                            self.must_select[(checker.y, checker.x)][far_left] = left
                            checker.must_be_moved = True

                if right in self.all_pos:
                    if (self.all_pos[right].color != checker.color):
                        far_right = (checker.y + dy * 2 , checker.x + 2) if (checker.x <= 7 - 2 and 0 <= checker.y + dy * 2 <= 7) else (0, 0)

                        if far_right not in self.all_pos and far_right != (0, 0):
                            if (checker.y, checker.x) not in self.must_select:
                                self.must_select[(checker.y, checker.x)] = {}

                            self.must_select[(checker.y, checker.x)][far_right] = right
                            checker.must_be_moved = True

    def must_select_checker(self):
        for pos in self.all_pos:
            checker = self.all_pos[pos]
            self.check_eat_move(checker)
            

    def handle_checker_click(self, pos, mouse_pos):
        row, col = pos
        x, y = mouse_pos
        checker = self.all_pos[pos]

        if (not self.must_select) or (self.must_select and (row, col) in self.must_select):
            if checker.check_if_clicked((x, y)):
                self.checking = (row, col)
                self.next_moves.clear()
                self.hint_of_next_move(self.next_moves, self.checking)

                if self.next_moves: 
                    return True
                else:
                    self.checking = None


    def draw_window(self):
        self.win.fill("black")
        if not self.winner:
            pygame.draw.rect(self.win, self.turn, (0, 0, WIDTH, HEIGHT))

        
        # draw the board_game
        draw_board(self.win)

        for pos in self.all_pos:
            self.all_pos[pos].draw(self.win, self.all_pos)

        for y, x in self.next_moves: 
            x_ = OFFSET_X + x * BLOCK_SIZE + BLOCK_SIZE / 2
            y_ = y * BLOCK_SIZE + BLOCK_SIZE / 2
            pygame.draw.circle(self.win, "yellow", (x_, y_), 20)
    
        # display points 
        display_points(self.win, self.points)
    
        if self.winner:            
            font = pygame.font.SysFont("comicsans", 100)
            if self.winner == RED:
                text = font.render("RED wins", False, "black")
            else:
                text = font.render("BLUE wins", False, "black")

            pygame.draw.rect(self.win, self.winner, (0, 0, WIDTH, HEIGHT))

            self.win.blit(text, (WIDTH / 2 - text.get_width()/2,
                                HEIGHT / 2 - text.get_height()/2))



    def hint_of_next_move(self, next_moves, checking):
        checker = self.all_pos[checking]

        if self.must_select:
            for move in self.must_select[checking]:    
                next_moves.add(move)
        else:     
            #find next move if there is no checker that must be moved
            for dy in checker.dy:               
                left = (checker.y + dy, checker.x - 1) if (checker.x > 0 and 0 <= checker.y + dy <= 7 ) else (0, 0)
                right = (checker.y + dy, checker.x + 1) if (checker.x < 7 and 0 <= checker.y + dy <= 7) else (0, 0)         

                if left != (0, 0) and left not in self.all_pos: 
                    next_moves.add(left)

                if right != (0, 0) and right not in self.all_pos:
                    next_moves.add(right)
                    

    def run(self):
        run = True 

        while run:
            if not self.must_select:                   
                self.must_select_checker()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if x >= OFFSET_X and x <= OFFSET_X + 8 * BLOCK_SIZE:
                        row = y // BLOCK_SIZE 
                        col = (x - OFFSET_X) // BLOCK_SIZE
                        
                        
                        if (row, col) in self.all_pos and self.all_pos[(row, col)].color == self.turn and not self.moving:
                            self.handle_checker_click((row, col), (x, y))

                        else:
                            if self.checking:
                                if (row, col) in self.next_moves:
                                    checker = self.all_pos[self.checking]

                                    # swap the checker position self.all_pos
                                    del self.all_pos[self.checking]
                                    self.all_pos[(row, col)] = checker
                                    
                                    checker.y, checker.x = row, col
                                    self.moving = (row, col)
                                   
                                    # checking player after move
                                    checker.clicked = False
                                    checker.must_be_moved = False
                                    if checker.y == checker.king_y_pos and not checker.is_king:
                                        checker.is_king = True
                                        checker.dy = [1, -1]


                                    if self.must_select:
                                        delete_pos = self.must_select[self.checking][(row, col)]
                                        self.points[self.all_pos[delete_pos].color] -= 1
                                        del self.all_pos[delete_pos]


                                        # turn the must_be_moved to false when it wasn't moved
                                        for pos in self.must_select:
                                            if pos in self.all_pos:
                                                self.all_pos[pos].must_be_moved = False


                                        # check if checker can continue going else swap turn 
                                        self.must_select.clear()
                                        self.check_eat_move(checker)

                                        if self.must_select:
                                            self.turn = self.turns[self.turn]
                                            self.checking = (row, col)

                                    self.turn = self.turns[self.turn]
                                    self.next_moves.clear()
                                    
                                    # make a new next moves if a checker can continue going 
                                    if self.must_select:
                                        for move in self.must_select[self.checking]:    
                                            self.next_moves.add(move) 

                                    self.checking = None if not self.must_select else self.checking


            if not self.winner and not self.moving:
                self.check_winner()

            if self.moving:
                finish_moved = self.all_pos[self.moving].move(self.moving, self.moving)

                if finish_moved:
                    self.moving = ()


            self.draw_window()
            pygame.display.update()

            if self.winner:
                pygame.time.delay(1000)
                self.resetGame()

game = Game()
game.run()
pygame.quit()
quit()