import sys, pygame, math, json, os
import levels, graphicsManager, colours


class LevelEditor():
    def __init__(self, level):
        pygame.init()
        
        self.level = level

        self.statics = []
        self.colourOverride = []

        screen = pygame.display
        screen.set_caption("Flow - Level editor")
        self.screen = screen.set_mode(level.screenSize)

        self.graphicsManager = graphicsManager.GraphicsManager(self)
        self.reloadBoard()


    def mouseManager(self, event):
        """Manages mouse events."""

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Check if the save or test button was pressed.
            if self.saveBox.collidepoint(pos):
                self.saveLevel()
            elif self.testBox.collidepoint(pos):
                self.testLevel()
            else:
                # Make a tile static.
                self.addStatic(pos)


    def addStatic(self, pos):
        """Converts a tile to a static tile."""

        # Get what tile was pressed
        for i, rect in enumerate(self.level.rectangles):
            if rect.collidepoint(pos):

                # Check if it's already static
                for j, static in enumerate(self.statics):
                    if static[0] == i:
                        # Remove staticity
                        self.colourOverride.append(static[1])

                        del self.statics[j]
                        self.reloadBoard()

                        return
                
                # Get a colour
                colour = self.selectColour()
                if not colour: return

                # Add the tile to the statics list
                self.statics.append((i, colour))
                
                if self.colourOverride:
                    del self.colourOverride[0]

                self.reloadBoard()

                return

    
    def selectColour(self):
        """Returns the next colour to be used."""

        # If a static tile was removed the colour is placed in the override list which has priority
        if self.colourOverride:
            colour = self.colourOverride[0]
            
        else:
            # Get the number of static tiles and divide by two to get an index. Two tiles share a colour.
            colourIndex = math.floor(len(self.statics)/2)
            if colourIndex >= len(colours.colours):
                print("No more colours.")
                return None

            colour = colours.colours[colourIndex]
    
        return colour


    def reloadBoard(self):
        """Reloads the board. Draws static tiles, a colour box and save and test buttons."""

        # Draws the statics
        self.graphicsManager.drawBoard(self.level)
        for static in self.statics:
            self.graphicsManager.drawEndPoint(static[0], static[1])

        # Gets the next colour and displays it
        colour = self.selectColour()
        if not colour:
            colour = (0,0,0)
        self.graphicsManager.drawColouredBox(colour, self.level.length, self.level.length, (0,0))

        # Test and save boxes
        self.saveBox = self.graphicsManager.drawTextBox("Save", 48, (self.level.length + 8, 8))
        self.testBox = self.graphicsManager.drawTextBox("Test the level", 48, (self.level.length * 3 + 8, 8))


    def saveLevel(self, test=False):
        """Saves the level. If testing is wanted it's saved to a temp file. Otherwise in the main levels file."""

        # Stores the statics in the correct way - [colour, tile1, tile2]
        points = []
        for static in self.statics:
            found = False
            i = 0
            while i < len(points):
                if points[i][0] == static[1]:
                    points[i].append(static[0])
                    found = True
                    break
                i += 1
            
            if not found:
                points.append([static[1], static[0]])

        # Appends to saved levels or overwrites old tempfile if testing is chosen.
        if test:
            levels = []
            filename = "tempsave.json"
        else:
            with open("levels.json") as f:
                levels = json.loads(f.read())
            filename = "levels.json"


        # Store the info in a dict
        newLevel = {}
        newLevel["points"] = points
        newLevel["height"] = self.level.height
        newLevel["width"] = self.level.width
        levels.append(newLevel)

        # Saves to file
        with open(filename, "w") as f:
            f.write(json.dumps(levels)) # , indent=4

        
        print(points)


    def testLevel(self):
        """Method for testing the level. Opens the main game in testing mode."""

        self.saveLevel(True)
        os.system("main.py -t -d")





if __name__ == "__main__":
    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        
        if width > 15 or height > 15:
            print("Width and height can be max 15 tiles.")
            sys.exit()

        level = levels.Level([], width, height)

        editor = LevelEditor(level)


    except (IndexError, TypeError):
        print("Not a valid input.")
        print("Usage: levelEditor.py <width> <height>")
        sys.exit()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                print("Exiting..")
                sys.exit()


            editor.mouseManager(event)

        # Update the screen.
        pygame.display.flip()