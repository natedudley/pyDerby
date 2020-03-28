from datetime import datetime
from pathlib import Path

class logger:
    def __init__(self):
        a = 1

    def logRace(self, times):
        file = open('raceSchedule.csv', 'r')
        races = file.readlines()
        file.close()

        newRes = []
        found = False
        for race in races:
            if not found and "-" in race:
                found = True
                for time in times:
                    race = race.replace("-", str(time), 1)
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