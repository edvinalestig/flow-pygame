import pygame, sys, json
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
        
        self.level = levels.getLevel()
        self.loadLevel()

        


    def loadLevel(self):
        
        self.height = self.level["height"]
        self.width = self.level["width"]

        size = self.sideLength * (self.width+2), self.sideLength * (self.height+2)
        if self.dev: print("Screen size:", size)

        fillHeight, fillWidth = self.sideLength * self.height, self.sideLength * self.width

        self.screen = pygame.display.set_mode(size)
        

        # Draw board
        self.graphicsManager.drawBoard(self.sideLength, self.width, self.height)


        # Create the end points (static tiles)
        for value in self.level["colours"]:
            colour = value[0]
            index1 = value[1]
            index2 = value[2]
            self.graphicsManager.drawEndPoint(index1, colour)
            self.graphicsManager.drawEndPoint(index2, colour)
            self.statics.append([index1, colour])
            self.statics.append([index2, colour])

        # Extra stuff for developer mode
        if self.dev: 
            rect = pygame.Rect(0, 0, 100, 25)
            self.reloadButton = pygame.draw.rect(self.screen, (255,255,255), rect)

            print("Level loaded")
            print("Rectangles:", self.rectangles)
            print("Statics:", self.statics)
            print("Centre points:", self.centrePoints)
            print("Connections:", self.connections)
    

    def removeTile(self, tile):
        for array in self.statics:
            if array[0] == tile:
                return

        self.graphicsManager.removeTile(tile)


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
        
        self.graphicsManager.drawLine(tile1, tile2, colour)


    def reloadBoard(self):
        # When a new connection is added, reload the board to show new lines. 
        # When a connection is removed it becomes easier to remove the line.
        self.graphicsManager.drawBoard(self.sideLength, self.width, self.height)

        for value in self.level["colours"]:
            colour = value[0]
            tile1 = value[1]
            tile2 = value[2]
            self.graphicsManager.drawEndPoint(tile1, colour)
            self.graphicsManager.drawEndPoint(tile2, colour)

        for array in self.connections:
            self.graphicsManager.drawLine(array[0], array[1], array[2])
        


    def addConnection(self, tile1, tile2, colour):
        self.connections.append((tile1, tile2, colour))
        self.reloadBoard()
        print("Connections:", self.connections)



            
            
            
                    
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