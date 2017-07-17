#!/usr/bin/env python
import sys

# Usage:
#
# #Create object
# your_map = EECSMap()
#
# #Use Object (examples)
# your_map.printObstacleMap()
# your_map.clearObstacleMap()
# your_map.printCostMap()
# your_map.setObstacle(3, 4, 1, DIRECTION.North)
# isBlocked = your_map.getObstacle(3, 4, DIRECTION.North)
# cell_cost = your_map.getCost(3, 4)

def enum(**enums):
    return type('Enum', (), enums)

DIRECTION = enum(North=1, East=2, South=3, West=4)

class EECSMap():
    def __init__(self):
        self.horizontalWalls = [[0 for x in xrange(8)] for x in xrange(9)]
        self.verticalWalls = [[0 for x in xrange(9)] for x in xrange(8)]
        self.costMap = [[0 for x in xrange(8)] for x in xrange(8)]

        self.horizontalWalls[0][0] = 1
        self.horizontalWalls[0][1] = 1
        self.horizontalWalls[0][2] = 1
        self.horizontalWalls[0][3] = 1
        self.horizontalWalls[0][4] = 1
        self.horizontalWalls[0][5] = 1
        self.horizontalWalls[0][6] = 1
        self.horizontalWalls[0][7] = 1
        self.horizontalWalls[1][0] = 0
        self.horizontalWalls[1][1] = 1
        self.horizontalWalls[1][2] = 1
        self.horizontalWalls[1][3] = 1
        self.horizontalWalls[1][4] = 1
        self.horizontalWalls[1][5] = 1
        self.horizontalWalls[1][6] = 0
        self.horizontalWalls[1][7] = 1
        self.horizontalWalls[2][0] = 0
        self.horizontalWalls[2][1] = 1
        self.horizontalWalls[2][2] = 1
        self.horizontalWalls[2][3] = 1
        self.horizontalWalls[2][4] = 0
        self.horizontalWalls[2][5] = 0
        self.horizontalWalls[2][6] = 0
        self.horizontalWalls[2][7] = 0
        self.horizontalWalls[3][0] = 0
        self.horizontalWalls[3][1] = 1
        self.horizontalWalls[3][2] = 1
        self.horizontalWalls[3][3] = 0
        self.horizontalWalls[3][4] = 1
        self.horizontalWalls[3][5] = 0
        self.horizontalWalls[3][6] = 0
        self.horizontalWalls[3][7] = 0
        self.horizontalWalls[4][0] = 0
        self.horizontalWalls[4][1] = 1
        self.horizontalWalls[4][2] = 0
        self.horizontalWalls[4][3] = 0
        self.horizontalWalls[4][4] = 0
        self.horizontalWalls[4][5] = 0
        self.horizontalWalls[4][6] = 1
        self.horizontalWalls[4][7] = 1
        self.horizontalWalls[5][0] = 0
        self.horizontalWalls[5][1] = 0
        self.horizontalWalls[5][2] = 0
        self.horizontalWalls[5][3] = 0
        self.horizontalWalls[5][4] = 0
        self.horizontalWalls[5][5] = 0
        self.horizontalWalls[5][6] = 1
        self.horizontalWalls[5][7] = 1
        self.horizontalWalls[6][0] = 0
        self.horizontalWalls[6][1] = 0
        self.horizontalWalls[6][2] = 1
        self.horizontalWalls[6][3] = 0
        self.horizontalWalls[6][4] = 0
        self.horizontalWalls[6][5] = 1
        self.horizontalWalls[6][6] = 1
        self.horizontalWalls[6][7] = 1
        self.horizontalWalls[7][0] = 0
        self.horizontalWalls[7][1] = 1
        self.horizontalWalls[7][2] = 1
        self.horizontalWalls[7][3] = 0
        self.horizontalWalls[7][4] = 0
        self.horizontalWalls[7][5] = 1
        self.horizontalWalls[7][6] = 1
        self.horizontalWalls[7][7] = 0
        self.horizontalWalls[8][0] = 1
        self.horizontalWalls[8][1] = 1
        self.horizontalWalls[8][2] = 1
        self.horizontalWalls[8][3] = 1
        self.horizontalWalls[8][4] = 1
        self.horizontalWalls[8][5] = 1
        self.horizontalWalls[8][6] = 1
        self.horizontalWalls[8][7] = 1

        self.verticalWalls[0][0] = 1
        self.verticalWalls[0][1] = 0
        self.verticalWalls[0][2] = 0
        self.verticalWalls[0][3] = 0
        self.verticalWalls[0][4] = 1
        self.verticalWalls[0][5] = 0
        self.verticalWalls[0][6] = 0
        self.verticalWalls[0][7] = 0
        self.verticalWalls[0][8] = 1
        self.verticalWalls[1][0] = 1
        self.verticalWalls[1][1] = 0
        self.verticalWalls[1][2] = 0
        self.verticalWalls[1][3] = 0
        self.verticalWalls[1][4] = 0
        self.verticalWalls[1][5] = 0
        self.verticalWalls[1][6] = 1
        self.verticalWalls[1][7] = 1
        self.verticalWalls[1][8] = 1
        self.verticalWalls[2][0] = 1
        self.verticalWalls[2][1] = 1
        self.verticalWalls[2][2] = 0
        self.verticalWalls[2][3] = 0
        self.verticalWalls[2][4] = 0
        self.verticalWalls[2][5] = 1
        self.verticalWalls[2][6] = 1
        self.verticalWalls[2][7] = 1
        self.verticalWalls[2][8] = 1
        self.verticalWalls[3][0] = 1
        self.verticalWalls[3][1] = 0
        self.verticalWalls[3][2] = 0
        self.verticalWalls[3][3] = 1
        self.verticalWalls[3][4] = 1
        self.verticalWalls[3][5] = 1
        self.verticalWalls[3][6] = 0
        self.verticalWalls[3][7] = 0
        self.verticalWalls[3][8] = 1
        self.verticalWalls[4][0] = 1
        self.verticalWalls[4][1] = 0
        self.verticalWalls[4][2] = 0
        self.verticalWalls[4][3] = 1
        self.verticalWalls[4][4] = 1
        self.verticalWalls[4][5] = 1
        self.verticalWalls[4][6] = 0
        self.verticalWalls[4][7] = 0
        self.verticalWalls[4][8] = 1
        self.verticalWalls[5][0] = 1
        self.verticalWalls[5][1] = 1
        self.verticalWalls[5][2] = 1
        self.verticalWalls[5][3] = 0
        self.verticalWalls[5][4] = 1
        self.verticalWalls[5][5] = 0
        self.verticalWalls[5][6] = 0
        self.verticalWalls[5][7] = 0
        self.verticalWalls[5][8] = 1
        self.verticalWalls[6][0] = 1
        self.verticalWalls[6][1] = 1
        self.verticalWalls[6][2] = 0
        self.verticalWalls[6][3] = 1
        self.verticalWalls[6][4] = 0
        self.verticalWalls[6][5] = 1
        self.verticalWalls[6][6] = 0
        self.verticalWalls[6][7] = 0
        self.verticalWalls[6][8] = 1
        self.verticalWalls[7][0] = 1
        self.verticalWalls[7][1] = 0
        self.verticalWalls[7][2] = 0
        self.verticalWalls[7][3] = 0
        self.verticalWalls[7][4] = 1
        self.verticalWalls[7][5] = 0
        self.verticalWalls[7][6] = 0
        self.verticalWalls[7][7] = 0
        self.verticalWalls[7][8] = 1

        for i in xrange(8):
            for j in xrange(8):
                self.costMap[i][j] = 0

        self.obstacle_size_x = 8
        self.obstacle_size_y = 8
        self.costmap_size_x = 8
        self.costmap_size_y = 8

    # ***********************************************************************
    # Function Name : getNeighborObstacle
    # Description   : Checks if the neighboring cell is blocked on the map.
    # Input         : i: The row coordinate of the current cell on the map.
    #               : j: The column coordinate of the current cell on the map
    #               : dir: A Direction enumeration (North, South, East, West)
    #               :      indicating which neighboring cell to check for
    #               :      obstacles
    # Output        : None
    # Return        : 1 if neighboring cell is blocked, 0 if neighboring cell
    #               : is clear, -1 if index i or j is out of bounds
    # ***********************************************************************/
    def getNeighborObstacle(self, i, j, dir):
        if (((i < 0 or i > 7 or j < 0 or j > 8) and (dir == DIRECTION.West or dir == DIRECTION.East)) and ((j < 0 or j > 7 or i < 0 or i > 8) and (dir == DIRECTION.North or dir == DIRECTION.South))):
            print "ERROR (getNeighborObstacle): index out of range"
            return -1

        isBlocked = 0
        if dir == DIRECTION.North:
            isBlocked = self.horizontalWalls[i][j]
        elif dir == DIRECTION.South:
            isBlocked = self.horizontalWalls[i+1][j]
        elif dir == DIRECTION.West:
            isBlocked = self.verticalWalls[i][j]
        elif dir == DIRECTION.East:
            isBlocked = self.verticalWalls[i][j+1]

        return isBlocked

    # ******************************************************************************
    # Function Name  : setObstacle
    # Description    : Used for map building, sets the obstacle status of a given map cell
    # Input          : i: The row coordinate of the current cell on the map.
    #                : j: The column coordinate of the current cell on the map
    #                : isBlocked: A boolean (0 or 1) value indicated if the cell is blocked
    #                : dir: A Direction enumeration (North, South, East, West) indicating
    #                :      which neighboring cell to set for obstacles
    # Output         : None
    # Return         : 0 if successful, -11 if i or j is out of map bounds, -2 if isBlocked is not 0 or 1
    # *****************************************************************************/
    def setObstacle(self, i, j, isBlocked, dir):
        if (((i < 0 or i > 7 or j < 0 or j > 8) and (dir == DIRECTION.West or dir == DIRECTION.East)) or ((j < 0 or j > 7 or i < 0 or i > 8) and (dir == DIRECTION.North or dir == DIRECTION.South))):
            print "ERROR (setObstacle): index out of range, obstacle not set"
            return -1

        if isBlocked > 1:
            print "ERROR (setObstacle): isBlocked not a valid input, obstacle not set"
            return -2

        if dir == DIRECTION.North:
            self.horizontalWalls[i][j] = isBlocked
        elif dir == DIRECTION.South:
            self.horizontalWalls[i+1][j] = isBlocked
        elif dir == DIRECTION.West:
            self.verticalWalls[i][j] = isBlocked
        elif dir == DIRECTION.East:
            self.verticalWalls[i][j+1] = isBlocked

        return 0

    # ******************************************************************************
    # Function Name  : getNeighborCost
    # Description    : Retrieves the calculated cost of a neighboring cell on the map.
    # Input          : i: The row coordinate of the current cell on the map.
    #                : j: The column coordinate of the current cell on the map
    #                : dir: A Direction enumeration (North, South, East, West) indicating
    #                :      which neighboring cell to retrieve the cost.
    # Output         : None
    # Return         : Positive float valued cost for the neighboring cell, -1 on error
    # *****************************************************************************/
    def getNeighborCost(self, i, j, dir):
        if (i < 0 or i > 7 or j < 0 or j > 7):
            print "ERROR (getNeighborCost): index out of range"
            return -1

        cellValue = 0
        if dir == DIRECTION.North:
            if (i == 0):
                cellValue = 1000
            else:
                cellValue = self.costMap[i-1][j]
        elif dir == DIRECTION.South:
            if(i == 7):
                cellValue = 1000
            else:
                cellValue = self.costMap[i+1][j]
        elif dir == DIRECTION.West:
            if (j == 0):
                cellValue = 1000
            else:
                cellValue = self.costMap[i][j-1]
        elif dir == DIRECTION.East:
            if (j == 7):
                cellValue = 1000
            else:
                cellValue = self.costMap[i][j+1]

        return cellValue

    # ******************************************************************************
    # Function Name  : setNeighborCost
    # Description    : Sets the calculated cost of a neighboring cell on the map.
    # Input          : i: The row coordinate of the current cell on the map.
    #                : j: The column coordinate of the current cell on the map
    #                : dir: A Direction enumeration (North, South, East, West) indicating
    #                :      which neighboring cell to retrieve the cost.
    #                : val: Positive float valued cost for the neighboring cell
    # Output         : None
    # Return         : None
    # *****************************************************************************/
    def setNeighborCost(self, i, j, dir, val):
        if (i < 0 or i > 7 or j < 0 or j > 7):
            print "ERROR (setNeighborCost): index out of range, value not set"
            return

        if dir == DIRECTION.North:
            if (i > 0):
                self.costMap[i-1][j] = val
        elif dir == DIRECTION.South:
            if (i < 7):
                self.costMap[i+1][j] = val
        elif dir == DIRECTION.West:
            if (j > 0):
                self.costMap[i][j-1] = val
        elif dir == DIRECTION.East:
            if (j < 7):
                self.costMap[i][j+1] = val

    # ******************************************************************************
    # Function Name  : setCost
    # Description    : Used for map building, sets the calculated cost of a given map cell
    # Input          : i: The row coordinate of the current cell on the map.
    #                : j: The column coordinate of the current cell on the map
    #                : val: An integer value (0 to 1023) indicated the cost of a map cell
    # Output         : None
    # Return         : 0 if successful, -1 if i or j is out of map bounds
    # *****************************************************************************/
    def setCost(self, i, j, val):
        if (i < 0 or i > 7 or j < 0 or j > 7):
            print "ERROR (setCost): index out of range"
            return -1

        self.costMap[i][j] = val
        return 0

    # ******************************************************************************
    # Function Name  : getCost
    # Description    : Used for map building, gets the calculated cost of a given map cell
    # Input          : i: The row coordinate of the current cell on the map.
    #                : j: The column coordinate of the current cell on the map
    # Output         : None
    # Return         : cost >= 0 if successful, -1 if i or j is out of map bounds
    # *****************************************************************************/
    def getCost(self, i, j):
        if (i < 0 or i > 7 or j < 0 or j > 7):
            print "ERROR (getCost): index out of range"
            return -1

        return self.costMap[i][j]

    # ******************************************************************************
    # Function Name  : clearCostMap
    # Description    : Sets all of the values in the cost map to 0
    # Input          : None
    # Output         : None
    # Return         : None
    # *****************************************************************************/
    def clearCostMap(self):
        for i in xrange(8):
            for j in xrange(8):
                self.costMap[i][j] = 0

    # ******************************************************************************
    # Function Name  : clearObstacleMap
    # Description    : Sets all of the values in the obstacle map to 0
    # Input          : None
    # Output         : None
    # Return         : None
    # *****************************************************************************/
    def clearObstacleMap(self):
        for i in xrange(8):
            for j in xrange(9):
                self.verticalWalls[i][j] = 0

        for i in xrange(9):
            for j in xrange(8):
                self.horizontalWalls[i][j] = 0

    # ******************************************************************************
    # Function Name  : printCostMap
    # Description    : When connected to a terminal, will print out the 8x8 cost map
    # Input          : None
    # Output         : None
    # Return         : None
    # *****************************************************************************/
    def printCostMap(self):
        print "Cost Map:"
        for i in xrange(8):
            for j in xrange(8):
                print(str(self.costMap[i][j])),

            print " "

    # ******************************************************************************
    # Function Name  : printObstacleMap
    # Description    : When connected to a terminal, will print out the 8x8 obstacle map
    # Input          : None
    # Output         : None
    # Return         : None
    # *****************************************************************************/
    def printObstacleMap(self):
        print "Obstacle Map: "
        for i in xrange(8):
            for j in xrange(8):
                if (self.horizontalWalls[i][j] == 0):
                    if i == 0:
                        sys.stdout.write(" ---")
                    else:
                        sys.stdout.write("    ")
                else:
                    sys.stdout.write(" ---")

            print " "
            for j in xrange(8):
                if (self.verticalWalls[i][j] == 0):
                    if j == 7:
                        sys.stdout.write("  O |")
                    elif j == 0:
                        sys.stdout.write("| O ")
                    else:
                        sys.stdout.write("  O ")
                else:
                    if j == 7:
                        sys.stdout.write("| O |")
                    else:
                        sys.stdout.write("| O ")
            print " "
        for j in xrange(8):
                sys.stdout.write(" ---")
        print " "

    # ******************************************************************************
    # Function Name  : getCostmapSize
    # Description    : Retrieve the size of a given dimension of the costmap
    # Input          : bool xDim (true for x dimension, false for y dimension)
    # Output         : None
    # Return         : costmap size in the requested dimension
    # *****************************************************************************/
    def getCostmapSize(self, xDim):
        if (xDim):
            return self.costmap_size_x
        else:
            return self.costmap_size_y

    # ******************************************************************************
    # Function Name  : getObstacleMapSize
    # Description    : Retrieve the size of a given dimension of the Obstacle Map
    # Input          : bool xDim (true for x dimension, false for y dimension)
    # Output         : None
    # Return         : obstacle map size in the requested dimension
    # *****************************************************************************/
    def getObstacleMapSize(self, xDim):
        if xDim:
            return self.obstacle_size_x
        else:
            return self.obstacle_size_y
