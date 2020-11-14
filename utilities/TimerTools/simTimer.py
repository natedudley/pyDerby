import time
from random import random
from classes import logger
from classes import CsvReader

#simulator to play back an actual previous race for testing purposes
count = 40
timeBetweenRaces = 0.5

log = logger.logger()

sampleData = CsvReader.CSVReader('../../csv/sampleData.csv')

carsLanesTime = {}

#maps a previous race by car and lane. In the playback regardless of order, the cars get the same average and min time as in the origional race.
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

raceSchedule = CsvReader.CSVReader('../../csv/raceSchedule.csv')

for heat in raceSchedule.getRows():
    lanes = []
    for j in range(len(heat)):
        if 'car' in raceSchedule.getColumnName(j):
            lanes.append(heat[j])
    racesLanesCar.append(lanes)

#fileArduino is used to build an emulator of the real timer on an Arduino board to test the serial interfaces.
fileArduino = open('../../csv/arduinoSample.txt', 'w+')
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
