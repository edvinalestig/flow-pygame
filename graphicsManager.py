import pygame, math

class GraphicsManager():
    def __init__(self, gameLogic):
        self.logic = gameLogic
        self.level = gameLogic.level


    def drawBoard(self, level):
        length = level.length

        totalHeight = length * level.height
        totalWidth = length * level.width

        board = pygame.Rect(length, length, length+totalWidth, length+totalHeight)
        pygame.draw.rect(self.logic.screen, (0,0,0), board)

        borderColour = (64, 64, 176)
        
        for rectangle in level.rectangles:
            pygame.draw.rect(self.logic.screen, borderColour, rectangle, 5)


    def drawEndPoint(self, tile, colour):
        centrePoint = self.level.centrePoints[tile]
        pygame.draw.circle(self.logic.screen, colour, centrePoint, math.floor(self.level.length/3))


    def drawLine(self, tile1, tile2, colour):
        tile1Centre = self.level.centrePoints[tile1]
        tile2Centre = self.level.centrePoints[tile2]
        
        width = math.floor(self.level.length/4 + 0.5)

        if width % 2 == 0:
            width += 1
        self.radius = math.floor(width/2)

        rect = pygame.draw.line(self.logic.screen, colour, tile1Centre, tile2Centre, width)


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