import flask
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask import jsonify
import os
from flask import send_from_directory
import statistics
import CsvReader
import Register
from threading import Lock
import time

app = Flask(__name__)

registration = Register.Register('registration.csv')

@app.route('/register', methods=['GET', 'POST'])
def register():
    print(flask.request.values)
    regId = -1
    name=""
    den=""
    carNum=""
    groups=['Lion', 'Tiger', 'Wolf', 'Webelos 1', 'Webelos 2', 'Adult']

    alerts = []
    if 'lookupRegId' in flask.request.values:
        id = int(flask.request.values['lookupRegId'])
        res = registration.getParticipant(id)
        regId = id
        if 'name' in res:
            name = res['name']
        if 'carNum' in res:
            carNum = res['carNum']
        if 'den' in res:
            den = res['den']
    elif(len(flask.request.values)>0):
        alerts = registration.addParticipant(flask.request.values)
        if len(alerts) > 0:
            if 'regId' in flask.request.values:
                regId = int(flask.request.values['regId'])
            if 'name' in flask.request.values:
                name = flask.request.values['name']
            if 'carNum' in flask.request.values:
                carNum = flask.request.values['carNum']
            if 'den' in flask.request.values:
                den = flask.request.values['den']


    if regId < 0:
        regId = registration.getNewRegId()

    return render_template("register.html",
                           data=registration.getHtmlData(),
                           columns=registration.getHtmlCols(),
                           regId=regId,
                           name=name,
                           carNum=carNum,
                           den=den,
                           alerts=alerts,
                           groups=groups,
                           title='Welcome to the Pinewood Derby!')
@app.route('/cars')
def cars():
    if 'sleep' in flask.request.values:
        s = float(flask.request.values['sleep'])
        with lock:
            time.sleep(s)
    data = []
    # other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options

    raceSchedule = CsvReader.CSVReader('raceSchedule.csv')

    columns = [getTableColSettingsWithCookie('cars', 'car#', 'car#'),
               getTableColSettingsWithCookie('cars', 'min', 'min'),
               getTableColSettingsWithCookie('cars', 'avg', 'avg'),
               getTableColSettingsWithCookie('cars', 'total', 'total'),
               getTableColSettingsWithCookie('cars', 'stdev', 'stdev')]

    count = 0
    for h in raceSchedule.getHeader():
        if 'car' in h:
            count = count + 1
            columns.append(getTableColSettingsWithCookie('cars', 'heat#' + str(count), 'heat#'))
            columns.append(getTableColSettingsWithCookie('cars', 'pos' + str(count), 'pos'))
            columns.append(getTableColSettingsWithCookie('cars', 'time' + str(count), 'time'))


    cars = {}
    carTimes = {}
    for heat in raceSchedule.getRows():
        curCar = 0
        count = 0
        curHeat = 0;
        for i in range(len(heat)):
            h = heat[i]
            if 'car' in raceSchedule.getColumnName(i):
                count = count + 1
                curCar = h
                if not h in cars:
                    cars[h] = {}
                cars[curCar].update({'heat#' + str(count): curHeat})
            if 'pos' in raceSchedule.getColumnName(i):
                cars[curCar].update({'pos' + str(count): h})
            if raceSchedule.getColumnName(i) == 'time':
                try:
                    cars[curCar].update({'time' + str(count): h})
                    if curCar in carTimes:
                        carTimes[curCar].append(float(h))
                    else:
                        carTimes[curCar] = [float(h)]
                except ValueError:
                    pass
            if 'heat' in raceSchedule.getColumnName(i):
                curHeat = h

    for car in cars:
        row = {'car#': car}
        row.update(cars[car])
        if car in carTimes:
            row['avg'] = "{:.3f}".format(statistics.mean(carTimes[car]))
            row['stdev'] = "{:.3f}".format(statistics.pstdev(carTimes[car]))
            row['total'] = "{:.3f}".format(sum(carTimes[car]))
            row['min'] = "{:.3f}".format(min(carTimes[car]))

        data.append(row)



    return render_template("cars.html",
      data=data,
      columns=columns,
      title='Welcome to the Pinewood Derby!')

@app.route('/')
def homepage():
    raceSchedule = CsvReader.CSVReader('raceSchedule.csv')

    timeIndex = []
    fastestTimes = []

    i = 0
    for col in raceSchedule.getHeader():
        if 'time' in col and not 'timestamp' in col:
            timeIndex.append(i)
            fastestTimes.append(999999)
        i += 1

    for heat in raceSchedule.getRows():
        for i in range(len(timeIndex)):
            try:
                fastestTimes[i] = min(fastestTimes[i], float(heat[timeIndex[i]]))
            except:
                print("An exception occurred")

    data = []
    columns = []

    colCount = {}
    for col in raceSchedule.getHeader():
        if not col in colCount:
            colCount[col] = 0
        else:
            colCount[col] += 1
        columns.append(getTableColSettingsWithCookie('index', col + str(colCount[col]), col))

    for heat in raceSchedule.getRows():
        heatInfo = {}
        colCount = {}
        for i in range(len(heat)):
            col = raceSchedule.getColumnName(i)
            if not col in colCount:
                colCount[col] = 0
            else:
                colCount[col] += 1

            heatInfo.update({col+str(colCount[col]): heat[i]})
        data.append(heatInfo)

    fastestTimesStr = 'Fastest times: '
    for f in range(len(fastestTimes)):
        if fastestTimes[f] < 999:
            fastestTimesStr = fastestTimesStr + ' Lane ' + str(f+1) + ': ' + "{:.3f}".format(fastestTimes[f])

    return render_template("index.html",
                           title = "Pinewood Derby",
                           data=data,
                           columns=columns,
                           fastestTime=fastestTimesStr
                           )



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

def getTableColSettingsWithCookie(pageId, field, title):
    res = {}
    vis = True

    cookieName = pageId + 'ColVis' + field
    if cookieName in flask.request.cookies and 'false' in flask.request.cookies.get(cookieName):
        vis = False
    cookieName = pageId + 'ColSort' + field


    res['field'] =  field
    res['title'] = title
    res['sortable'] = True
    if not vis:
        res['visible'] = False
    res.update()
    return res
    #columns = [{'field': 'car#', 'title': 'car#', 'sortable': True, 'visible': carnumVis},


if __name__ == "__main__":
    Bootstrap(app)
    app.run(host='0.0.0.0')