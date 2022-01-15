import pygame
import sys
from random import *
import pickle

class create():
    def __init__(self):
        self.body_pos = [[(randint(0, screen_width-1) * one_block), (randint(0, screen_height-1) * one_block)]]
        self.body = None
        self.head = pygame.Rect(-40, -40, one_block, one_block)
        self.body_color = (0, 0, 0)
        self.feed = pygame.Rect(randint(0, screen_width-1) * one_block, randint(0, screen_height-1) * one_block, one_block, one_block)
        self.feed_color= (0, 150, 0)
        self.to_y = 0
        self.to_x = 0
        self.score = 0
        self.dir = 0
        self.n = 0
        self.gen_n=1
        self.live =True

    def control(self):
        if self.live == False:
            return 0
        self.move()
        self.body_loop()
        self.check_f_col()
        self.check_b_col()
        self.move_head()
        self.check_roop()
        self.draw()

    def move(self):
        self.dir=randint(0, 3)
        
        if self.dir == 0:
                if self.to_x != one_block:
                    self.to_x = -one_block
                    self.to_y = 0
        elif self.dir == 1:
                if self.to_x != -one_block:
                    self.to_x = one_block
                    self.to_y = 0
        elif self.dir == 2:
                if self.to_y != one_block:
                    self.to_y = -one_block
                    self.to_x = 0
        elif self.dir == 3:
                if self.to_y != -one_block:
                    self.to_y = one_block
                    self.to_x = 0    
        

    def body_loop(self):
        self.body_pos.insert(0, [self.body_pos[0][0],self.body_pos[0][1]])
        del self.body_pos[-1]
        
    def check_f_col(self):
        self.body = pygame.Rect(self.body_pos[0][0], self.body_pos[0][1], one_block, one_block)
        if self.body.colliderect(self.feed):
            self.body_pos.insert(0, [self.body.left, self.body.top])
            self.score +=1
            self.feed = pygame.Rect(randint(0, screen_width-1) * one_block, randint(0, screen_height-1) * one_block, one_block, one_block)
            for n in range(0, self.score):
                if (self.feed.left == self.body_pos[n][0]) and (self.feed.top == self.body_pos[n][1]):
                    self.feed = pygame.Rect(randint(0, screen_width-1) * one_block, randint(0, screen_height-1) * one_block, one_block, one_block)
                    continue        
                
    def check_b_col(self):
        self.head.left = self.body_pos[0][0]
        self.head.top = self.body_pos[0][1]
        if self.score > 3:
            for n in range(3, self.score):
                self.body.left = self.body_pos[n][0]
                self.body.top = self.body_pos[n][1]
                if self.head.colliderect(self.body):
                    self.head.left = -20
                    self.head.top = -20
                    self.live = False
                    
                    
    def move_head(self):            
        self.body_pos[0][0] += self.to_x
        self.body_pos[0][1] += self.to_y

    def check_roop(self):
        if self.body_pos[0][0] > (screen_width-1) * one_block:
            self.body_pos[0][0] = 0
        if self.body_pos[0][0] < 0:
            self.body_pos[0][0] = (screen_width-1) * one_block
        if self.body_pos[0][1] > (screen_height-1) * one_block:
            self.body_pos[0][1] = 0
        if self.body_pos[0][1] < 0:
            self.body_pos[0][1] = (screen_height-1) * one_block

    def draw(self):
        pygame.draw.rect(screen, self.feed_color, self.feed, width=0)
        for body_pos in self.body_pos:
            self.body = pygame.Rect(body_pos[0], body_pos[1], one_block, one_block)
            pygame.draw.rect(screen, self.body_color, self.body, width=0)

def quit():
    pygame.quit()
    sys.exit()
    
def main():
    pygame.init()
    global screen_width, screen_height, one_block, screen

    screen_width = 10
    screen_height = 10
    one_block = 20
    
    screen = pygame.display.set_mode((screen_width * one_block, screen_height * one_block))
    pygame.display.set_caption("Snake")

    
    snake = create()
    
    while True:
        snake.control()
        pygame.display.update()
        pygame.time.Clock().tick(60)
        screen.fill((200, 200, 200))
        if(snake.live):
            pass
        else:
            quit()
    
    


if __name__ == '__main__':
    main()
