import pygame, sys, math, json

class Menu():
    def __init__(self, main):
        self.main = main
        pygame.init()   
        self.screenSize = (500, 700)
        screen = pygame.display
        self.caption = screen
        self.screen = screen.set_mode(self.screenSize)

        self.menu = "main"

        # self.drawMainMenu()
        rectangles = self.drawLevelsMenu()
        self.eventman = EventManager(rectangles)
        self.mainLoop()

    
    def mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    print("Exiting..")
                    sys.exit()

                # Send event to the event manager.
                self.eventman.processEvent(event, self.menu)

            # Update the screen.
            pygame.display.flip()


    def drawMainMenu(self):
        self.menu = "menu"
        self.caption.set_caption("Main Menu")
        self.rectangles = []
        
        # Print the header
        font = pygame.font.SysFont("framd.ttf", 72)
        textSurface = font.render("Flow!", True, (255,255,255))
        size = font.size("Flow!")

        x =  math.floor(self.screenSize[0]/2 - size[0]/2 + 0.5)
        y = math.floor(self.screenSize[1]/15)

        self.screen.blit(textSurface, (x, y))
        # End of print header

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


    def drawLevelsMenu(self):
        self.menu = "levels"
        self.caption.set_caption("Levels")
        self.rectangles = []

        # Print the header
        font = pygame.font.SysFont("framd.ttf", 72)
        textSurface = font.render("Levels", True, (255,255,255))
        size = font.size("Levels")

        x =  math.floor(self.screenSize[0]/2 - size[0]/2 + 0.5)
        y = math.floor(self.screenSize[1]/15)

        self.screen.blit(textSurface, (x, y))


        with open("levels.json") as f:
            levels = json.loads(f.read())

        rects = []

        for i in range(len(levels)):
            rects.append(self.createLevelButton(i))

        rects.append(self.createMainMenuButton("Go back", self.screenSize[1]*0.85))

        return rects


    def createLevelButton(self, number):
        sideLength = math.floor(self.screenSize[0]/7)
        buttonLength = sideLength*0.8

        boxSize = (buttonLength, buttonLength)

        boxX = math.floor(sideLength*1.1 + (((number)%5)) * sideLength)
        boxY = math.floor(sideLength*1.1 + (((number)//5)+1) * sideLength)


        levelBox = pygame.Rect((boxX, boxY), boxSize)
        pygame.draw.rect(self.screen, (0,0,0), levelBox)
        pygame.draw.rect(self.screen, (255, 255, 255), levelBox, 5)

        text = str(number+1)
        font = pygame.font.SysFont("framd.ttf", 36)
        textSurface = font.render(text, True, (255, 255, 255))
        size = font.size(text)

        # x =  math.floor(self.screenSize[0]/2 - size[0]/2 + 0.5)
        x = boxX + math.floor((boxSize[0]/2 + 0.5) - size[0]/2)
        y = boxY + math.floor((boxSize[1]/2 + 0.5) - size[1]/2)
        self.screen.blit(textSurface, (x,y))

        return levelBox


class EventManager():
    def __init__(self, rectangles):
        self.rectangles = rectangles

    def processEvent(self, event, menu):
        if event == pygame.MOUSEBUTTONDOWN:
            if menu == "levels":
                pass
            elif menu == "main":
                pass


if __name__ == "__main__":
    menu = Menu()
    