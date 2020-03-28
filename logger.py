from datetime import datetime
from pathlib import Path

class logger:
    def __init__(self):
        a = 1

    def calcPlacement(self, times):
        res = [1] * len(times)
        for i in range(len(times) - 1):
            for j in range(i + 1, len(times)):
                if times[i] > times[j]:
                    res[i] = res[i] + 1
                elif times[i] < times[j]:
                    res[j] = res[j] + 1
        return res

    def logRace(self, times):
        places = self.calcPlacement(times)
        file = open('raceSchedule.csv', 'r')
        races = file.readlines()
        file.close()

        newRes = []
        found = False
        for race in races:
            if not found and "-" in race:
                found = True
                for t in range(len(times)):
                    race = race.replace("-", str(places[t]), 1)
                    race = race.replace("-", "{:.3f}".format(times[t]), 1)
                race = race.replace("-", datetime.now().strftime("%H:%M:%S"))
                newRes.append(race)
            else:
                newRes.append(race)

        file = open('raceSchedule.csv', 'w+')
        file.writelines(newRes)
        file.close()

        Path('backup').mkdir(exist_ok=True)

        file = open('backup/raceSchedule'+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.csv', 'w+')
        file.writelines(newRes)
        file.close()