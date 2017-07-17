#!/usr/bin/env python

import roslib
import rospy
from fw_wrapper.srv import *
import time
import sys
import signal
from map import *
from map_empty import * 
import pickle

# -----------SERVICE DEFINITION-----------
# allcmd REQUEST DATA
# ---------
# string command_type
# int8 device_id
# int16 target_val
# int8 n_dev
# int8[] dev_ids
# int16[] target_vals

# allcmd RESPONSE DATA
# ---------
# int16 val
# --------END SERVICE DEFINITION----------

# ----------COMMAND TYPE LIST-------------
# GetMotorTargetPosition
# GetMotorCurrentPosition
# GetIsMotorMoving
# GetSensorValue
# GetMotorWheelSpeed
# SetMotorTargetPosition
# SetMotorTargetSpeed
# SetMotorTargetPositionsSync
# SetMotorMode
# SetMotorWheelSpeed

# wrapper function to call service to set a motor mode
# 0 = set target positions, 1 = set wheel moving
def setMotorMode(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('SetMotorMode', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to get motor wheel speed
def getMotorWheelSpeed(motor_id):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('GetMotorWheelSpeed', motor_id, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to set motor wheel speed
def setMotorWheelSpeed(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('SetMotorWheelSpeed', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to set motor target speed
def setMotorTargetSpeed(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('SetMotorTargetSpeed', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to get sensor value
def getSensorValue(port):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('GetSensorValue', port, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to set a motor target position
def setMotorTargetPositionCommand(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
	resp1 = send_command('SetMotorTargetPosition', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to get a motor's current position
def getMotorPositionCommand(motor_id):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
	resp1 = send_command('GetMotorCurrentPosition', motor_id, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to check if a motor is currently moving
def getIsMotorMovingCommand(motor_id):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
	resp1 = send_command('GetIsMotorMoving', motor_id, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# shutdown function to stop wheels
def shutdown(sig, stackframe):
    print("  Caught ctrl-c!")
    setMotorWheelSpeed(5, 0)
    setMotorWheelSpeed(6, 0)
    
    # pickling map object goes here
    
    sys.exit(0)    

def stop():
    setMotorWheelSpeed(5, 0)
    setMotorWheelSpeed(6, 0)

def move(cells, head, pos):
    
    setMotorWheelSpeed(5, 1024 + 400)
    setMotorWheelSpeed(6, 400)
    
    time.sleep(4.5 * cells)
    stop()
        
    if head == "S":
        pos = (pos[0] + cells, pos[1])
    elif head == "N":
        pos = (pos[0] - cells, pos[1])
    elif head == "W":
        pos = (pos[0], pos[1] - cells)
    else:
        pos = (pos[0], pos[1] + cells)
        
    return pos
    
def rightTurn(head):
    stop()
    setMotorWheelSpeed(5, 400)
    setMotorWheelSpeed(6, 400)
    time.sleep(1.26)
    stop()
    if head == "S":
        head = "W"
    elif head == "W":
        head = "N"
    elif head == "N":
        head = "E"
    else: 
        head = "S"    
    return head
    
def leftTurn(head):
    stop()
    setMotorWheelSpeed(5, 1024 + 400)
    setMotorWheelSpeed(6, 1024 + 400)
    time.sleep(1.26)
    stop()
    if head == "S":
        head = "E"
    elif head == "E":
        head = "N"
    elif head == "N":
        head = "W"
    else: 
        head = "S"
    return head
    
def changeHeading(curr, goal):
    if curr == "N" and goal == "N":
        pass
    if curr == "N" and goal == "S":
        leftTurn("N")
        leftTurn("W")
    if curr == "N" and goal == "W":
        leftTurn("N")
    if curr == "N" and goal == "E": 
        rightTurn("N")
    if curr == "S" and goal == "S":
        pass
    if curr == "S" and goal == "N":
        rightTurn("S")
        rightTurn("W")
    if curr == "S" and goal == "W":
        rightTurn("S")
    if curr == "S" and goal == "E":
        leftTurn("S") 
    if curr == "W" and goal == "W":
        pass
    if curr == "W" and goal == "E":
        rightTurn("W")
        rightTurn("N")
    if curr == "W" and goal == "S":
        leftTurn("W")
    if curr == "W" and goal == "N":
        rightTurn("W")     
    if curr == "E" and goal == "E":
        pass
    if curr == "E" and goal == "W":
        leftTurn("E")
        leftTurn("N")
    if curr == "E" and goal == "S":
        rightTurn("E")
    if curr == "E" and goal == "N":
        leftTurn("E") 
          
def fillCostMap(map, goal):
    print goal
    for i in xrange(8):
            for j in xrange(8):
                map.costMap[i][j] = None
    
    wavefront = getUnblockedNeighbors(map, goal)
    cost = 0
    map.setCost(goal[0], goal[1], cost)
    
    while wavefront:
        cost +=1
        potentials = []
        for cell in wavefront:
            map.setCost(cell[0], cell[1], cost)
            potentials += getUnblockedNeighbors(map, cell)
        wavefront = set(potentials)
       
def getUnblockedNeighbors(map, pos):
    neighbors = []
    if (not map.getNeighborObstacle(pos[0], pos[1], DIRECTION.North)) and map.getCost(pos[0] - 1, pos[1]) == None:
        neighbors.append( (pos[0] - 1, pos[1]))
    if (not map.getNeighborObstacle(pos[0], pos[1], DIRECTION.South)) and map.getCost(pos[0] + 1, pos[1]) == None:
        neighbors.append( (pos[0] + 1, pos[1]))
    if (not map.getNeighborObstacle(pos[0], pos[1], DIRECTION.West)) and map.getCost(pos[0], pos[1] - 1) == None:
        neighbors.append( (pos[0], pos[1] - 1))
    if (not map.getNeighborObstacle(pos[0], pos[1], DIRECTION.East)) and map.getCost(pos[0], pos[1] + 1) == None:
        neighbors.append( (pos[0], pos[1] + 1))
    return neighbors
    
def getNeighbors(map, pos):
    neighbors = []
    if (not map.getNeighborObstacle(pos[0], pos[1], DIRECTION.North)):
        neighbors.append( (pos[0] - 1, pos[1]))
    if (not map.getNeighborObstacle(pos[0], pos[1], DIRECTION.South)):
        neighbors.append( (pos[0] + 1, pos[1]))
    print pos[0], pos[1]
    if (not map.getNeighborObstacle(pos[0], pos[1], DIRECTION.West)):
        neighbors.append( (pos[0], pos[1] - 1))
    if (not map.getNeighborObstacle(pos[0], pos[1], DIRECTION.East)):
        neighbors.append( (pos[0], pos[1] + 1))
    return neighbors
    
def genPath(map, start_pos):
    
    curr_pos = start_pos
    print curr_pos
    curr_cost = 666
    path = []
    
    while curr_cost:
        costs = [map.getCost(cell[0], cell[1]) for cell in getNeighbors(map, curr_pos)]
        
        if not costs:
            break
            
        next_step = getNeighbors(map, curr_pos)[costs.index(min(costs))]    
        path.append(next_step)
        curr_pos = next_step
        curr_cost = map.getCost(curr_pos[0], curr_pos[1])
        
    print "\nTHE PATH: " 
    print path
    return path
    
def genComms(path, start_pos, start_head, goal_head):
    
    curr_pos = start_pos
    curr_head = start_head
    
    for cell in path:
        if curr_pos[0] != cell[0]:
            if cell[0] > curr_pos[0]:
                #going south
                changeHeading(curr_head, "S")
                curr_head = "S"
                curr_pos = move(1, curr_head, curr_pos)
                print "Move south"
            else:
                #going north
                changeHeading(curr_head, "N")
                curr_head = "N"
                curr_pos = move(1, curr_head, curr_pos)
                print "Move north"
        else:
            if cell[1] > curr_pos[1]:
                #going east
                changeHeading(curr_head, "E")
                curr_head = "E"
                curr_pos = move(1, curr_head, curr_pos)
                print "Move east"
            else:
                #going west
                changeHeading(curr_head, "W")
                curr_head = "W"
                curr_pos = move(1, curr_head, curr_pos)
                print "Move west"
                
    changeHeading(curr_head, goal_head)
    
### Building Map
# 
#build map - start at (0,0), facing south
def buildMap(map):
    model_map = map
    
    #model_map.clearObstacleMap()
    
    curr_pos = (0,0)
    curr_head = 'S'
    avail_dirs = setWalls(model_map, curr_pos, curr_head)
    count_visited = 0
    
    while len(avail_dirs) != 0:
        
        if 'left' in avail_dirs:
            curr_head = leftTurn(curr_head)
            curr_pos = move(1, curr_head, curr_pos)
        elif 'front' in avail_dirs:
            curr_pos = move(1, curr_head, curr_pos)
        elif 'right' in avail_dirs:
            curr_head = rightTurn(curr_head)
            curr_pos = move(1, curr_head, curr_pos)
        else:
            curr_head = leftTurn(curr_head)
            curr_head = leftTurn(curr_head)
            curr_pos = move(1, curr_head, curr_pos)
            
        avail_dirs = setWalls(model_map, curr_pos, curr_head)
        
    return model_map
              
def setWalls(model_map, pos, head):

    dirs = ['N', 'E', 'S', 'W']
    head_int = dirs.index(head) + 1
    
    reading_front = getSensorValue(3)
    print 'reading front: ', reading_front
    reading_left = getSensorValue(1)
    print 'reading left: ', reading_left
    reading_right = getSensorValue(6)
    print 'reading right: ', reading_right
    '''
    temp_head = leftTurn(head)
    time.sleep(2)
    reading_back = getSensorValue(1)
    print 'reading back: ', reading_back
    rightTurn(temp_head)
    '''
    avail_dirs = ['back']
    if reading_front > 800:
        model_map.setObstacle(pos[0], pos[1], 1, head_int)
    else:
        avail_dirs.append('front')
        
    if reading_left > 40:
        direction = (head_int + 3) % 4
        if direction == 0:
            direction = 4
        model_map.setObstacle(pos[0], pos[1], 1, direction)
    else:
        avail_dirs.append('left')
        
    if reading_right > 100:
        direction = (head_int + 1) % 4
        if direction == 0:
            direction = 4 
        model_map.setObstacle(pos[0], pos[1], 1, direction)
    else:
        avail_dirs.append('right')
        
    '''
    if reading_back > 200:
        direction = (head_int + 2) % 4
        if direction == 0:
            direction = 4  
        model_map.setObstacle(pos[0], pos[1], 1, direction)
    ''' 
    model_map.printObstacleMap()
    
    pickle.dump(model_map, open("map_file.p", "w"))
    
    return avail_dirs   

def neighborPosition(pos, direction):
    if direction == 1:
        return (pos[0]-1, pos[1])
    if direction == 2:
        return (pos[0], pos[1] + 1)
    if direction == 3:
        return (pos[0]+1, pos[1])
    if direction == 4:
        return (pos[0], pos[1] -1)
    
# Main function
if __name__ == "__main__":
    
    # taking command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if len(sys.argv) > 2:
            start_pos = (int(sys.argv[2]), int(sys.argv[3]))
            start_head = sys.argv[4]
            goal_pos = (int(sys.argv[5]), int(sys.argv[6]))
            goal_head = sys.argv[7]
            print start_pos
    
    # node startup and signal declaration
    rospy.init_node('example_node', anonymous=True)
    rospy.loginfo("Starting Group X Control Node...")
    signal.signal(signal.SIGINT, shutdown)
    
    # setting motors to wheel mode
    setMotorMode(5, 1)
    setMotorMode(6, 1)
    
    # initialize map
    map1 = EECSMap()
    empty = EECSMapEmpty()
    
    if (mode == "map"):
        empty = buildMap(empty)
        
    if (mode == "plan_built"):
        map1 = pickle.load(open("map_file.p", "r"))
        fillCostMap(map1, goal_pos)
        map1.printCostMap()
        map1.printObstacleMap()
        path = genPath(map1, start_pos)
        genComms(path, start_pos, start_head, goal_head)
        
    if (mode == "plan_default"):
        map2 = EECSMap()
        fillCostMap(map2, goal_pos)
        map2.printCostMap()
        map2.printObstacleMap()
        path = genPath(map2, start_pos)
        genComms(path, start_pos, start_head, goal_head)
        
    
    '''
    # control loop running at 10hz
    r = rospy.Rate(10)# 10hz
    
    while not rospy.is_shutdown():
        reading_front = getSensorValue(3)
        reading_left = getSensorValue(1)
        reading_right = getSensorValue(6)
        
        rospy.loginfo("Front port: %f    Left Port: %f    Right Port: %f", \
                reading_front, reading_left, reading_right)
        
        
        # Sleep to enforce loop rate
        r.sleep()
    '''
    
    





'''
# Vestigial remnants of battle droid walking. I made walking better from the asn1.py code

def returnToNeutral():
    pos_list = [510,510,510,510,772,250,600,420]
    for i, pos in enumerate(pos_list):
        setMotorTargetPositionCommand(i+1, pos)
    time.sleep(1)

def leftStep():
    
    setMotorTargetPositionCommand(4, 350)
    time.sleep(0.1)  
    setMotorTargetPositionCommand(3, 420)
    time.sleep(0.5)
    
    setMotorTargetPositionCommand(1, 400)
    setMotorTargetPositionCommand(2, 400)
    time.sleep(0.5)     
    
    setMotorTargetPositionCommand(3, 510)
    setMotorTargetPositionCommand(4, 510)
    time.sleep(0.5)
   
    setMotorTargetPositionCommand(1, 510)
    setMotorTargetPositionCommand(2, 510)
    time.sleep(0.5)
    
    
def rightStep():  
   
    setMotorTargetPositionCommand(3, 650)
    time.sleep(0.1)  
    setMotorTargetPositionCommand(4, 620)  
    time.sleep(0.5)
    
    setMotorTargetPositionCommand(1, 600)
    setMotorTargetPositionCommand(2, 600)
    time.sleep(0.6)     
    
    setMotorTargetPositionCommand(3, 510)
    setMotorTargetPositionCommand(4, 510)
    time.sleep(0.5)
    
   
    setMotorTargetPositionCommand(1, 510)
    setMotorTargetPositionCommand(2, 510)
    time.sleep(0.5)
    
    
def turnLeft():
    setMotorTargetPositionCommand(4, 320)   
    setMotorTargetPositionCommand(3, 420)  
    time.sleep(0.5)
    setMotorTargetPositionCommand(1, 650)
    time.sleep(0.5)
    setMotorTargetPositionCommand(3, 510)
    setMotorTargetPositionCommand(4, 510)
    time.sleep(0.2)
    setMotorTargetPositionCommand(1, 510)
    time.sleep(0.2)
    
    setMotorTargetPositionCommand(4, 320)   
    setMotorTargetPositionCommand(3, 420)  
    time.sleep(0.5)
    setMotorTargetPositionCommand(1, 650)
    time.sleep(0.5)
    setMotorTargetPositionCommand(3, 510)
    setMotorTargetPositionCommand(4, 510)
    time.sleep(0.2)
    setMotorTargetPositionCommand(1, 510)
    time.sleep(0.2)
    
    setMotorTargetPositionCommand(4, 320)   
    setMotorTargetPositionCommand(3, 420)  
    time.sleep(0.5)
    setMotorTargetPositionCommand(1, 650)
    time.sleep(0.5)
    setMotorTargetPositionCommand(3, 510)
    setMotorTargetPositionCommand(4, 510)
    time.sleep(0.2)
    setMotorTargetPositionCommand(1, 510)
    time.sleep(0.2)

def turnRight():
    setMotorTargetPositionCommand(3, 700)   
    setMotorTargetPositionCommand(4, 600)  
    time.sleep(0.5)
    setMotorTargetPositionCommand(2, 345)
    time.sleep(0.5)
    setMotorTargetPositionCommand(4, 510)
    setMotorTargetPositionCommand(3, 510)
    time.sleep(0.2)
    setMotorTargetPositionCommand(2, 510)
    time.sleep(0.2)
    
    setMotorTargetPositionCommand(3, 700)   
    setMotorTargetPositionCommand(4, 600)  
    time.sleep(0.5)
    setMotorTargetPositionCommand(2, 345)
    time.sleep(0.5)
    setMotorTargetPositionCommand(4, 510)
    setMotorTargetPositionCommand(3, 510)
    time.sleep(0.2)
    setMotorTargetPositionCommand(2, 510)
    time.sleep(0.2)
    
    setMotorTargetPositionCommand(3, 700)   
    setMotorTargetPositionCommand(4, 600)  
    time.sleep(0.5)
    setMotorTargetPositionCommand(2, 345)
    time.sleep(0.5)
    setMotorTargetPositionCommand(4, 510)
    setMotorTargetPositionCommand(3, 510)
    time.sleep(0.2)
    setMotorTargetPositionCommand(2, 510)
    time.sleep(0.2)

def turnAround():
    turnLeft()
    turnLeft()
    setMotorTargetPositionCommand(4, 320)   
    setMotorTargetPositionCommand(3, 420)  
    time.sleep(0.5)
    setMotorTargetPositionCommand(1, 650)
    time.sleep(0.5)
    setMotorTargetPositionCommand(3, 510)
    setMotorTargetPositionCommand(4, 510)
    time.sleep(0.2)
    setMotorTargetPositionCommand(1, 510)
    time.sleep(0.2)
     
def walkForward(num):
  
    steps = num * 10
    
    for i in xrange(steps):
        leftStep()
        rightStep()
        
    returnToNeutral()    
'''  
      
