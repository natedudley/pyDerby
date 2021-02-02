import random
from collections import deque
from os import path

from classes import CsvReader

from tkinter import *
from tkinter.ttk import *
from classes import logger



class RaceSchedule:

    def __init__(self, scheduleFileName, registrationFileName, numLanes=4):

        self.numLanes = numLanes
        self.numCars = 40

        self.fileName = scheduleFileName
        if path.exists(self.fileName):
            self.prevSched = CsvReader.CSVReader(self.fileName)

        self.reg = CsvReader.CSVReader(registrationFileName)

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
        for i in range(0, self.numCars):
            l.append(val)
            val = val + skipAmount
            if val > self.numCars:
                startVal = startVal + 1
                val = startVal
        return l

    #returns an array of deque/queue
    def generateWaitingList(self):
        carsWaiting = deque()
        carsWaiting.append(deque((range(1, self.numCars+1))))
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

    def printDidNotCompetDirectly(self, res):
        cars =res['byCar']
        for c in cars:
            if len(cars[c]) > 0:
                print(str(c) + " did not compete against: ", end='')
                for ca in cars[c]:
                    print(str(ca) + ", ", end='')
                print('')
        print('total did not compete againt another: ' + str(res['totalCount']) + ' max: ' + str(res['max']) + ' backToBackCount:' + str(res['backToBackCount']))

    # car that do not race each other
    def didNotCompeteDirectly(self):
        carsByRows = []
        cars = {}
        for l in range(0, len(self.lanes)):
            for i in range(0, len(self.lanes[l])):
                carNum = self.lanes[l][i]
                if i +1 > len(carsByRows):
                    carsByRows.append([])
                carsByRows[i].append(carNum)

        for c in self.carsInRace:
            cars[c] = []
            for c2 in self.carsInRace:
                if not c == c2:
                    cars[c].append(c2)

        for c in cars:
            for r in carsByRows:
                if c in r:
                    for c2 in r:
                        if c2 in cars[c]:
                            cars[c].remove(c2)

        didNotCompete = {}
        byCar = {}
        totalCount = 0
        max = 0
        for c in cars:
            if len(cars[c]) > 0:
                byCar[c] = cars[c]
                total = 0
                for ca in cars[c]:
                    totalCount += 1
                    total +=1

                if total > max:
                    max = total

        didNotCompete['byCar'] = byCar
        didNotCompete['totalCount'] = totalCount
        didNotCompete['max'] = max

        #how many competed in previous race?
        backToBackCount = 0
        for r in range (1, len(carsByRows)):
            row1 = carsByRows[r-1]
            row2 = carsByRows[r]
            backToBackCount += len(set(row1) & set(row2))


        didNotCompete['backToBackCount'] = backToBackCount
        return didNotCompete


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
                                #print("could not find spots for: ")
                                #for q in curQ:
                                #    print(str(q))
                                return False
                    else:
                        pq = pq[1:] + pq[:1]

        return True




    def writeSchedule(self, updateExisting):
        file = open(self.fileName, 'w+')

        file.write('heat#, ')
        for i in range(1, self.numLanes + 1):
            file.write('car' + str(i) + '#, pos, time' + ', ')
        file.write('timestamp\n')

        start = 0
        if path.exists(self.fileName) and updateExisting:
            for r in self.prevSched.rows:
                if len(r[self.prevSched.headerToIndex['timestamp']]) > 2:
                    start += 1
                    for c in r:
                        if len(c) > 0:
                            file.write(c + ', ')
                    file.write('\n')

        for i in range(start, len(self.lanes[0])):
            file.write(str(i + 1) + ', ')
            for j in range(0, self.numLanes):
                if i < len(self.lanes[j]):
                    file.write(str(self.lanes[j][i]) + ', -, -,')
            file.write('-\n')

        file.close()

    def initLanes(self, updateExisting=False):
        self.lanes = []

        for i in range(0, self.numLanes):
            self.lanes.append([])

        cars = []
        if path.exists(self.fileName) and updateExisting:
            prevSched = CsvReader.CSVReader(self.fileName)

            carHeaders = ['car1#', 'car2#', 'car3#', 'car4#']
            for r in prevSched.rows:
                if len(r[prevSched.headerToIndex['timestamp']]) > 2:
                    for i in range(1,self.numLanes+1):
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

    def byDen(self, denName, updateExisting=False):
        denName = denName.lower().strip()

        self.carsInRace = []
        for r in self.reg.rows:
            if denName == r[self.reg.headerToIndex['den']].lower().strip() and r[self.reg.headerToIndex['checkedIn']].lower() == 'yes':
                carNum = int(r[self.reg.headerToIndex['carNum']])
                self.carsInRace.append((carNum))

        self.numCars = len(self.carsInRace)
        self.processCarList(updateExisting)

    def processCarList(self, updateExisting=False):
        if self.numCars == 3:
            self.numCars += 1
            self.carsInRace.append(0)

        if self.numCars < 3:
            a = self.carsInRace[0]
            b = 0
            if self.numCars > 1:
                b = self.carsInRace[1]
            self.lanes = [[a,0,0,b],[b,a,0,0],[0,b,a,0],[0,0,b,a]]
            self.writeSchedule(updateExisting)
            return

        found = False
        self.finalLanes = None
        self.bestLanes = None


        tries = 10
        if self.numCars > 3:
            tries = 500
        if self.numCars > 6:
            tries = 1000
        if self.numCars > 9:
            tries = 2000

        print('tries: ' + str(tries))
        for j in range(0,tries):
            if j % 1000 == 0:
                print('.', end='')
            usedCars = self.initLanes(updateExisting)

            carsWaiting = deque()
            carsCopy = self.carsInRace.copy()
            self.removeFromList(usedCars, carsCopy)
            carsWaiting.append(deque(carsCopy))
            for i in range(1, self.numLanes):
                carsCopy = self.carsInRace.copy()
                self.removeFromList(usedCars, carsCopy)
                carsWaiting.append(deque(random.sample(carsCopy, len(carsCopy))))

            if self.putWaitingCarsInLanes(carsWaiting):
                if self.finalLanes == None:
                    self.finalLanes = self.lanes
                    self.bestLanes = self.didNotCompeteDirectly()
                    print('placing cars attempt: ' + str(j))
                    self.printDidNotCompetDirectly(self.bestLanes)
                else:
                    res = self.didNotCompeteDirectly()
                    if res['max'] < self.bestLanes['max'] or \
                            (res['max'] == self.bestLanes['max'] and res['totalCount'] < self.bestLanes['totalCount']) or \
                            (res['backToBackCount'] < self.bestLanes['backToBackCount'] and res['max'] == self.bestLanes['max'] and res['totalCount'] == self.bestLanes['totalCount']):
                        self.finalLanes = self.lanes
                        self.bestLanes = res
                        print('placing cars: ' + str(j))
                        self.printDidNotCompetDirectly(res)



        self.lanes = self.finalLanes

        self.writeSchedule(updateExisting)

class scheduleGUI:
    def __init__(self, root):
        root.title("Schedule Generator")

        dens = []

        rowCount = 0
        columnCount = 0
        self.cbStateDen = dict()
        self.cbsDen = dict()
        self.cbStateScout = dict()
        self.cbsScout = dict()
        for r in rs.reg.rows:
            den = r[rs.reg.headerToIndex['den']].lower().strip()

            if den not in dens:
                dens.append(den)
                self.cbStateDen[den] = BooleanVar()
                self.cbStateDen[den].set(False)
                self.cbsDen[den] = Checkbutton(root, text=den, variable=self.cbStateDen[den], command=lambda d=den: self.denCallBack(d))
                rowCount = 0
                columnCount += 1
                self.cbsDen[den].grid(column=columnCount, row=rowCount)

                rowCount = 1




                for r2 in rs.reg.rows:
                    if den == r2[rs.reg.headerToIndex['den']].lower().strip() and r2[rs.reg.headerToIndex['checkedIn']].lower() == 'yes':
                        displayName = r2[rs.reg.headerToIndex['displayName']]
                        carNum = r2[rs.reg.headerToIndex['carNum']]
                        self.cbStateScout[carNum] = BooleanVar()
                        self.cbStateScout[carNum].set(False)
                        displayText = carNum + '_' + displayName
                        self.cbsScout[carNum] = Checkbutton(root, text=displayText, variable=self.cbStateScout[carNum],
                                                       command=self.scoutCallBack)
                        self.cbsScout[carNum].grid(column=columnCount, row=rowCount)
                        rowCount += 1



        self.createButton = Button(root, text="CREATE", command=self.createCallBack)
        self.createButton.grid(column=0, row=(rowCount + 1))

    def createCallBack(self):
        rs.carsInRace = []

        for r2 in rs.reg.rows:
            carNum = r2[rs.reg.headerToIndex['carNum']]
            if carNum in self.cbStateScout and self.cbStateScout[carNum].get():
                rs.carsInRace.append(int(carNum))

        rs.numCars = len(rs.carsInRace)
        rs.processCarList()


    def denCallBack(self, den):
        denState = self.cbStateDen[den].get()
        for r2 in rs.reg.rows:
            if den == r2[rs.reg.headerToIndex['den']].lower().strip() and r2[
                rs.reg.headerToIndex['checkedIn']].lower() == 'yes':
                carNum = r2[rs.reg.headerToIndex['carNum']]
                self.cbStateScout[carNum].set(denState)

        return

    def scoutCallBack(self):
        return


#if __name__ == "__main__":
numLanes = 4
rs = RaceSchedule('../csv/raceSchedule.csv', '../csv/registration.csv', numLanes)
#basic(numLanes, numCars)
#rs.byDen("Tiger")
#rs.byDen("Wolf")
#rs.byDen("Bear")
#rs.byDen("Webelos I")
#rs.byDen("Webelos II")

window = Tk()
tGui = scheduleGUI(window)
window.mainloop()
tGui.s.close()
tGui.file.close()