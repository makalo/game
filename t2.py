# coding=UTF-8
#!/usr/bin/env python
import pygame,sys,time,random
from pygame.locals import *
import numpy as np
import copy
#定义颜色变量
#redColour = pygame.Color(255,255,255)
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
#greyColour = pygame.Color(150,150,150)

# 定义gameOver函数
class game:
    


    def __init__(self):
        
        # 初始化pygame
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        self.reward=0.1
         # 创建pygame显示层
        self.playSurface = pygame.display.set_mode((300,500))
        pygame.display.set_caption('Raspberry Snake')
        #print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")

        # 初始化变量
        self.snakePosition = [140,240]
        #temp2=self.snakePosition
        #self.temp=temp2
        self.temp=copy.copy(self.snakePosition)
        self.snakeSegments = [[140,240]]
        x = random.randrange(0,15)
        y = random.randrange(0,25)
        self.raspberryPosition = [int(x*20),int(y*20)]
        #for position in self.snakeSegments:
        #    pygame.draw.rect(self.playSurface,whiteColour,Rect(position[0],position[1],20,20))
        #    pygame.draw.rect(self.playSurface,redColour,Rect(self.raspberryPosition[0], self.raspberryPosition[1],20,20))
        #self.raspberryPosition = [100,30]
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
    
        

    def frame_step(self,input_actions,t):
    

    

    
        # 检测例如按键等pytegame事件
        #input_actions[0]=1  right
        #input_actions[1]=1  left
        #input_actions[2]=1  up
        #input_actions[3]=1  down
        # 判断是否输入了反方向
        #pygame.event.pump()

        flag=0
        terminal = False
        #temp=self.snakePosimtionte
        self.temp=copy.copy(self.snakePosition)

        #if t % 100==0:
        #    self.__init__()
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
        
        
        
        #print(self.temp)
        #print(self.snakePosition)
        #print(self.raspberryPosition)
        #print("kkkkkkkkk")
        #temp=np.zeros(2)
        # 增加蛇的长度
        self.snakeSegments.insert(0,list(self.snakePosition))
        # 判断是否吃掉了树莓
        if self.snakePosition[0] == self.raspberryPosition[0] and self.snakePosition[1] == self.raspberryPosition[1]:
            self.raspberrySpawned = 0
            self.reward+=10
        else:
            self.snakeSegments.pop()
        dis1=abs(self.snakePosition[0]-self.raspberryPosition[0])+abs(self.snakePosition[1]-self.raspberryPosition[1])
        dis2=abs(self.temp[0]-self.raspberryPosition[0])+abs(self.temp[1]-self.raspberryPosition[1])
        #print("dis1=%d"%dis1)
        #print("dis2=%d"%dis2)
        

        # 如果吃掉树莓，则重新生成树莓
        if self.raspberrySpawned == 0:
            x = random.randrange(0,15)
            y = random.randrange(0,25)
            self.raspberryPosition = [int(x*20),int(y*20)]
            self.raspberrySpawned = 1
        if dis2>dis1:
            self.reward+=1
            if dis1<=(dis2-10):
                self.reward+=1.5
            elif dis1<=(dis2-20):
                self.reward+=3
            elif dis1<=(dis2-40):
                self.reward+=4
            elif dis1<=(dis2-60):
                self.reward+=5
            
            #print(self.reward)
        elif dis2<dis1:
            self.reward-=1
            if dis2<=(dis1-10):
                self.reward-=1.5
            elif dis2<=(dis1-20):
                self.reward-=3
            elif dis2<=(dis1-40):
                self.reward-=4
            elif dis2<=(dis1-60):
                self.reward-=5
        #print("pppppppp")

        #temp1=self.snakePosition
        

        # 绘制pygame显示层
        self.playSurface.fill(blackColour)
        for position in self.snakeSegments:
            #pygame.draw.rect(self.playSurface,whiteColour,Rect(280,480,20,20))
            pygame.draw.rect(self.playSurface,whiteColour,Rect(position[0],position[1],20,20))
            pygame.draw.rect(self.playSurface,whiteColour,Rect(self.raspberryPosition[0], self.raspberryPosition[1],20,20))
            #pygame.draw.rect(self.playSurface,blackColour,Rect(0,0,300,500))
            


        # 刷新pygame显示层
        pygame.display.flip()
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        # 判断是否死亡
        if self.snakePosition[0] > 288 or self.snakePosition[0] < 0:
            terminal = True
            self.reward = -1
            reward1=copy.copy(self.reward)
            flag=1
            self.__init__()
            
        if self.snakePosition[1] > 512 or self.snakePosition[1] < 0:
            terminal = True
            self.reward = -1
            reward1=copy.copy(self.reward)
            flag=1
            self.__init__()

        for snakeBody in self.snakeSegments[1:]:
            if self.snakePosition[0] == snakeBody[0] and self.snakePosition[1] == snakeBody[1]:
                terminal = True
                self.reward = -1
                reward1=copy.copy(self.reward)
                flag=1
                self.__init__()

        
        

        pygame.display.update()
        #np.set_printoptions(threshold='nan')
        
        #print (image_data)

        #image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        if (flag==0):
            reward1=copy.copy(self.reward)
        else:
            flag=0
        
        

        # 控制游戏速度
        self.fpsClock.tick(100)
        return image_data, reward1, terminal


