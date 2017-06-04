# coding=UTF-8
#!/usr/bin/env python
import pygame,sys,time,random
from pygame.locals import *
import numpy as np
import win32api,win32con
import copy
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
redColour = pygame.Color(255,0,0)
blueColour= pygame.Color(0,0,255)
class game:
    def __init__(self,num,flag,tag):
        pygame.init()
        pygame.mixer.init()
        self.fpsClock = pygame.time.Clock()
        
        pygame.display.set_caption('人机大战')
        if flag==0:
            self.snakePosition_m = [140,240]
            self.snakeSegments_m = [[140,240]]
            a=random.randint(0,3)
            if a==0:
                self.direction_m = 'right'
            if a==1:
                self.direction_m = 'left'
            if a==2:
                self.direction_m = 'up'
            if a==3:
                self.direction_m = 'down'
            self.changeDirection_m = self.direction_m

            self.snakePosition = [140,240]
            self.snakeSegments = [[140,240]]
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
            

            x = random.randrange(0,15)
            y = random.randrange(0,25)
            self.raspberryPosition = [int(x*20),int(y*20)]
            self.raspberrySpawned = 1
            
            self.fps=5



        if num==1 and flag==1:
            self.snakePosition_m = [140,240]
            self.snakeSegments_m = [[140,240]]
            a=random.randint(0,3)
            if a==0:
                self.direction_m = 'right'
            if a==1:
                self.direction_m = 'left'
            if a==2:
                self.direction_m = 'up'
            if a==3:
                self.direction_m = 'down'
            self.changeDirection_m = self.direction_m
            
        elif num==0 and flag==1:
            self.snakePosition = [140,240]
            self.snakeSegments = [[140,240]]
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
            

        if tag==0:
            x = random.randrange(0,15)
            y = random.randrange(0,25)
            self.raspberryPosition = [int(x*20),int(y*20)]
            self.raspberrySpawned = 1
            self.playSurface = pygame.display.set_mode((300,500))




    def frame_step(self,input_actions):
        q=0
        acce=0
        terminal=False 

        pygame.mixer.Sound('audio/swoosh.wav').play()
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




        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 判断键盘事件
                if event.key == ord('1'):
                    self.fps=7
                    win32api.MessageBox(0,"简单模式","提示",win32con.MB_OK)
                if event.key == ord('2'):
                    self.fps=12
                    win32api.MessageBox(0,"中级模式","提示",win32con.MB_OK)
                if event.key == ord('3'):
                    self.fps=20
                    win32api.MessageBox(0,"高级模式","提示",win32con.MB_OK)
                if event.key == ord('4'):
                    self.fps=30
                    win32api.MessageBox(0,"终极模式","提示",win32con.MB_OK)
                if event.key == ord('5'):
                    self.fps=80
                    win32api.MessageBox(0,"闪电蛇","提示",win32con.MB_OK)
                if event.key == ord('z'):
                    acce=1
                if event.key == K_RIGHT or event.key == ord('d'):
                    self.changeDirection_m = 'right'
                if event.key == K_LEFT or event.key == ord('a'):
                    self.changeDirection_m = 'left'
                if event.key == K_UP or event.key == ord('w'):
                    self.changeDirection_m = 'up'
                if event.key == K_DOWN or event.key == ord('s'):
                    self.changeDirection_m = 'down'
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
            # 判断是否输入了反方向

        if len(self.snakeSegments_m)!=1:
            if self.changeDirection_m == 'right' and not self.direction_m == 'left':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'left' and not self.direction_m == 'right':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'up' and not self.direction_m == 'down':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'down' and not self.direction_m == 'up':
                self.direction_m = self.changeDirection_m
        else:
            if self.changeDirection_m == 'right':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'left':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'up':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'down':
                self.direction_m = self.changeDirection_m
        # 根据方向移动蛇头的坐标
        if self.direction_m == 'right':
            if acce==1:
                self.snakePosition_m[0] += 40
                for i in range(len(self.snakeSegments_m)):
                    self.snakeSegments_m[i][0]+=20
            else:
                self.snakePosition_m[0] += 20
        if self.direction_m == 'left':
            if acce==1:
                self.snakePosition_m[0] -= 40
                for i in range(len(self.snakeSegments_m)):
                    self.snakeSegments_m[i][0]-=20
            else:
                self.snakePosition_m[0] -= 20
            #self.snakePosition_m[0] -= 20
        if self.direction_m == 'up':
            if acce==1:
                self.snakePosition_m[1] -= 40
                for i in range(len(self.snakeSegments_m)):
                    self.snakeSegments_m[i][1]-=20
            else:
                self.snakePosition_m[1] -= 20
            #self.snakePosition_m[1] -= 20
        if self.direction_m == 'down':
            if acce==1:
                self.snakePosition_m[1] += 40
                for i in range(len(self.snakeSegments_m)):
                    self.snakeSegments_m[i][1]+=20
            else:
                self.snakePosition_m[1] += 20
            #self.snakePosition_m[1] += 20
            
        # 增加蛇的长度
        self.snakeSegments.insert(0,list(self.snakePosition))
        
        # 判断是否吃掉了树莓
        if self.snakePosition[0] == self.raspberryPosition[0] and self.snakePosition[1] == self.raspberryPosition[1]:
            self.raspberrySpawned = 0
            pygame.mixer.Sound('audio/point.wav').play()
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



         # 增加蛇的长度
        self.snakeSegments_m.insert(0,list(self.snakePosition_m))
        # 判断是否吃掉了树莓
        if self.snakePosition_m[0] == self.raspberryPosition[0] and self.snakePosition_m[1] == self.raspberryPosition[1]:
            self.raspberrySpawned = 0
            pygame.mixer.Sound('audio/point.wav').play()
        else:
            self.snakeSegments_m.pop()
        # 如果吃掉树莓，则重新生成树莓
        if self.raspberrySpawned == 0:
            while(True):
                x = random.randrange(0,15)
                y = random.randrange(0,25)
                self.raspberryPosition = [int(x*20),int(y*20)]
                for position in self.snakeSegments_m:
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
            pygame.mixer.Sound('audio/hit.wav').play()
            self.__init__(0,1,1)
            
        if self.snakePosition[1] > 480 or self.snakePosition[1] < 0:
            terminal=True
            pygame.mixer.Sound('audio/hit.wav').play()
            self.__init__(0,1,1)


       
        # 绘制pygame显示层
        self.playSurface.fill(blackColour)
        for position in self.snakeSegments:
            pygame.draw.rect(self.playSurface,whiteColour,Rect(position[0],position[1],20,20))
            pygame.draw.rect(self.playSurface,redColour,Rect(self.raspberryPosition[0], self.raspberryPosition[1],20,20))
        for position_m in self.snakeSegments_m:
            pygame.draw.rect(self.playSurface,blueColour,Rect(position_m[0],position_m[1],20,20))
            pygame.draw.rect(self.playSurface,redColour,Rect(self.raspberryPosition[0], self.raspberryPosition[1],20,20))

        # 刷新pygame显示层
        pygame.display.flip()
        # 判断是否死亡
        if self.snakePosition_m[0] > 280 or self.snakePosition_m[0] < 0:
            if terminal:
                self.__init__(1,1,0)
                pygame.mixer.Sound('audio/die.wav').play()
            else:
                self.__init__(1,1,1)
                pygame.mixer.Sound('audio/die.wav').play()
        if self.snakePosition_m[1] > 480 or self.snakePosition_m[1] < 0:
            if terminal:
                self.__init__(1,1,0)
                pygame.mixer.Sound('audio/die.wav').play()
            else:
                self.__init__(1,1,1)
                pygame.mixer.Sound('audio/die.wav').play()
        

        #pygame.display.update()

        self.fpsClock.tick(self.fps)
        return image_data,terminal


