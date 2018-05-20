import pygame, sys
import levels


class Game():
    def __init__(self):
        pygame.init()

        
        
        self.sideLength = 75
        squares = 5

        size = self.sideLength * (squares+2), self.sideLength * (squares+2)
        fillHeight, fillWidth = self.sideLength * squares, self.sideLength * squares

        self.screen = pygame.display.set_mode(size)

        self.rectangles = []
        self.statics = []

        i = self.sideLength
        while i < fillWidth + self.sideLength:

            j = self.sideLength
            while j < fillHeight + self.sideLength:

                rectangle = pygame.Rect(i, j, self.sideLength, self.sideLength)
                pygame.draw.rect(self.screen, [i/2, j/2, 255], rectangle, 5)
                self.rectangles.append(rectangle)

                j += self.sideLength
            i += self.sideLength


    def createLevel(self, level):
        pass


    def createStaticSquare(self, index, colour):
        self.statics.append(index)
        rectangle = self.rectangles[index]
        pygame.draw.rect(self.screen, colour, rectangle)


    def fillRect(self, pos, colour=[0, 255, 0]): # Byt funktionsnamn
        for i in self.rectangles:
            if i.collidepoint(pos):
                pygame.draw.rect(self.screen, colour, i)


game = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            game.fillRect(pos)

    
    pygame.display.flip()