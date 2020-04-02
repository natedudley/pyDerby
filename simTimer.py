import time
from random import random

import logger
import CsvReader

count = 40
timeBetweenRaces = 1.5

log = logger.logger()

sampleData = CsvReader.CSVReader('sampleData.csv')

carsLanesTime = {}

for heat in sampleData.getRows():
    curCar = 0
    curRace = 0;
    lane = 0
    for i in range(len(heat)):
        r = heat[i]
        if 'car' in sampleData.getColumnName(i):
            lane = lane + 1
            curCar = r
            if not r in carsLanesTime:
                carsLanesTime[r] = {}
        if sampleData.getColumnName(i) == 'time':
            carsLanesTime[curCar].update({lane: float(r)})

racesLanesCar = []

raceSchedule = CsvReader.CSVReader('raceSchedule.csv')

for heat in raceSchedule.getRows():
    lanes = []
    for j in range(len(heat)):
        if 'car' in raceSchedule.getColumnName(j):
            lanes.append(heat[j])
    racesLanesCar.append(lanes)

for i in range(count):
    if i < len(racesLanesCar):
        times = []
        lane = 0
        for c in racesLanesCar[i]:
            lane += 1
            if c in carsLanesTime:
                times.append(carsLanesTime[c][lane])
            else:
                times.append(3+random())
        log.logRace(times)

    else:
        log.logRace([3+random(), 3+random(), 3+random(), 3+random()])
    print(i)
    time.sleep(timeBetweenRaces)

