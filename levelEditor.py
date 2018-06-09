import sys, pygame
import levels, graphicsManager


class LevelEditor():
    def __init__(self, level):
        self.level = level

        screen = pygame.display
        screen.set_caption("Flow - Level editor")
        self.screen = screen.set_mode(level.screenSize)

        self.graphicsManager = graphicsManager.GraphicsManager(self)
        self.graphicsManager.drawBoard(self.level)


if __name__ == "__main__":              
    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        
        if width > 15 or height > 15:
            print("Width and height can be max 15 tiles.")
            sys.exit()

        level = levels.Level([], width, height)

        LevelEditor(level)


    except (IndexError, TypeError):
        print("Not a valid input.")
        print("Usage: levelEditor.py <width> <height>")
        sys.exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                print("Exiting..")
                sys.exit()

            

        # Update the screen.
        pygame.display.flip()