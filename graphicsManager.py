import pygame, math

class GraphicsManager():
    def __init__(self, gameLogic):
        self.logic = gameLogic
        self.level = gameLogic.level


    def drawBoard(self, level):
        """Draws a blank board."""
        
        length = level.length

        totalHeight = length * level.height
        totalWidth = length * level.width

        # Make the background with the correct dimensions.
        board = pygame.Rect(length, length, length+totalWidth, length+totalHeight)
        pygame.draw.rect(self.logic.screen, (0,0,0), board)

        borderColour = (64, 64, 176)
        
        # Draw the borders of the tiles.
        for rectangle in level.rectangles:
            pygame.draw.rect(self.logic.screen, borderColour, rectangle, 5)


    def drawEndPoint(self, tile, colour):
        """Draws a circle which functions as an end point. (static tile)"""

        centrePoint = self.level.centrePoints[tile]
        pygame.draw.circle(self.logic.screen, colour, centrePoint, math.floor(self.level.length/3))


    def drawLine(self, tile1, tile2, colour):
        """Draws a line between two tiles."""

        tile1Centre = self.level.centrePoints[tile1]
        tile2Centre = self.level.centrePoints[tile2]
        
        width = math.floor(self.level.length/4 + 0.5)

        # Make sure the width looks good with the end circles.
        if width % 2 == 0:
            width += 1
        self.radius = math.floor(width/2)

        rect = pygame.draw.line(self.logic.screen, colour, tile1Centre, tile2Centre, width)


    def drawSmoothTurn(self, point, colour):
        """Draws a small circle the same size as a line in a tile."""

        pygame.draw.circle(self.logic.screen, colour, point, self.radius)


    def drawWinScreen(self):
        """Draws the win screen."""

        # Get the middle coords of the screen.
        screenWidth, screenHeight = self.logic.screen.get_size()
        middleX = math.floor(screenWidth/2 + 0.5)
        middleY = math.floor(screenHeight/2 + 0.5)

        # Dimensions of the box and define the upper left corner.
        width, height = 400, 250
        left = middleX - width/2
        top = middleY - height/2

        # Draw the box in the middle of the screen with a white border.
        winRect = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.logic.screen, (0,0,0), winRect)
        pygame.draw.rect(self.logic.screen, (255, 255, 255), winRect, 5)

        # Add text saying "Level complete!".
        font = pygame.font.SysFont("framd.ttf", 48)
        textSurface = font.render("Level Complete!", True, (255, 255, 255))
        size = font.size("Level Complete!")

        # Define the upper left corner of the text and print it.
        left = math.floor(middleX - size[0]/2 + 0.5)
        top = math.floor(middleY - size[1]/2 + 0.5)
        
        self.logic.screen.blit(textSurface, (left, top))


    def drawColouredBox(self, colour, width, height, corner):
        if corner == "centred":
            screenWidth, screenHeight = self.logic.screen.get_size()
            middleX = math.floor(screenWidth/2 + 0.5)
            middleY = math.floor(screenHeight/2 + 0.5)

            # Define the upper left corner.
            left = middleX - width/2
            top = middleY - height/2
            corner = (left, top)

        rect = pygame.Rect(corner[0], corner[1], width, height)
        pygame.draw.rect(self.logic.screen, colour, rect)

        return rect

    
    def drawTextBox(self, text, fontSize, corner):
        # Add the text.
        font = pygame.font.SysFont("framd.ttf", fontSize)
        textSurface = font.render(text, True, (255, 255, 255))
        size = font.size(text)      

        if corner == "centred":
            # Get the middle coords of the screen.
            screenWidth, screenHeight = self.logic.screen.get_size()
            middleX = math.floor(screenWidth/2 + 0.5)
            middleY = math.floor(screenHeight/2 + 0.5)

            # Define the upper left corner.
            left = math.floor(middleX - size[0]/2 + 0.5)
            top = math.floor(middleY - size[1]/2 + 0.5)

            corner = (left, top)
        
        self.logic.screen.blit(textSurface, corner)

        rect = pygame.Rect(corner, size)
        return rect