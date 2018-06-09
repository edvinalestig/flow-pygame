import sys, pygame, math
import levels, graphicsManager, colours


class LevelEditor():
    def __init__(self, level):
        self.level = level

        self.statics = []

        screen = pygame.display
        screen.set_caption("Flow - Level editor")
        self.screen = screen.set_mode(level.screenSize)

        self.graphicsManager = graphicsManager.GraphicsManager(self)
        self.reloadBoard()


    def mouseManager(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.addStatic(pos)


    def addStatic(self, pos):
        colourIndex = math.floor(len(self.statics)/2)
        if colourIndex >= len(colours.colours):
            print("No more colours.")
            return
            
        colour = colours.colours[colourIndex]

        for i, rect in enumerate(self.level.rectangles):
            if rect.collidepoint(pos):
                try:
                    index = self.statics.index(i) # NOPE
                    del self.statics[index]
                    # self.reloadBoard()

                    # return
                    print("Hello")

                except ValueError:
                    self.statics.append((i, colour))

                self.reloadBoard()
                return


    def reloadBoard(self):
        self.graphicsManager.drawBoard(self.level)
        for static in self.statics:
            self.graphicsManager.drawEndPoint(static[0], static[1])



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