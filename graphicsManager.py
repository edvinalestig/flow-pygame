import pygame, math

class GraphicsManager():
    def __init__(self, logicClass):
        self.logic = logicClass
        self.length = logicClass.sideLength
        # self.screen = logicClass.screen

    
    def drawBoard(self, length, width, height):
        totalHeight = length * height
        totalWidth = length * width
        
        y = length
        while y < totalHeight + length:

            x = length
            while x < totalWidth + length:

                # Rect(left, top, width, height) -> Rect
                rectangle = pygame.Rect(x, y, length, length)
                pygame.draw.rect(self.logic.screen, [x/4, y/4, 255], rectangle, 5)
                self.logic.rectangles.append(rectangle)

                centrePoint = (math.floor(x + length/2), math.floor(y + length/2))
                self.logic.centrePoints.append(centrePoint)
                self.logic.filledTiles.append(False)

                x += length
            y += length

    def drawEndPoint(self, tile, colour):
        self.logic.statics.append([tile, colour])
        centrePoint = self.logic.centrePoints[tile]
        pygame.draw.circle(self.logic.screen, colour, centrePoint, math.floor(self.length/3))