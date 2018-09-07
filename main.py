import pygame, sys, json, copy, math
import levels, mouseManager, graphicsManager, winChecker, menu


class Game():
    def __init__(self, alts):
        self.dev = False
        self.testingMode = False
        
        # Start alternatives
        for alt in alts:
            if alt == "-d":
                self.dev = True
            if alt == "-t":
                self.testingMode = True


        # Game data
        if self.testingMode:
            self.level = levels.getTestLevel()
        else:
            self.level = levels.getRandomLevel()
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
                # Don't do anything if the tile is static.
                return

        # Make a copy of the connections.
        newConnections = copy.copy(self.connections)

        # Find all connections within the tile.
        # Loop over the old list and remove from the new.
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
        
        # Replace the connections list
        self.connections = newConnections
        self.reloadBoard()



    def reloadBoard(self):
        # Reload the board with all connections and statics etc.
        self.graphicsManager.drawBoard(self.level)

        # Draw the statics
        for static in self.level.statics:
            tile, colour = static
            self.graphicsManager.drawEndPoint(tile, colour)

        # Draw the connections
        for array in self.connections:
            self.graphicsManager.drawLine(array[0], array[1], array[2])

        # Draw the ends of the lines
        self.smoothenTurns()

        # Check if the player has won
        if winChecker.checkWin(self.level.statics, self.level.rectangles, self.findConnections):
            self.graphicsManager.drawWinScreen()
        


    def addConnection(self, tile1, tile2, colour):
        """Adds a connections between two tiles with a colour."""

        # Info about the two tiles
        connectionsFound = 0
        staticTile = False
        connectionsFound += self.findConnections(tile1)[0]
        connectionsFound += self.findConnections(tile2)[0]

        if connectionsFound > 1:
            # Tile already has too many connections and can't handle another one.
            falseConnection = True
        else:
            falseConnection = False
        
            for static in self.level.statics:
                
                if static[0] == tile1:

                    if connectionsFound > 0:
                        # The static tile can't handle more connections and has reached the limit.
                        falseConnection = True
                    else:
                        if static[1] != colour:
                            # The static tile is not the same colour.
                            falseConnection = True

                if static[0] == tile1 or static[0] == tile2:
                    if static[1] != colour:
                        # The static tile is not the same colour.
                        falseConnection = True



        if self.dev: print("Connections found:", connectionsFound)

        # Add a connection if it's a valid move.
        if not falseConnection:
            self.connections.append((tile1, tile2, colour))
            self.reloadBoard()
            if self.dev: print("Connections:", self.connections)
        else:
            # Release the mouse to prevent making connections beyond faulty connections.
            self.mouseManager.mousePressed = False


    def smoothenTurns(self):
        # Go through all connections and add a small circle to each end.
        for connection in self.connections:
            centrePoint1 = self.level.centrePoints[connection[0]]
            centrePoint2 = self.level.centrePoints[connection[1]]
            self.graphicsManager.drawSmoothTurn(centrePoint1, connection[2])
            self.graphicsManager.drawSmoothTurn(centrePoint2, connection[2])
        # Not very efficient but it works.


    def replaceConnection(self, tile, colour):
        """Replaces an old connection with a new one."""
        self.removeTile(tile)
        self.addConnection(self.lastSelectedTile, tile, colour)


    def mousePressed(self):
        # Called when the mouse button has been pressed.
        pos = pygame.mouse.get_pos()

        if self.dev:
            if self.reloadButton.collidepoint(pos):
                print("\nReloading game\n")
                # pygame.quit()
                self.__init__(sys.argv)
                return
        
        # Go through all tiles and find which one has been pressed.
        for i, value in enumerate(self.level.rectangles):
            if value.collidepoint(pos):
                # The tile pressed is i.
                self.lastSelectedTile = i

                # Check if the tile is static.
                for array in self.level.statics:
                    if array[0] == i:
                        self.mouseManager.mousePressed = True
                        if self.dev: print("Mouse pressed on a static tile")
                        
                        self.selectedColour = array[1]
                        if self.dev: print("Selected colour:", self.selectedColour)

                        # Information stored about colour and selected tile. Ready for mouse movement.

                        return

                # Check if mouse pressed a line stump which can be continued.
                connectionsFound = self.findConnections(i)
                if connectionsFound[0] == 1:
                    self.mouseManager.mousePressed = True
                    if self.dev: print("Mouse pressed on a coloured tile")
                    
                    index = connectionsFound[1][0]
                    self.selectedColour = self.connections[index][2]
                    if self.dev: print("Selected colour:", self.selectedColour)

                    # Information stored about colour and selected tile. Ready for mouse movement.

                    return
                elif connectionsFound[0] == 2:
                    # Tile has 2 connections and they will therefore be removed.
                    if self.dev: print("Connections:", connectionsFound[0])
                    self.removeTile(i)


    def mouseMoved(self):
        pos = pygame.mouse.get_pos()

        # Check which tile was pressed
        for i, rect in enumerate(self.level.rectangles):
            if rect.collidepoint(pos):
                # If the mouse has moved to a different tile.
                if i != self.lastSelectedTile:
                    
                    # Check if the new tile is right next to the old.
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
                        connectionsFound = self.findConnections(i)
                        if self.dev: print(f"Connections found: {connectionsFound[0]}")
                        
                        # If the tile already has connections, replace or remove them.
                        if connectionsFound[0] > 0:

                            connectionIndex = connectionsFound[1][0]
                            if self.dev: print(f"Index: {connectionIndex}")

                            colour = self.connections[connectionIndex][2]
                            if colour != self.selectedColour:
                                # The tile is not the same colour and should be overwritten.
                                if self.dev: print("Replacing connection...")
                                self.replaceConnection(i, self.selectedColour)
                            else:
                                # The tile is the same colour and should be removed.
                                if self.dev: print("Backtracking, removing connection...")
                                self.removeTile(self.lastSelectedTile)
                            self.lastSelectedTile = i
                            

                        else:
                            # No connections were found and a new connection will be added.
                            if self.dev: print("Tile changed:", i)

                            self.addConnection(self.lastSelectedTile, i, self.selectedColour)
                            self.lastSelectedTile = i
                    
                    return


    def findConnections(self, tile):
        # Finds the number of connection a tile has.
        connectionsFound = 0
        connectionIndex = []

        for index, connection in enumerate(self.connections):
            if connection[0] == tile or connection[1] == tile:
                connectionsFound += 1
                connectionIndex.append(index)

        # Return number of connections and a list of the connection indexes.
        return connectionsFound, connectionIndex

            
            
                    
if __name__ == "__main__":
    game = Game(sys.argv)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                if game.dev: print("Exiting..")
                sys.exit()

            # Send event to game logic (MouseManager).
            game.mouseManager.mouseTrack(event)

        # Update the screen.
        pygame.display.flip()