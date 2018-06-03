import pygame, sys, json, copy, math
import levels, mouseManager, graphicsManager, winChecker


class Game():
    def __init__(self, dev=False):
        self.dev = dev

        # Game data
        self.level = levels.getRandomLevel()
        # self.level = levels.level1
        self.connections = []

        # Initialise classes
        pygame.init()
        self.mouseManager = mouseManager.MouseManager(self)
        self.graphicsManager = graphicsManager.GraphicsManager(self)

        # Load the level
        self.loadLevel(self.level)

        
    def loadLevel(self, level):
        screen = pygame.display
        screen.set_caption("Flow")
        self.screen = screen.set_mode(level.screenSize)

        # Reload the board with the new level
        self.reloadBoard()

        # Extra stuff for developer mode
        if self.dev: 
            rect = pygame.Rect(0, 0, 100, 25)
            self.reloadButton = pygame.draw.rect(self.screen, (255,255,255), rect)

            print("Level loaded")
            print("Rectangles:", self.level.rectangles)
            print("Statics:", self.level.statics)
            print("Centre points:", self.level.centrePoints)
            print("Connections:", self.connections)
    

    def removeTile(self, tile):
        for array in self.level.statics:
            if array[0] == tile:
                return

        newConnections = copy.copy(self.connections)

        for i, connection in enumerate(self.connections):
            if self.dev: print("0:", connection[0], "1:", connection[1])
            
            if connection[0] == tile:
                index = newConnections.index(connection)
                del newConnections[index]
                self.reloadBoard()

                if self.dev: print("Deleted", connection)
            if connection[1] == tile:
                index = newConnections.index(connection)
                del newConnections[index]
                self.reloadBoard()
                if self.dev: print("Deleted", connection)
        self.connections = newConnections
        self.reloadBoard()



    def reloadBoard(self):
        # When a new connection is added, reload the board to show new lines. 
        # When a connection is removed it becomes easier to remove the line.
        self.graphicsManager.drawBoard(self.level)

        for static in self.level.statics:
            tile, colour = static
            self.graphicsManager.drawEndPoint(tile, colour)

        for array in self.connections:
            self.graphicsManager.drawLine(array[0], array[1], array[2])

        self.smoothenTurns()
        if winChecker.checkWin(self.level.statics, self.level.rectangles, self.findConnections):
            self.graphicsManager.drawWinScreen()
        


    def addConnection(self, tile1, tile2, colour):
        connectionsFound = 0
        staticTile = False
        connectionsFound += self.findConnections(tile1)[0]
        connectionsFound += self.findConnections(tile2)[0]

        if connectionsFound > 1:
            falseConnection = True
        else:
            falseConnection = False
        
            for static in self.level.statics:
                
                if static[0] == tile1:

                    if connectionsFound > 0:
                        falseConnection = True
                    else:
                        if static[1] != colour:
                            falseConnection = True

                if static[0] == tile1 or static[0] == tile2:
                    if static[1] != colour:
                            falseConnection = True



        if self.dev: print("Connections found:", connectionsFound)

        if not falseConnection:
            self.connections.append((tile1, tile2, colour))
            self.reloadBoard()
            if self.dev: print("Connections:", self.connections)
        else:
            self.mouseManager.mousePressed = False


    def smoothenTurns(self):
        for connection in self.connections:
            centrePoint1 = self.level.centrePoints[connection[0]]
            centrePoint2 = self.level.centrePoints[connection[1]]
            self.graphicsManager.drawSmoothTurn(centrePoint1, connection[2])
            self.graphicsManager.drawSmoothTurn(centrePoint2, connection[2])
        # Not very efficient but it works.


    def replaceConnection(self, tile, colour):
        self.removeTile(tile)
        self.addConnection(self.lastSelectedTile, tile, colour)


    def mousePressed(self):
        pos = pygame.mouse.get_pos()

        if self.dev:
            if self.reloadButton.collidepoint(pos):
                print("\nReloading game\n")
                # pygame.quit()
                self.__init__(True)
                return
        
        for i, value in enumerate(self.level.rectangles):
            if value.collidepoint(pos):
                self.lastSelectedTile = i

                for array in self.level.statics:
                    if array[0] == i:
                        self.mouseManager.mousePressed = True
                        if self.dev: print("Mouse pressed on a static tile")
                        
                        self.selectedColour = array[1]
                        if self.dev: print("Selected colour:", self.selectedColour)

                        self.changedTiles = []

                        return

                connectionsFound = self.findConnections(i)
                if connectionsFound[0] == 1:
                    self.mouseManager.mousePressed = True
                    if self.dev: print("Mouse pressed on a coloured tile")
                    
                    index = connectionsFound[1][0]
                    self.selectedColour = self.connections[index][2]
                    if self.dev: print("Selected colour:", self.selectedColour)

                    self.changedTiles = []
                    return
                elif connectionsFound[0] == 2:
                    if self.dev: print("Connections:", connectionsFound[0])
                    self.removeTile(i)


    def mouseMoved(self):
        pos = pygame.mouse.get_pos()

        for i, rect in enumerate(self.level.rectangles):
            if rect.collidepoint(pos):
                if i != self.lastSelectedTile:
                    neighbourTile = False

                    if i == self.lastSelectedTile + 1:
                        neighbourTile = True
                    elif i == self.lastSelectedTile - 1:
                        neighbourTile = True
                    elif i == self.lastSelectedTile + self.level.width:
                        neighbourTile = True
                    elif i == self.lastSelectedTile - self.level.width:
                        neighbourTile = True

                    if neighbourTile:
                        try:
                            self.changedTiles.index(i)

                            return

                        except ValueError:
                            self.changedTiles.append(i)

                        connectionsFound = self.findConnections(i)
                        if self.dev: print(f"Connections found: {connectionsFound[0]}")
                        if connectionsFound[0] > 0:

                            connectionIndex = connectionsFound[1][0]
                            if self.dev: print(f"Index: {connectionIndex}")

                            colour = self.connections[connectionIndex][2]
                            if colour != self.selectedColour:
                                if self.dev: print("Replacing connection...")
                                self.replaceConnection(i, self.selectedColour)
                                self.lastSelectedTile = i

                        else:
                            if self.dev: print("Tile changed:", i)

                            self.addConnection(self.lastSelectedTile, i, self.selectedColour)
                            self.lastSelectedTile = i
                    
                    return


    def findConnections(self, tile):
        connectionsFound = 0
        connectionIndex = []
        for index, connection in enumerate(self.connections):
            if connection[0] == tile or connection[1] == tile:
                connectionsFound += 1
                connectionIndex.append(index)
        return connectionsFound, connectionIndex

            
            
                    
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