import pygame, sys, json, math
import levels, mouseManager, graphicsManager


class Game():
    def __init__(self, dev=False):
        self.dev = dev
        
        with open("config.txt") as f:
            config = json.loads(f.read())

        if self.dev: print(config)
        self.sideLength = config["sideLength"]

        # Initialise classes
        pygame.init()
        self.mouseManager = mouseManager.MouseManager(self)
        self.graphicsManager = graphicsManager.GraphicsManager(self)

        # Game data
        self.centrePoints = []
        self.rectangles = []
        self.statics = []
        self.filledTiles = []
        self.connections = []
        
        level = levels.getLevel()
        self.loadLevel(level)

        


    def loadLevel(self, level):
        
        self.height = level["height"]
        self.width = level["width"]

        size = self.sideLength * (self.width+2), self.sideLength * (self.height+2)
        if self.dev: print("Screen size:", size)

        fillHeight, fillWidth = self.sideLength * self.height, self.sideLength * self.width

        self.screen = pygame.display.set_mode(size)
        

        # Draw board
        self.graphicsManager.drawBoard(self.sideLength, self.width, self.height)


        # Create the end points (static tiles)
        for value in level["colours"]:
            colour = value[0]
            index1 = value[1]
            index2 = value[2]
            self.graphicsManager.drawEndPoint(index1, colour)
            self.graphicsManager.drawEndPoint(index2, colour)

        if self.dev: 
            rect = pygame.Rect(0, 0, 100, 25)
            self.reloadButton = pygame.draw.rect(self.screen, (255,255,255), rect)

            print("Level loaded")
            print("Rectangles:", self.rectangles)
            print("Statics:", self.statics)
            print("Centre points:", self.centrePoints)
            print("Filled tiles:", self.filledTiles)
    

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
                    self.mouseManager.mousePressed = False
                    return
            if array[0] == tile1:
                if array[1] != colour:
                    self.mouseManager.mousePressed = False
                    return

        if self.filledTiles[tile2]:
            self.mouseManager.mousePressed = False
            return
        
        tile1Centre = self.centrePoints[tile1]
        tile2Centre = self.centrePoints[tile2]
        
        width = 10
        rect = pygame.draw.line(self.screen, colour, tile1Centre, tile2Centre, width)
        self.filledTiles[tile2] = True



            
            
            
                    
if __name__ == "__main__":              

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