import random, json, math
import pygame

class Level():
    def __init__(self, points, width, height):
        """Initialise the level with screen info and tiles."""
        
        # Length in pixels
        self.length = self.__getSideLength(width, height)
        # Screen size in pixels
        self.screenSize = self.length * (width+2), self.length * (height+2)
        # Width in tiles
        self.width = width
        # Height in tiles
        self.height = height
        
        # Creating the static and normal tiles.
        self.statics = self.__createStatics(points)
        self.rectangles, self.centrePoints = self.__createTiles(self.length, width, height)


    def __getSideLength(self, width, height):
        """Returns the optimal tile side length."""

        # Get screen size from config file.
        with open("config.txt") as f:
            config = json.loads(f.read())

        tileWidth = config["screenWidth"]
        tileHeight = config["screenHeight"]

        # Get max tile height and width.
        tileHeight = math.floor(tileHeight / (height+2))
        tileWidth = math.floor(tileWidth / (width+2))

        # Get the smallest of the two so the tile can be square.
        if tileHeight > tileWidth:
            sideLength = tileWidth
        else:
            sideLength = tileHeight

        return sideLength


    def __createStatics(self, points):
        """Creates a list of static tiles."""

        statics = []
        for array in points:
            colour = array[0]
            index1 = array[1]
            index2 = array[2]
            statics.append([index1, colour])
            statics.append([index2, colour])

        return statics
        

    def __createTiles(self, length, width, height):
        """Creates a list of tiles and their centre points."""

        rectangles = []
        centrePoints = []
        
        # Defines the dimensions required to fit all tiles
        totalHeight = length * height
        totalWidth = length * width
        
        # Go through all tiles
        y = length
        while y < totalHeight + length:

            x = length
            while x < totalWidth + length:
                # Creates a Rect object
                rectangle = pygame.Rect(x, y, length, length)
                rectangles.append(rectangle)

                # Calculates the tile's centre point.
                centrePoint = (math.floor(x + length/2), math.floor(y + length/2))
                centrePoints.append(centrePoint)

                x += length
            y += length

        return rectangles, centrePoints


# Colours
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
magenta = (255, 0, 255)
cyan = (0, 255, 255)
white = (255, 255, 255)
grey = (127, 127, 127)
orange = (255, 128, 0)
darkGreen = (0, 100, 0)
purple = (128, 0, 128)
darkRed = (139, 0, 0)


# --- The levels ---

# [colour, start tile, end tile]
# points1 = [[red, 0, 24], [green, 1, 14], [blue, 12, 23], [yellow, 10, 20], [cyan, 11, 21]]
# level1 = Level(points1, 5, 5)

# points2 = [[yellow, 3, 96], [red, 4, 43], [purple, 6, 97], [grey, 13, 68], [orange, 31, 58], [blue, 32, 40], [darkGreen, 33, 66], [white, 42, 59], [magenta, 52, 88], [darkRed, 60, 87], [cyan, 67, 65]]
# level2 = Level(points2, 9, 11)

# points3 = [(darkGreen, 22, 104), (red, 34, 123), (blue, 44, 127), (yellow, 65, 117), (orange, 90, 133), (cyan, 105, 124)]
# level3 = Level(points3, 12, 12)

# levels = [level1, level2, level3]

with open("levels.json") as f:
    levels = json.loads(f.read())



# Functions to call when you want to get a level.
def getRandomLevel():
    level = random.randint(0, len(levels)-1)
    return Level(levels[level]["points"], levels[level]["width"], levels[level]["height"])

def getLevel(number):
    return levels[number]