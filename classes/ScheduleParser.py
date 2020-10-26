import statistics
from classes import CsvReader

class ScheduleParser:
    def __init__(self, fileName):
        self.raceSchedule = CsvReader.CSVReader(fileName)

    def computeCarStats(self):
        cars = {}
        carTimes = {}
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
                    cars[curCar].update({'pos' + str(count): h})
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
                cars[car]['total'] = "{:.3f}".format(sum(carTimes[car]))
                cars[car]['min'] = "{:.3f}".format(min(carTimes[car]))

        return cars

    def getBasicSchedule(self):
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
                if not 'car' in indexesToFields[i]:
                    d[indexesToFields[i]] = r[i]
                else:
                    d[indexesToFields[i]] = '<b>' + str(r[i]) + '</b>'

            data.append(d)

        res = {'data':data, 'columns':columns}
        return res

    def getBasicCars(self):
        cars = self.computeCarStats()
        useCols = ['car', 'pos', 'pos', 'pos', 'pos', 'total']
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
                    d[field] = carRes[field]
            data.append(d)

        res = {'data': data, 'columns': columns}
        return res
