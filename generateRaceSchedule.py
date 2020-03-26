from queue import PriorityQueue
import random
import json
from collections import deque

numLanes = 4
numCars = 39

def shortestLane(lanes):
    pq = PriorityQueue()
    for i in range(0, numLanes):
        pq.put((len(lanes[i]), i))
    return pq

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

def generateWaitingList():
    carsWaiting = deque()
    carsWaiting.append(deque((range(1, numCars+1))))
    #carsWaiting.append(deque((range(numCars, 0, -1))))
    carsWaiting.append(deque(getSeperatedCarList(5)))
    for i in range(2, numLanes):
        carsWaiting.append(deque(random.sample(list(range(1, numCars+1)), numCars)))
    return carsWaiting

def isCollision(selLane, val):
    collision = False
    pos = len(lanes[selLane]);
    for i in range(0, selLane):
        if len(lanes[i]) > pos:
            if lanes[i][pos] == val:
                collision = True
    return collision



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

file = open('raceSchedule.csv', 'w+')


file.write('race#, ')
for i in range(1, numLanes+1):
    file.write('car' + str(i) + '#, time' + str(i)  + ', ')
file.write('timestamp\n')

for i in range(0, len(lanes[0])):
    file.write(str(i+1) + ', ')
    for j in range(0, numLanes):
        if i < len(lanes[j]):
            file.write(str(lanes[j][i]) + ', -, ')
    file.write('-\n')



file.close()

