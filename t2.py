# coding=UTF-8
#!/usr/bin/env python
import pygame,sys,time,random
from pygame.locals import *
import numpy as np
import copy
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
redColour = pygame.Color(255,0,0)
class game:
    def __init__(self):
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        self.playSurface = pygame.display.set_mode((300,500))
        pygame.display.set_caption('Raspberry Snake')
        self.snakePosition = [140,240]
        self.snakeSegments = [[140,240]]
        x = random.randrange(0,15)
        y = random.randrange(0,25)
        self.raspberryPosition = [int(x*20),int(y*20)]
        self.raspberrySpawned = 1
        a=random.randint(0,3)
        if a==0:
            self.direction = 'right'
        if a==1:
            self.direction = 'left'
        if a==2:
            self.direction = 'up'
        if a==3:
            self.direction = 'down'
        self.changeDirection = self.direction
    def frame_step(self,input_actions):
        q=0  
        terminal=False 
        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        if input_actions[0]==1:
            self.changeDirection = 'right'
        if input_actions[1]==1:
            self.changeDirection = 'left'
        if input_actions[2]==1:
            self.changeDirection = 'up'
        if input_actions[3]==1:
            self.changeDirection = 'down'

        if input_actions[0]==1 and not self.direction == 'left':
            self.direction = self.changeDirection
        if input_actions[1]==1 and not self.direction == 'right':
            self.direction = self.changeDirection
        if input_actions[2]==1 and not self.direction == 'down':
            self.direction = self.changeDirection
        if input_actions[3]==1 and not self.direction == 'up':
            self.direction = self.changeDirection
        # 根据方向移动蛇头的坐标
        if self.direction == 'right':
            self.snakePosition[0] += 20
            
        if self.direction == 'left':
            self.snakePosition[0] -= 20
         
        if self.direction == 'up':
            self.snakePosition[1] -= 20
           
        if self.direction == 'down':
            self.snakePosition[1] += 20
            
        # 增加蛇的长度
        self.snakeSegments.insert(0,list(self.snakePosition))
        
        # 判断是否吃掉了树莓
        if self.snakePosition[0] == self.raspberryPosition[0] and self.snakePosition[1] == self.raspberryPosition[1]:
            self.raspberrySpawned = 0
        else:
            self.snakeSegments.pop()
        # 如果吃掉树莓，则重新生成树莓
        if self.raspberrySpawned == 0:
            while(True):
                x = random.randrange(0,15)
                y = random.randrange(0,25)
                self.raspberryPosition = [int(x*20),int(y*20)]
                for position in self.snakeSegments:
                    if position==self.raspberryPosition:
                        q=1
                if q==1:
                    q=0
                    continue
                else:
                    break
            self.raspberrySpawned = 1
        q=0
        self.playSurface.fill(blackColour)
        for position in self.snakeSegments:
            pygame.draw.rect(self.playSurface,whiteColour,Rect(position[0],position[1],20,20))
            pygame.draw.rect(self.playSurface,redColour,Rect(self.raspberryPosition[0], self.raspberryPosition[1],20,20))
        pygame.display.flip()
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())

        if self.snakePosition[0] > 280 or self.snakePosition[0] < 0:
            terminal=True
            self.__init__()
            
        if self.snakePosition[1] > 480 or self.snakePosition[1] < 0:
            terminal=True
            self.__init__()

        pygame.display.update()

        self.fpsClock.tick(30)
        return image_data,terminal


