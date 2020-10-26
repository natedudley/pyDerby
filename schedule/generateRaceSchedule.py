import random
import json
from collections import deque
from classes import CsvReader
from os import path

class RaceSchedule:

    lanes = []
    numCars = 40
    numLanes = 4;
    fileName = ''

    def __init__(self, fileName, numLanes=4):

        if numLanes > numCars:
            numLanes = numCars

        self.fileName = fileName
        if path.exists(self.fileName):
            self.prevSched = CsvReader.CSVReader(self.fileName)

    #returns the lane with the least number of cars
    def shortestLane(self):
        laneIndexByLen = [0]

        for i in range(1, self.numLanes):
            found = False
            lenI = len(self.lanes[i])
            for j in range(0, len(laneIndexByLen)):
                if lenI < len(self.lanes[laneIndexByLen[j]]):
                    laneIndexByLen.insert(j, i)
                    found = True
                    break
            if not found:
                laneIndexByLen.append(i)
        return laneIndexByLen

    #list of cars say every 5th car defined by skipAmount
    def getSeperatedCarList(self, skipAmount):
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
    def generateWaitingList(self):
        carsWaiting = deque()
        carsWaiting.append(deque((range(1, numCars+1))))
        carsWaiting.append(deque(self.getSeperatedCarList(5)))
        for i in range(2, self.numLanes):
            carsWaiting.append(deque(random.sample(list(range(1, self.numCars+1)), self.numCars)))
        return carsWaiting

    #detects if the same car is used twice in the same heat
    def isCollision(self, selLane, val):
        collision = False
        pos = len(self.lanes[selLane]);
        for i in range(0, selLane):
            if len(self.lanes[i]) > pos:
                if self.lanes[i][pos] == val:
                    collision = True
        return collision


    #sorts the cars into lanes, making sure each car gets to use a different lane each time
    def putWaitingCarsInLanes(self, carsWaiting):
        while(len(carsWaiting) > 0):
            curQ = carsWaiting.popleft()
            while(len(curQ) > 0):
                pq = self.shortestLane()
                qPassCount = 0
                while len(pq) > 0:
                    selLane = pq[0]
                    if not curQ[0] in self.lanes[selLane]:
                        if not self.isCollision(selLane, curQ[0]):
                            self.lanes[selLane].append(curQ.popleft())
                            break
                        else:
                            curQ.rotate()
                            qPassCount+=1
                            if qPassCount < len(curQ) + 1:
                                pq = self.shortestLane()
                            else:
                                pq = pq[1:] + pq[:1]

                            if qPassCount > 1000:
                                print("could not find spots for: ")
                                for q in curQ:
                                    print(str(q))
                                return False
                    else:
                        pq = pq[1:] + pq[:1]

        return True




    def writeSchedule(self):
        file = open(self.fileName, 'w+')

        file.write('heat#, ')
        for i in range(1, numLanes + 1):
            file.write('car' + str(i) + '#, pos, time' + ', ')
        file.write('timestamp\n')

        start = 0
        if path.exists(self.fileName):
            for r in self.prevSched.rows:
                if len(r[self.prevSched.headerToIndex['timestamp']]) > 2:
                    start += 1
                    for c in r:
                        if len(c) > 0:
                            file.write(c + ', ')
                    file.write('\n')

        for i in range(start, len(self.lanes[0])):
            file.write(str(i + 1) + ', ')
            for j in range(0, numLanes):
                if i < len(self.lanes[j]):
                    file.write(str(self.lanes[j][i]) + ', -, -,')
            file.write('-\n')

        file.close()

    def initLanes(self):
        self.lanes = []
        if self.numCars < self.numLanes:
            self.numLanes = self.numCars
        for i in range(0, numLanes):
            self.lanes.append([])

        cars = []
        if path.exists(self.fileName):
            prevSched = CsvReader.CSVReader(self.fileName)

            carHeaders = ['car1#', 'car2#', 'car3#', 'car4#']
            for r in prevSched.rows:
                if len(r[prevSched.headerToIndex['timestamp']]) > 2:
                    for i in range(1,numLanes+1):
                        h = 'car' + str(i) + '#'
                        if h in prevSched.headerToIndex:
                            carNum = int(r[prevSched.headerToIndex[h]])
                            cars.append(carNum)
                            self.lanes[i-1].append(carNum)

        return cars

    def basic(self):
        self.initLanes()
        self.putWaitingCarsInLanes(self.generateWaitingList())
        self.writeSchedule()

    def removeFromList(self, listA, listB):
        toRemove = []
        for i in range(0, len(listB)):
            if listB[i] in listA:
                toRemove.append(listB[i])
        for r in toRemove:
            if r in listB and r in listA:
                listA.remove(r)
                listB.remove(r)

    def byDen(self, name):
        name = name.lower()

        reg = CsvReader.CSVReader('../csv/registration.csv')

        cars = []
        for r in reg.rows:
            if r[reg.headerToIndex['den']].lower() == name and r[reg.headerToIndex['checkedIn']].lower() == 'yes':
                carNum = int(r[reg.headerToIndex['carNum']])
                cars.append((carNum))

        self.numCars = len(cars)

        if numCars < 1:
            print("no cars for: " + name)
            return

        found = False
        while not found:
            print('placing cars:')
            usedCars = self.initLanes()

            carsWaiting = deque()
            carsCopy = cars.copy()
            self.removeFromList(usedCars, carsCopy)
            carsWaiting.append(deque(carsCopy))
            for i in range(1, self.numLanes):
                carsCopy = cars.copy()
                self.removeFromList(usedCars, carsCopy)
                carsWaiting.append(deque(random.sample(carsCopy, len(carsCopy))))

            found = self.putWaitingCarsInLanes(carsWaiting)

        print('found spots')
        self.writeSchedule()

if __name__ == "__main__":
    numLanes = 4
    numCars = 40
    rs = RaceSchedule('../csv/raceSchedule.csv')
    #basic(numLanes, numCars)
    rs.byDen("Tiger")