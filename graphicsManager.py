import pygame, math

class GraphicsManager():
    def __init__(self, logicClass):
        self.logic = logicClass
        self.length = logicClass.sideLength

    
    def drawBoard(self, length, width, height):        
        totalHeight = length * height
        totalWidth = length * width

        board = pygame.Rect(length, length, length+totalWidth, length+totalHeight)
        pygame.draw.rect(self.logic.screen, (0,0,0), board)

        borderColour = (64, 64, 176)
        
        y = length
        while y < totalHeight + length:

            x = length
            while x < totalWidth + length:

                # Rect(left, top, width, height) -> Rect
                rectangle = pygame.Rect(x, y, length, length)
                pygame.draw.rect(self.logic.screen, borderColour, rectangle, 5)
                self.logic.rectangles.append(rectangle)

                centrePoint = (math.floor(x + length/2), math.floor(y + length/2))
                self.logic.centrePoints.append(centrePoint)
                self.logic.filledTiles.append(False)

                x += length
            y += length


    def drawEndPoint(self, tile, colour):
        centrePoint = self.logic.centrePoints[tile]
        pygame.draw.circle(self.logic.screen, colour, centrePoint, math.floor(self.length/3))


    def removeTile(self, tile):
        pygame.draw.rect(self.logic.screen, (0, 0, 0), self.logic.rectangles[tile])
        pygame.draw.rect(self.logic.screen, (64, 64, 176), self.logic.rectangles[tile], 5)
        self.logic.filledTiles[tile] = False


    def drawLine(self, tile1, tile2, colour):
        tile1Centre = self.logic.centrePoints[tile1]
        tile2Centre = self.logic.centrePoints[tile2]
        
        width = self.length/4
        width = math.floor(width)
        rect = pygame.draw.line(self.logic.screen, colour, tile1Centre, tile2Centre, width)
        self.logic.filledTiles[tile2] = True