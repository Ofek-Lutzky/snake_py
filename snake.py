import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox



class Cube(object):
    rows = 20
    w = 500
    def __init__(self, start, drinx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + dirny) #tuple that define the place you are

    def draw(self, surface, eyes= False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface,self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        if eyes:# if its True
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos): #my snake will be build from allot of parts of cubes
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0 # from the word direction
        self.dirny = 1 # if y is 1 x dirn need to be 0 (or upsite) because this is telling were our snake will go

    def move(self):
        for event in pygame.event.get(): # pygame have a list of commands call's events
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # will change the direction of the way we move according to turns dict
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body): #the loop catch the new position to move and doing the step step of the snake to the new move
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else: #check the border and move the snake according to them. if you stuck the edge you will start from the parallel edge
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny) # if we are not stck on border just move the same way


    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1



    def addcube(self): # add the cube to the tail according to the direction you are moving
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface): # not really understand diplly
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)




def drawGrid(w,rows,surface):
    sizeBtwn = w // rows #the distance between the rows on the grid
    x=0
    y=0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255,255,255), (x,0), (x,w)) #drawing lines from up to down
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def redrawWindow(surface):
    global rows, width , snake, food
    surface.fill((0,0,0))
    snake.draw(surface)
    food.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomsnack(rows, item):
    position = item.body
    while True:
        x = random.randrange(rows)
        y= random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), position))) > 0:
            continue
        else:
            break
    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass





def main():
    global width, rows , snake, food
    width = 500
    height = 500
    rows = 20
    win = pygame.display.set_mode((width,height)) # shows the display board
    snake = Snake((255,0,0), (10,10))
    food = Cube(randomsnack(rows, snake), color= (0,255,0))
    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50) #so the game wont be so fast (can play with this)
        clock.tick(10) # our frame wont move more then 10 frmes per second
        snake.move()
        if snake.body[0].pos == food.pos:
            snake.addcube()
            food = Cube(randomsnack(rows, snake), color= (0,255,0))

        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                print('Score: '+ f"{len(snake.body)}")
                message_box('You Lost!', 'Play again')
                snake.reset((10, 10))
                break

        redrawWindow(win)



main()
# auto-py-to-exe