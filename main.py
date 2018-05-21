import pygame, sys, json, math
import levels


class Game():
    def __init__(self, dev=False):
        self.dev = dev
        
        pygame.init()

        with open("config.txt") as f:
            config = json.loads(f.read())

        if self.dev: print(config)
        self.sideLength = config["sideLength"]
        
        self.centrePoints = []
        self.rectangles = []
        self.statics = []
        self.filledTiles = []
        self.mousePressed = False
        
        level = levels.getLevel()
        self.loadLevel(level)


    def loadLevel(self, level):
        
        height = level["height"]
        width = level["width"]

        size = self.sideLength * (width+2), self.sideLength * (height+2)
        if self.dev: print("Screen size:", size)

        fillHeight, fillWidth = self.sideLength * height, self.sideLength * width

        self.screen = pygame.display.set_mode(size)
        

        i = self.sideLength
        while i < fillWidth + self.sideLength:

            j = self.sideLength
            while j < fillHeight + self.sideLength:

                rectangle = pygame.Rect(i, j, self.sideLength, self.sideLength)
                pygame.draw.rect(self.screen, [i/4, j/4, 255], rectangle, 5)
                self.rectangles.append(rectangle)

                centrePoint = (math.floor(i + self.sideLength/2), math.floor(j + self.sideLength/2))
                self.centrePoints.append(centrePoint)
                self.filledTiles.append(False)

                j += self.sideLength
            i += self.sideLength

        for value in level["colours"]:
            colour = value[0]
            index1 = value[1]
            index2 = value[2]
            self.createStaticTile(index1, colour)
            self.createStaticTile(index2, colour)

        if self.dev: 
            print("Level loaded")
            print("Rectangles:", self.rectangles)
            print("Statics:", self.statics)
            print("Centre points:", self.centrePoints)


    def createStaticTile(self, index, colour):
        self.statics.append([index, colour])
        centrePoint = self.centrePoints[index]
        pygame.draw.circle(self.screen, colour, centrePoint, math.floor(self.sideLength/3))


    def fillTile(self, pos=None, colour=[0, 255, 0], index=None): # Byt funktionsnamn
        if pos:
            for i, value in enumerate(self.rectangles):
                if value.collidepoint(pos):
                    for array in self.statics:
                        if array[0] == i:
                            return

                    if not self.filledTiles[i]:
                        pygame.draw.rect(self.screen, colour, value)
                        self.filledTiles[i] = True
                    else:
                        pygame.draw.rect(self.screen, (0, 0, 0), value)
                        pygame.draw.rect(self.screen, (15, 15, 200), value, 8)
                        self.filledTiles[i] = False
        else:
            for array in self.statics:
                if array[0] == index:
                    return

            if not self.filledTiles[index]:
                pygame.draw.rect(self.screen, colour, self.rectangles[index])
                self.filledTiles[index] = True
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), self.rectangles[index])
                pygame.draw.rect(self.screen, (15, 15, 200), self.rectangles[index], 8)
                self.filledTiles[index] = False


    def mouseTrack(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()
            for i, value in enumerate(self.rectangles):
                if value.collidepoint(pos):
                    for array in self.statics:
                        if array[0] == i:
                            self.mousePressed = True
                            if self.dev: print("Mouse pressed at a static tile")
                            
                            self.selectedColour = array[1]
                            if self.dev: print("Selected colour:", self.selectedColour)

                            self.changedTiles = []

                            return
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mousePressed = False
            
            
        elif self.mousePressed:
            pos = pygame.mouse.get_pos()
            if self.dev: print(pos)

            for i, rect in enumerate(self.rectangles):
                if rect.collidepoint(pos):
                    try:
                        self.changedTiles.index(i)
                        # if self.dev: print("Tile already changed")
                        return
                    except ValueError:
                        pass
                    self.changedTiles.append(i)
                    if self.dev: print("Tile changed")

                    self.fillTile(colour=self.selectedColour, index=i)



            
            
            
                    
                    

try:
    if sys.argv[1] == "-d": 
        game = Game(True)
    else:
        game = Game()
except IndexError:
    game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            if game.dev: print("Exiting..")
            sys.exit()
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     pos = pygame.mouse.get_pos()
        #     game.fillTile(pos)
        #     if game.dev: print("Click at", pos)

        game.mouseTrack(event)

    
    pygame.display.flip()