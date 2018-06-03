import random, json, math
import pygame

def getLevel():
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
    
    # [colour, start tile, end tile]
    points1 = [[red, 0, 24], [green, 1, 14], [blue, 12, 23], [yellow, 10, 20], [cyan, 11, 21]]
    level1 = Level(points1, 5, 5)

    points2 = [[yellow, 3, 96], [red, 4, 43], [purple, 6, 97], [grey, 13, 68], [orange, 31, 58], [blue, 32, 40], [darkGreen, 33, 66], [white, 42, 59], [magenta, 52, 88], [darkRed, 60, 87], [cyan, 67, 65]]
    level2 = Level(points2, 9, 11)


    levels = [level1, level2]
    level = random.randint(0, len(levels)-1)
    return levels[level]


class Level():
    def __init__(self, points, width, height):
        self.length = self.getSideLength(width, height)
        self.screenSize = self.length * (width+2), self.length * (height+2)
        self.width = width
        self.height = height
        
        self.statics = self.createStatics(points)
        self.rectangles, self.centrePoints = self.createTiles(self.length, width, height)


    def getSideLength(self, width, height):
        with open("config.txt") as f:
            config = json.loads(f.read())

        tileWidth = config["screenWidth"]
        tileHeight = config["screenHeight"]

        tileHeight = math.floor(tileHeight / (height+2))
        tileWidth = math.floor(tileWidth / (width+2))

        if tileHeight > tileWidth:
            sideLength = tileWidth
        else:
            sideLength = tileHeight

        return sideLength


    def createStatics(self, points):
        statics = []
        for array in points:
            colour = array[0]
            index1 = array[1]
            index2 = array[2]
            statics.append([index1, colour])
            statics.append([index2, colour])

        return statics
        

    def createTiles(self, length, width, height):
        rectangles = []
        centrePoints = []
        
        totalHeight = length * height
        totalWidth = length * width
        
        y = length
        while y < totalHeight + length:

            x = length
            while x < totalWidth + length:

                # Rect(left, top, width, height) -> Rect
                rectangle = pygame.Rect(x, y, length, length)
                rectangles.append(rectangle)

                centrePoint = (math.floor(x + length/2), math.floor(y + length/2))
                centrePoints.append(centrePoint)

                x += length
            y += length

        return rectangles, centrePoints