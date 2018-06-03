import pygame, math

class GraphicsManager():
    def __init__(self, gameLogic):
        self.logic = gameLogic


    
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
        pygame.draw.circle(self.logic.screen, colour, centrePoint, math.floor(self.logic.sideLength/3))


    def removeTile(self, tile):
        pygame.draw.rect(self.logic.screen, (0, 0, 0), self.logic.rectangles[tile])
        pygame.draw.rect(self.logic.screen, (64, 64, 176), self.logic.rectangles[tile], 5)
        self.logic.filledTiles[tile] = False


    def drawLine(self, tile1, tile2, colour):
        tile1Centre = self.logic.centrePoints[tile1]
        tile2Centre = self.logic.centrePoints[tile2]
        
        width = math.floor(self.logic.sideLength/4 + 0.5)

        if width % 2 == 0:
            width += 1
        self.radius = math.floor(width/2)

        rect = pygame.draw.line(self.logic.screen, colour, tile1Centre, tile2Centre, width)
        self.logic.filledTiles[tile2] = True


    def drawSmoothTurn(self, point, colour):
        pygame.draw.circle(self.logic.screen, colour, point, self.radius)


    def drawWinScreen(self):
        screenWidth, screenHeight = self.logic.screen.get_size()
        middleX = math.floor(screenWidth/2 + 0.5)
        middleY = math.floor(screenHeight/2 + 0.5)

        width, height = 400, 250
        left = middleX - width/2
        top = middleY - height/2

        winRect = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.logic.screen, (0,0,0), winRect)
        pygame.draw.rect(self.logic.screen, (255, 255, 255), winRect, 5)

        font = pygame.font.SysFont("framd.ttf", 48)
        
        textSurface = font.render("Level Complete!", True, (255, 255, 255))
        size = font.size("Level Complete!")

        left = math.floor(middleX - size[0]/2 + 0.5)
        top = math.floor(middleY - size[1]/2 + 0.5)
        
        self.logic.screen.blit(textSurface, (left, top))

        