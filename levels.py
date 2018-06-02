import random

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
    level1 = {"height": 5, "width": 5, "points": points1}

    points2 = [[yellow, 3, 96], [red, 4, 43], [purple, 6, 97], [grey, 13, 68], [orange, 31, 58], [blue, 32, 40], [darkGreen, 33, 66], [white, 42, 59], [magenta, 52, 88], [darkRed, 60, 87], [cyan, 67, 65]]
    level2 = {"height": 11, "width": 9, "points": points2}


    levels = [level1, level2]
    level = random.randint(0, len(levels)-1)
    return levels[level]