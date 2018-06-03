def checkWin(statics, rectangles, findConnections):
    """Checks if all tiles have 2 connections or 1 if it's static. If so return true."""

    # Number of tiles
    size = len(rectangles)

    # Go through all tiles and check number of connections
    for i in range(size):
        staticTile = False
        for static in statics:
            if static[0] == i:
                # Tile is static and should therefore have 1 connection
                if findConnections(i)[0] != 1:
                    # Static tile does not have a connection -> no win
                    return False
                staticTile = True
                break

        if not staticTile:
            # Tile is not static and should therefore have 2 connections
            if findConnections(i)[0] != 2:
                # Tile does not have 2 connections -> no win
                return False

    # All tiles have been looked at and none of them is missing a connection -> win!
    return True
                
        

    