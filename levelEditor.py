import sys, pygame, math, json
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if self.textBox.collidepoint(pos):
                self.saveLevel()
            else:
                self.addStatic(pos)


    def addStatic(self, pos):

        for i, rect in enumerate(self.level.rectangles):
            if rect.collidepoint(pos):

                for j, static in enumerate(self.statics):
                    if static[0] == i:
                        self.colourOverride.append(static[1])

                        del self.statics[j]
                        self.reloadBoard()

                        return
                
                colour = self.selectColour()
                if not colour: return

                self.statics.append((i, colour))
                
                if self.colourOverride:
                    del self.colourOverride[0]

                self.reloadBoard()

                return

    
    def selectColour(self):
        if self.colourOverride:
            colour = self.colourOverride[0]
            
        else:
            colourIndex = math.floor(len(self.statics)/2)
            if colourIndex >= len(colours.colours):
                print("No more colours.")
                return None

            colour = colours.colours[colourIndex]
    
        return colour


    def reloadBoard(self):
        self.graphicsManager.drawBoard(self.level)
        for static in self.statics:
            self.graphicsManager.drawEndPoint(static[0], static[1])

        colour = self.selectColour()
        if not colour:
            colour = (0,0,0)
        self.graphicsManager.drawColouredBox(colour, self.level.length, self.level.length, (0,0))

        self.textBox = self.graphicsManager.drawTextBox("Save", 48, (self.level.length + 8, 8))


    def saveLevel(self):
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

        with open("levels.json") as f:
            levels = json.loads(f.read())
        newLevel = {}
        newLevel["points"] = points
        newLevel["height"] = self.level.height
        newLevel["width"] = self.level.width
        levels.append(newLevel)

        with open("levels.json", "w") as f:
            f.write(json.dumps(levels, indent=4))

        
        print(points)




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