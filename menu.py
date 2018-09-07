import pygame, sys, math

class Menu():
    def __init__(self):
        pygame.init()   
        self.drawMainMenu()


    def drawMainMenu(self):
        self.screenSize = (500, 700)

        screen = pygame.display
        screen.set_caption("Main Menu")
        self.screen = screen.set_mode(self.screenSize)

        # Print the title
        font = pygame.font.SysFont("framd.ttf", 72)
        textSurface = font.render("Flow!", True, (255,255,255))
        size = font.size("Flow!")

        x =  math.floor(self.screenSize[0]/2 - size[0]/2 + 0.5)
        y = math.floor(self.screenSize[1]/15)

        self.screen.blit(textSurface, (x, y))
        # End of print title

        # Draw buttons
        self.createMainMenuButton("Levels", 125)
        self.createMainMenuButton("Level Editor", 200)



    def createMainMenuButton(self, text, ypos):
        boxSize = (math.floor(self.screenSize[0]*0.75), math.floor(self.screenSize[1]/12))
        boxX = math.floor((self.screenSize[0] - boxSize[0]) / 2)
        levelBox = pygame.Rect((boxX, ypos), boxSize)
        pygame.draw.rect(self.screen, (0,0,0), levelBox)
        pygame.draw.rect(self.screen, (255, 255, 255), levelBox, 5)

        font = pygame.font.SysFont("framd.ttf", 36)
        textSurface = font.render(text, True, (255, 255, 255))
        size = font.size(text)

        x =  math.floor(self.screenSize[0]/2 - size[0]/2 + 0.5)
        y = ypos + math.floor((boxSize[1]/2 + 0.5) - size[1]/2)
        self.screen.blit(textSurface, (x,y))

        return levelBox
        


class EventManager():
    def __init__(self):
        pass

    def processEvent(self, event):
        pass



menu = Menu()
eventman = EventManager()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            print("Exiting..")
            sys.exit()

        # Send event to the event manager.
        eventman.processEvent(event)

    # Update the screen.
    pygame.display.flip()