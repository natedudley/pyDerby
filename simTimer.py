import time
from random import random

import logger
import CsvReader

count = 40
timeBetweenRaces = 0.5

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

fileArduino = open('arduinoSample.txt', 'w+')
stringArrayArduino = "const char *const string_table[] PROGMEM = {"
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
        fileArduino.write('const char string_'+str(i)+'[] PROGMEM = \"A='+str(times[0]) +'  B=' + str(times[1]) + '  C=' + str(times[2]) + '  D=' + str(times[3]) + '  E=0.000 F=0.000\";\n')
        stringArrayArduino += 'string_' + str(i) + ', '

    else:
        log.logRace([3+random(), 3+random(), 3+random(), 3+random()])
    print(i)
    time.sleep(timeBetweenRaces)
stringArrayArduino += "};\n"
fileArduino.write(stringArrayArduino)
fileArduino.close()
