import time
from random import random

import logger

count = 40
timeBetweenRaces = 3

log = logger.logger()

file = open('sampleData.csv', 'r')
races = file.readlines()
file.close()

carsLanesTime = {}
race = races[0].split(',')
header = []

for r in race:
    r = r.strip()
    header.append(r)

for race in races[1:]:
    race = race.split(',')
    curCar = 0
    curRace = 0;
    lane = 0
    for i in range(len(race)):
        r = race[i]
        r = r.strip()
        if 'car' in header[i]:
            lane = lane + 1
            curCar = r
            if not r in carsLanesTime:
                carsLanesTime[r] = {}
        if header[i] == 'time':
            carsLanesTime[curCar].update({lane: float(r)})

racesLanesCar = []
header = []
file = open('raceSchedule.csv', 'r')
races = file.readlines()
file.close()

race = races[0].split(',')
for r in race:
    header.append(r.strip())

for race in races[1:]:
    r = race.split(',')
    lanes = []
    for j in range(len(r)):
        if 'car' in header[j]:
            lanes.append((r[j].strip()))
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

