import pygame

import numpy as np
import time
import random
pygame.init()
DispH = 720
DispW = 1280
fps = 30
setDisplay = pygame.display.set_mode((DispW, DispH))


class Block:
    def __init__(self, x, y, isAlive):
        self.box = pygame.Rect(x, y, 10, 10)
        self.alive = isAlive
        self.printblock()

    def printblock(self):
        global setDisplay
        if self.alive:
            pygame.draw.rect(setDisplay, WHITE, self.box)
        else:
            pygame.draw.rect(setDisplay, BLACK, self.box)

    def check(self, count):
        if count > 3 and self.alive:
            self.alive = False
            self.printblock()
        elif count == 3 and not self.alive:
            self.alive = True
            self.printblock()
        elif 1 < count < 4 and self.alive:
            self.alive = True
            self.printblock()
        elif count < 2 and self.alive:
            self.alive = False
            self.printblock()


#   R   G   B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

if __name__ == "__main__":
    setDisplay.fill(BLACK)
    fpsTime = pygame.time.Clock()
    pygame.display.set_caption("monopoly")
    x = 10
    y = 10
    maxx = int((DispW - 20) / 10)
    maxy = int((DispH - 20) / 10)
    boxesnp = np.empty([maxx, maxy], dtype=Block)
    for i in range(maxx):
        for j in range(maxy):
            boxesnp[i, j] = Block(i*10, j*10, False)
    pygame.display.update()
    fpsTime.tick(fps)
    n = int(input("enter the number of active boxes"))
    ch = int(input("do you wish to randomize? "))
    for i in range(n):
        if not ch:
            x1 = int(input("enter the x coordinate"))
            y1 = int(input("enter the y coordinate"))
        else:
            x1 = random.randint(0, maxx-1)
            y1 = random.randint(0, maxy-1)
        boxesnp[x1, y1].alive = True
        boxesnp[x1, y1].printblock()
    pygame.display.update()
    fpsTime.tick(fps)
    gencount = 0
    start = input("Start in 3 seconds? :")
    time.sleep(3)
    while True:
        print("Generation: "+str(gencount))
        gencount += 1
        surfacearray = np.remainder(pygame.surfarray.pixels_red(setDisplay), 2)
        for x in range(maxx):
            for y in range(maxy):
                i = x*10
                j = y*10
                try:
                    boxesnp[x, y].check(sum([surfacearray[i-5, j-5],
                                             surfacearray[i-5, j+5],
                                             surfacearray[i-5, j+15],
                                             surfacearray[i+5, j-5],
                                             surfacearray[i+5, j+15],
                                             surfacearray[i+15, j-5],
                                             surfacearray[i+15, j+5],
                                             surfacearray[i+15, j+15]]))
                except IndexError:
                    if i == 0:
                        if j == 0:
                            boxesnp[i, j].check(sum([surfacearray[i+15, j+5],
                                                    surfacearray[i+5, j+15],
                                                    surfacearray[i+15, j+15]]))
                        elif 0 < j < maxy-1:
                            boxesnp[i, j].check(sum([surfacearray[i+5, j-5],
                                                    surfacearray[i+15, j-5],
                                                    surfacearray[i+15, j+5],
                                                    surfacearray[i+5, j+15],
                                                    surfacearray[i+15, j+15]]))
                        elif j == maxy-1:
                            boxesnp[i, j].check(sum([surfacearray[i+5, j-5],
                                                    surfacearray[i+15, j-5],
                                                    surfacearray[i+15, j+5]]))
                    elif 0 < i < maxx-1:
                        if j == 0:
                            boxesnp[i, j].check(sum([surfacearray[i-5, j+5],
                                                    surfacearray[i+15, j+5],
                                                    surfacearray[i-5, j+15],
                                                    surfacearray[i+5, j+15],
                                                    surfacearray[i+15, j+15]]))

                        elif j == maxy-1:
                            boxesnp[i, j].check(sum([surfacearray[i-5, j-5],
                                                    surfacearray[i+5, j-5],
                                                    surfacearray[i+15, j-5],
                                                    surfacearray[i-5, j+5],
                                                    surfacearray[i+15, j+5]]))
                    elif i == maxx-1:
                        if j == 0:
                            boxesnp[i, j].check(sum([surfacearray[i-5, j+5],
                                                    surfacearray[i-5, j+15],
                                                    surfacearray[i+5, j+15]]))

                        elif 0 < j < maxy-1:
                            boxesnp[i, j].check(sum([surfacearray[i-5, j-5],
                                                    surfacearray[i+5, j-5],
                                                    surfacearray[i-5, j+5],
                                                    surfacearray[i-5, j+15],
                                                    surfacearray[i+5, j+15]]))
                        elif j == maxy-1:
                            boxesnp[i, j].check(sum([surfacearray[i-5, j-5],
                                                    surfacearray[i+5, j-5],
                                                    surfacearray[i-5, j+5]]))
        pygame.display.update()
        fpsTime.tick(fps)
