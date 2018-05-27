import pygame

class MouseManager():
    def __init__(self, game):
        self.game = game

        self.mousePressed = False

    def mouseTrack(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()
            for i, value in enumerate(self.game.rectangles):
                if value.collidepoint(pos):
                    self.lastSelectedTile = i

                    for array in self.game.statics:
                        if array[0] == i:
                            self.mousePressed = True
                            if self.game.dev: print("Mouse pressed at a static tile")
                            
                            self.game.selectedColour = array[1]
                            if self.game.dev: print("Selected colour:", self.game.selectedColour)

                            self.game.changedTiles = []

                            return
                    if self.game.filledTiles[i]:
                        self.game.removeTile(i)

        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mousePressed = False
            
            
        elif self.mousePressed:
            pos = pygame.mouse.get_pos()

            for i, rect in enumerate(self.game.rectangles):
                if rect.collidepoint(pos):
                    if i != self.lastSelectedTile:
                        try:
                            self.game.changedTiles.index(i)
                            return

                        except ValueError:
                            self.game.changedTiles.append(i)

                        if self.game.dev: print("Tile changed:", i)

                        self.game.drawLine(self.lastSelectedTile, i, self.game.selectedColour)

                        #self.game.fillTile(colour=self.game.selectedColour, index=i)
                        self.lastSelectedTile = i
                        return