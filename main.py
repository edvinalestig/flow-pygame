import pygame, sys, json
import levels


class Game():
    def __init__(self, dev=False):
        self.dev = dev
        
        pygame.init()

        with open("config.txt") as f:
            config = json.loads(f.read())

        if self.dev: print(config)
        self.sideLength = config["sideLength"]
        

        self.rectangles = []
        self.statics = []
        
        level = levels.getLevel()
        self.loadLevel(level)


    def loadLevel(self, level):
        
        squares = level["squares"]

        size = self.sideLength * (squares+2), self.sideLength * (squares+2)
        if self.dev: print("Screen size:", size)

        fillHeight, fillWidth = self.sideLength * squares, self.sideLength * squares

        self.screen = pygame.display.set_mode(size)
        

        i = self.sideLength
        while i < fillWidth + self.sideLength:

            j = self.sideLength
            while j < fillHeight + self.sideLength:

                rectangle = pygame.Rect(i, j, self.sideLength, self.sideLength)
                pygame.draw.rect(self.screen, [i/2, j/2, 255], rectangle, 5)
                self.rectangles.append(rectangle)

                j += self.sideLength
            i += self.sideLength

        if self.dev: 
            print("Level loaded")
            print("Rectangles:", self.rectangles)
            print("Statics:", self.statics)


    def createStaticSquare(self, index, colour):
        self.statics.append(index)
        rectangle = self.rectangles[index]
        pygame.draw.rect(self.screen, colour, rectangle)


    def fillRect(self, pos, colour=[0, 255, 0]): # Byt funktionsnamn
        for i in self.rectangles:
            if i.collidepoint(pos):
                pygame.draw.rect(self.screen, colour, i)

print(sys.argv[1])
if sys.argv[1] == "-d": 
    game = Game(True)
else:
    game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            game.fillRect(pos)
            if game.dev: print("Click at", pos)

    
    pygame.display.flip()