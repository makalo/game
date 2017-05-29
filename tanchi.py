# coding=UTF-8
#!/usr/bin/env python
import pygame,sys,time,random
from pygame.locals import *
# 定义颜色变量
redColour = pygame.Color(255,0,0)
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
greyColour = pygame.Color(150,150,150)

# 定义gameOver函数


# 定义main函数
class main():
    # 初始化pygame
    def __init__(self):
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        # 创建pygame显示层
        self.playSurface = pygame.display.set_mode((300,500))
        pygame.display.set_caption('Raspberry Snake')

        # 初始化变量
        self.snakePosition = [140,240]
        self.snakeSegments = [[140,240]]
        #self.raspberryPosition = [300,300]
        x = random.randrange(0,15)
        y = random.randrange(0,25)
        self.raspberryPosition = [int(x*20),int(y*20)]
        self.raspberrySpawned = 1
        #self.direction = 'right'
        a=random.randint(0,3)
        if a==0:
            self.direction = 'right'
        if a==1:
            self.direction = 'left'
        if a==2:
            self.direction = 'up'
        if a==3:
            self.direction = 'down'
        self.chagedirection = self.direction
        q=0
    def game(self):
        while True:
            # 检测例如按键等pygame事件
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    # 判断键盘事件
                    if event.key == K_RIGHT or event.key == ord('d'):
                        self.chagedirection = 'right'
                    if event.key == K_LEFT or event.key == ord('a'):
                        self.chagedirection = 'left'
                    if event.key == K_UP or event.key == ord('w'):
                        self.chagedirection = 'up'
                    if event.key == K_DOWN or event.key == ord('s'):
                        self.chagedirection = 'down'
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
            # 判断是否输入了反方向

            if len(self.snakeSegments)!=1:
                if self.chagedirection == 'right' and not self.direction == 'left':
                    self.direction = self.chagedirection
                if self.chagedirection == 'left' and not self.direction == 'right':
                    self.direction = self.chagedirection
                if self.chagedirection == 'up' and not self.direction == 'down':
                    self.direction = self.chagedirection
                if self.chagedirection == 'down' and not self.direction == 'up':
                    self.direction = self.chagedirection
            else:
                if self.chagedirection == 'right':
                    self.direction = self.chagedirection
                if self.chagedirection == 'left':
                    self.direction = self.chagedirection
                if self.chagedirection == 'up':
                    self.direction = self.chagedirection
                if self.chagedirection == 'down':
                    self.direction = self.chagedirection
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
            # 绘制pygame显示层
            self.playSurface.fill(blackColour)
            for position in self.snakeSegments:
                pygame.draw.rect(self.playSurface,whiteColour,Rect(position[0],position[1],20,20))
                pygame.draw.rect(self.playSurface,redColour,Rect(self.raspberryPosition[0], self.raspberryPosition[1],20,20))

            # 刷新pygame显示层
            pygame.display.flip()
            # 判断是否死亡
            if self.snakePosition[0] > 280 or self.snakePosition[0] < 0:
                self.__init__()
            if self.snakePosition[1] > 480 or self.snakePosition[1] < 0:
                self.__init__()
            for snakeBody in self.snakeSegments[1:]:
                if self.snakePosition[0] == snakeBody[0] and self.snakePosition[1] == snakeBody[1]:
                    self.__init__()
            # 控制游戏速度
            self.fpsClock.tick(10)

if __name__ == "__main__":
    t=main()
    a=t.game()