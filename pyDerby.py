from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask import jsonify
import os
from flask import send_from_directory
import statistics

app = Flask(__name__)

@app.route('/cars')
def index():
    data = []
    # other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options


    file = open('raceSchedule.csv', 'r')
    races = file.readlines()
    file.close()

    race = races[0].split(',')
    columns = [{'field': 'car#', 'title': 'car#', 'sortable': True},
               {'field': 'min', 'title': 'min', 'sortable': True},
               {'field': 'avg', 'title': 'avg', 'sortable': True},
               {'field': 'total', 'title': 'total', 'sortable': True},
               {'field': 'stdev', 'title': 'stdev', 'sortable': True}]
    header=[]
    count = 0
    for r in race:
        r = r.strip()
        header.append(r)
        if 'car' in r:
            count = count + 1
            columns.append({'field': 'race#' + str(count), 'title': 'race#', 'sortable': True})
            columns.append({'field': 'pos' + str(count), 'title': 'pos', 'sortable': True})
            columns.append({'field': 'time' + str(count), 'title': 'time', 'sortable': True})


    cars = {}
    carTimes = {}
    for race in races[1:]:
        race = race.split(',')
        curCar = 0
        count = 0
        curRace = 0;
        for i in range(len(race)):
            r = race[i]
            r= r.strip()
            if 'car' in header[i]:
                count = count + 1
                curCar = r
                if not r in cars:
                    cars[r] = {}
                cars[curCar].update({'race#' + str(count): curRace})
            if 'pos' in header[i]:
                cars[curCar].update({'pos' + str(count): r})
            if header[i] == 'time':
                try:
                    cars[curCar].update({'time' + str(count): r})
                    if curCar in carTimes:
                        carTimes[curCar].append(float(r))
                    else:
                        carTimes[curCar] = [float(r)]
                except ValueError:
                    pass
            if 'race' in header[i]:
                curRace = r

    places = [0]*4
    for c in cars:
        row = {'car#': c}
        row.update(cars[c])
        row['avg'] = "{:.3f}".format(statistics.mean(carTimes[c]))
        row['stdev'] = "{:.3f}".format(statistics.pstdev(carTimes[c]))
        row['total'] = "{:.3f}".format(sum(carTimes[c]))
        row['min'] = "{:.3f}".format(min(carTimes[c]))
        places[carTimes[c].index(min(carTimes[c]))] += 1
        data.append(row)

    print(places)

    return render_template("cars.html",
      data=data,
      columns=columns,
      title='Welcome to the Pinewood Derby!')

@app.route('/')
def homepage():
    file = open('raceSchedule.csv', 'r')
    races = file.readlines()
    file.close()

    table = []
    timeIndex = []
    fastestTimes = []
    for race in races:
        r = race.split(',')
        if 'time' in race:
            for i in range(len(r)):
                if 'time' in r[i] and not 'timestamp' in r[i]:
                    timeIndex.append(i)
                    fastestTimes.append(999999)
        elif '-' not in race:
            for i in range(len(timeIndex)):
                t = float(r[timeIndex[i]])
                if t < fastestTimes[i]:
                    fastestTimes[i] = t;

        map(str.strip, r)

        if len(table) > 0:
            for i in range(len(r)):
                if 'car' in table[0][i]:
                    r[i] = '<b>' + r[i] + '</b>'
        table.append(r)

    fastestTimesStr = 'Fastest times: '
    for f in range(len(fastestTimes)):
        if fastestTimes[f] < 999:
            fastestTimesStr = fastestTimesStr + ' Lane ' + str(f+1) + ': ' + "{:.3f}".format(fastestTimes[f])
    title = "Pinewood Derby"

    return render_template("index.html", title = title, table=table, fastestTime=fastestTimesStr)



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    Bootstrap(app)
    app.run(host='0.0.0.0')