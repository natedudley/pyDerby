import statistics
from classes import CsvReader

class ScheduleParser:
    def __init__(self, fileName):
        self.raceSchedule = CsvReader.CSVReader(fileName)

    def computeCarStats(self):
        cars = {}
        carTimes = {}
        carPoints = {}
        for heat in self.raceSchedule.getRows():
            curCar = 0
            count = 0
            curHeat = 0;
            for i in range(len(heat)):
                h = heat[i]
                if 'car' in self.raceSchedule.getColumnName(i):
                    count = count + 1
                    curCar = h
                    if not h in cars:
                        cars[h] = {}
                    cars[curCar].update({'heat#' + str(count): curHeat})
                if 'pos' in self.raceSchedule.getColumnName(i):
                    try:
                        cars[curCar].update({'pos' + str(count): h})
                        if curCar in carPoints:
                            carPoints[curCar].append(float(h))
                        else:
                            carPoints[curCar] = [float(h)]
                    except ValueError:
                        pass
                if self.raceSchedule.getColumnName(i) == 'time':
                    try:
                        cars[curCar].update({'time' + str(count): h})
                        if curCar in carTimes:
                            carTimes[curCar].append(float(h))
                        else:
                            carTimes[curCar] = [float(h)]
                    except ValueError:
                        pass
                if 'heat' in self.raceSchedule.getColumnName(i):
                    curHeat = h

        for car in cars:
            if car in carTimes:
                cars[car]['avg'] = "{:.3f}".format(statistics.mean(carTimes[car]))
                cars[car]['stdev'] = "{:.3f}".format(statistics.pstdev(carTimes[car]))
                cars[car]['totalTime'] = "{:.3f}".format(sum(carTimes[car]))
                cars[car]['totalPoints'] = "{:.1f}".format(sum(carPoints[car]))
                cars[car]['min'] = "{:.3f}".format(min(carTimes[car]))

        return cars

    def getBasicSchedule(self, showTime = False):
        useCols = ['heat#', 'car1#', 'pos', 'car2#', 'pos', 'car3#', 'pos', 'car4#', 'pos']
        columns = []
        data = []
        posCount = 0
        indexesToFields = {}
        for h in range(0, len(self.raceSchedule.header)):
            if self.raceSchedule.header[h] in useCols:
                title = self.raceSchedule.header[h]
                field = title
                if field == 'pos':
                    posCount += 1
                    field += str(posCount)
                columns.append({'field': field, 'title': title})
                indexesToFields[h] = field


        for r in self.raceSchedule.rows:
            d = {}
            for i in indexesToFields:
                if 'car' in indexesToFields:
                    d[indexesToFields[i]] = '<b>' + str(r[i]) + '</b>'
                elif showTime and 'pos' in indexesToFields[i] and len(r[i+1]) > 2:
                    d[indexesToFields[i]] = r[i] + ' (' + r[i+1] + ')'
                else:
                    d[indexesToFields[i]] = r[i]


            data.append(d)

        res = {'data':data, 'columns':columns}
        return res

    def getBasicCars(self, showTime = False):
        cars = self.computeCarStats()
        useCols = ['car', 'pos', 'pos', 'pos', 'pos', 'totalPoints', 'totalTime']
        columns = []
        data = []
        posCount = 0
        for title in useCols:
            field = title
            if field == 'pos':
                posCount += 1
                field += str(posCount)
            columns.append({'field': field, 'title': title})

        for car in cars:
            d = {'car': car}
            carRes = cars[car]
            for c in columns:
                field = c['field']
                if field in carRes:
                    timeField = field.replace('pos', 'time')
                    if 'pos' in field and timeField in carRes and len(carRes[timeField]) > 2:
                        d[field] = carRes[field] + ' (' + carRes[timeField] + ')'
                    else:
                        d[field] = carRes[field]
            data.append(d)

        res = {'data': data, 'columns': columns}
        return res

    def CurrentHeat(self):
        useCols = ['heat#', 'car1#', 'car2#', 'car3#', 'car4#']
        columns = []
        data = []
        posCount = 0
        indexesToFields = {}
        for h in range(0, len(self.raceSchedule.header)):
            if self.raceSchedule.header[h] in useCols:
                title = self.raceSchedule.header[h]
                field = title
                if field == 'pos':
                    posCount += 1
                    field += str(posCount)
                columns.append({'field': field, 'title': title})
                indexesToFields[h] = field

        for r in self.raceSchedule.rows:
            d = {}
            for i in indexesToFields:
                if not 'car' in indexesToFields[i]:
                    d[indexesToFields[i]] = r[i]
                else:
                    d[indexesToFields[i]] = '' + str(r[i]) + ''
            if len(r[self.raceSchedule.headerToIndex['timestamp']]) < 3:
                data.append(d)
                break

        res = {'data': data, 'columns': columns}
        return res
