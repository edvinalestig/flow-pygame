import pygame, sys

pygame.init()

class Game():
    def __init__(self):
        self.sideLength = 75
        squares = 5

        size = self.sideLength * (squares+2), self.sideLength * (squares+2)
        fillHeight, fillWidth = self.sideLength * squares, self.sideLength * squares

        self.screen = pygame.display.set_mode(size)

        self.rectangles = []
        i = self.sideLength
        while i < fillWidth + self.sideLength:
            j = self.sideLength
            while j < fillHeight + self.sideLength:
                rectangle = pygame.Rect(i, j, self.sideLength, self.sideLength)
                drawnRectangle = pygame.draw.rect(self.screen, [i/2, j/2, 255], rectangle, 5)
                self.rectangles.append(drawnRectangle)

                j += self.sideLength
            i += self.sideLength

    def fillRect(self, pos, colour=[0, 255, 0]):
        pass


game = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

    
    pygame.display.flip()