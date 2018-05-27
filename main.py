import pygame, sys, json, math
import levels, mouseManager


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
        
        level = levels.getLevel()
        self.loadLevel(level)

        self.mouseManager = mouseManager.MouseManager(self)


    def loadLevel(self, level):
        
        self.height = level["height"]
        self.width = level["width"]

        size = self.sideLength * (self.width+2), self.sideLength * (self.height+2)
        if self.dev: print("Screen size:", size)

        fillHeight, fillWidth = self.sideLength * self.height, self.sideLength * self.width

        self.screen = pygame.display.set_mode(size)
        

        # Create tiles
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

        # Create the end points (static tiles)
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


    def fillTile(self, colour=[0, 255, 0], index=None): # Byt funktionsnamn
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
    

    def removeTile(self, index):
        for array in self.statics:
            if array[0] == index:
                return
        
        pygame.draw.rect(self.screen, (0, 0, 0), self.rectangles[index])

        red = math.floor(((index / self.height) * self.sideLength)/4)
        if self.dev: print("Red:", red)
        green = math.floor(((index / self.width) * self.sideLength)/4)
        if self.dev: print("Green:", green)
        colour = (red, green, 255)
        pygame.draw.rect(self.screen, colour, self.rectangles[index], 5)
        self.filledTiles[index] = False


    def drawLine(self, tile1, tile2, colour):
        for array in self.statics:
            if array[0] == tile2:
                if array[1] != colour:
                    return
        if self.filledTiles[tile2]:
            return
        
        tile1Centre = self.centrePoints[tile1]
        tile2Centre = self.centrePoints[tile2]
        
        width = 10
        rect = pygame.draw.line(self.screen, colour, tile1Centre, tile2Centre, width)
        self.filledTiles[tile2] = True



            
            
            
                    
                    

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

        game.mouseManager.mouseTrack(event)

    
    pygame.display.flip()