import tensorflow as tf
import time, shutil, os
import pygame
import sys
from random import *
import pickle

class create():
    def __init__(self, pre_dir):
        self.body_pos = [[(randint(0, screen_width-1) * one_block), (randint(0, screen_height-1) * one_block)]]
        self.body = None
        self.head = pygame.Rect(-40, -40, one_block, one_block)
        self.body_color = (0, 0, 0)
        self.feed = pygame.Rect(randint(0, screen_width-1) * one_block, randint(0, screen_height-1) * one_block, one_block, one_block)
        self.feed_color= (0, 150, 0)
        self.to_y = 0
        self.to_x = 0
        self.score = 0
        self.dir = []
        self.n = 0
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
        if len(self.pre_dir) == 0:
            self.dir.append(randint(0, 3))
        else:
            #print(self.dir, self.pre_dir, self.n)
            if len(self.dir) == self.n:
                self.dir.append(randint(0, 3))
            else:
                self.dir.append(self.pre_dir[self.n])
        
        if self.dir[self.n] == 0:
                if self.to_x != one_block:
                    self.to_x = -one_block
                    self.to_y = 0
        elif self.dir[self.n] == 1:
                if self.to_x != -one_block:
                    self.to_x = one_block
                    self.to_y = 0
        elif self.dir[self.n] == 2:
                if self.to_y != one_block:
                    self.to_y = -one_block
                    self.to_x = 0
        elif self.dir[self.n] == 3:
                if self.to_y != -one_block:
                    self.to_y = one_block
                    self.to_x = 0        
        self.n +=1
        

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

    def print(self, n):
        fw = open('gen-v.txt', 'w')
        for i in self.dir:
            fw.write(str(i))
        fw.write('\n')
        fw.close()
        print (str(n)+'번째 객체 저장되엇습니다.')
        print (self.dir)

def quit():
    pygame.quit()
    sys.exit()

def generate():
    pre_gen = []
    spa_gen = []
    fr = open('gen-v.txt', 'r')
    bin_gen = fr.readlines()
    fr.close()
    print(bin_gen)
    for i in range(0, len(bin_gen)):
        for z in range(0, len(bin_gen[i])):
            if bin_gen[i][z] == '\n':
                break
            pre_gen.append(int(bin_gen[i][z]))
    print(pre_gen)
    return pre_gen

def g_create(n, pre_dir = []):
    for z in range(0, n):
        world.append(create(pre_dir))
    
def main():
    pygame.init()
    global world, play, screen_width, screen_height, one_block, screen, chr_n, gen_n, n, fw, fr

    screen_width = 10
    screen_height = 10
    one_block = 20
    world = []
    chr_n = 1
    gen_n = 1
    play = True
    n =int(input('개체 수:'))
    g_create(n)
    
    screen = pygame.display.set_mode((screen_width * one_block, screen_height * one_block))
    pygame.display.set_caption("Snake")
    game_font = pygame.font.Font(None, 40)

    
    
    
    while True:
        if len(world) == 0:
            exit()
            
        pygame.display.update()
        pygame.time.Clock().tick(60)
        screen.fill((200, 200, 200))
        for i in world:
            i.control()
            if i.live == False:
                i.print(chr_n)
                chr_n += 1
                world.remove(i)
    
    quit()


if __name__ == '__main__':
    main()
