import pygame

class MouseManager():
    def __init__(self, game):
        self.game = game

        self.mousePressed = False

    def mouseTrack(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()


            if self.game.dev:
                if self.game.reloadButton.collidepoint(pos):
                    print("\nReloading game\n")
                    self.game.__init__(True)
                    return

            
            for i, value in enumerate(self.game.rectangles):
                if value.collidepoint(pos):
                    self.lastSelectedTile = i

                    for array in self.game.statics:
                        if array[0] == i:
                            self.mousePressed = True
                            if self.game.dev: print("Mouse pressed on a static tile")
                            
                            self.selectedColour = array[1]
                            if self.game.dev: print("Selected colour:", self.selectedColour)

                            self.changedTiles = []

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

                        neighbourTile = False
                        if i == self.lastSelectedTile + 1:
                            neighbourTile = True
                        elif i == self.lastSelectedTile - 1:
                            neighbourTile = True
                        elif i == self.lastSelectedTile + self.game.width:
                            neighbourTile = True
                        elif i == self.lastSelectedTile - self.game.width:
                            neighbourTile = True

                        if neighbourTile:
                            try:
                                self.changedTiles.index(i)
                                return

                            except ValueError:
                                self.changedTiles.append(i)

                            if self.game.dev: print("Tile changed:", i)

                            self.game.addConnection(self.lastSelectedTile, i, self.selectedColour)
                            # self.game.drawLine(self.lastSelectedTile, i, self.selectedColour)

                            self.lastSelectedTile = i
                        return