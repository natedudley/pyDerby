from datetime import datetime
from pathlib import Path

class logger:
    def __init__(self, raceSchedulePath):
        self.raceSchedulePath = raceSchedulePath

    #for the input of list of times, returns list of 1st, 2nd, 3rd, etc. Index of list is the lane number
    def calcPlacement(self, times):
        res = [1] * len(times)
        for i in range(len(times) - 1):
            for j in range(i + 1, len(times)):
                if times[i] > times[j]:
                    res[i] = res[i] + 1
                elif times[i] < times[j]:
                    res[j] = res[j] + 1
        return res

    #takes the input of times from the timer and matches the times to the race Schedule, searchin for races that are not complete
    def logRace(self, times):
        places = self.calcPlacement(times)
        file = open(self.raceSchedulePath, 'r')
        races = file.readlines()
        file.close()

        newRes = []
        found = False
        for race in races:
            #"-" is the indicator that a heat has not been run in the schedule.
            if not found and "-" in race:
                found = True
                for t in range(len(times)):
                    race = race.replace("-", str(places[t]), 1)
                    race = race.replace("-", "{:.3f}".format(times[t]), 1)
                race = race.replace("-", datetime.now().strftime("%H:%M:%S"))
                newRes.append(race)
            else:
                newRes.append(race)

        file = open(self.raceSchedulePath, 'w+')
        file.writelines(newRes)
        file.close()

        Path('backup').mkdir(exist_ok=True)
        file = open('backup/raceSchedule'+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.csv', 'w+')
        file.writelines(newRes)
        file.close()