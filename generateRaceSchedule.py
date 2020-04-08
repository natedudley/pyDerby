from queue import PriorityQueue
import random
import json
from collections import deque

numLanes = 4
numCars = 40

#returns the lane with the least number of cars
def shortestLane(lanes):
    pq = PriorityQueue()
    for i in range(0, numLanes):
        pq.put((len(lanes[i]), i))
    return pq

#list of cars say every 5th car defined by skipAmount
def getSeperatedCarList(skipAmount):
    l = []
    val = 1
    startVal = val
    for i in range(0, numCars):
        l.append(val)
        val = val + skipAmount
        if val > numCars:
            startVal = startVal + 1
            val = startVal
    return l

#returns an array of deque/queue
def generateWaitingList():
    carsWaiting = deque()
    carsWaiting.append(deque((range(1, numCars+1))))
    carsWaiting.append(deque(getSeperatedCarList(5)))
    for i in range(2, numLanes):
        carsWaiting.append(deque(random.sample(list(range(1, numCars+1)), numCars)))
    return carsWaiting

#detects if the same car is used twice in the same heat
def isCollision(selLane, val):
    collision = False
    pos = len(lanes[selLane]);
    for i in range(0, selLane):
        if len(lanes[i]) > pos:
            if lanes[i][pos] == val:
                collision = True
    return collision


#sorts the cars into lanes, making sure each car gets to use a different lane each time
def putWaitingCarsInLanes(carsWaiting):
    while(len(carsWaiting) > 0):
        curQ = carsWaiting.popleft()
        while(len(curQ) > 0):
            pq = shortestLane(lanes)
            while pq.qsize() > 0:
                selLane = pq.get()[1]
                if not curQ[0] in lanes[selLane]:
                    if not isCollision(selLane, curQ[0]):
                        lanes[selLane].append(curQ.popleft())
                        break
                    else:
                        isCollision(selLane, curQ[0])
                        curQ.rotate()
                        pq = shortestLane(lanes)


lanes = []
for i in range(0, numLanes):
    lanes.append([])


putWaitingCarsInLanes(generateWaitingList())

file = open('csv/raceSchedule.csv', 'w+')


file.write('heat#, ')
for i in range(1, numLanes+1):
    file.write('car' + str(i) + '#, pos, time'  + ', ')
file.write('timestamp\n')

for i in range(0, len(lanes[0])):
    file.write(str(i+1) + ', ')
    for j in range(0, numLanes):
        if i < len(lanes[j]):
            file.write(str(lanes[j][i]) + ', -, -,')
    file.write('-\n')

file.close()

