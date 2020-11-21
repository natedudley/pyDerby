import flask
from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
import os
from flask import send_from_directory
import statistics
import time

from classes import CsvReader
from classes import Register
from classes import ScheduleParser


app = Flask(__name__)

#registation is done here. There is a lock on registration.csv to make sure there are not multiple writes at the same time
registration = Register.Register('csv/registration.csv')
schedFilePath = './csv/raceSchedule.csv'

@app.route('/register', methods=['GET', 'POST'])
def register():
    print(flask.request.values)
    regId = -1
    name=""
    den=""
    carNum=""
    groups=['Lion', 'Tiger', 'Wolf', 'Webelos1', 'Webelos2', 'Adult']

    alerts = []
    #used to edit participant information
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
    #used to add a new participant
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

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    raceSchedule = CsvReader.CSVReader('csv/raceSchedule.csv')

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
                pass

    data = []
    columns = []

    colCount = {}
    for col in raceSchedule.getHeader():

        if 'car' in col:
            if not 'name' in colCount:
                colCount['name'] = 0
            else:
                colCount['name'] += 1

            columns.append(getTableColSettingsWithCookie('index', str(colCount['name'] + 1),
                                                         '<b>' + str(colCount['name'] + 1) + '</b>'))
            columns.append(getTableColSettingsWithCookie('index', 'name' + str(colCount['name']), 'name'))
            columns.append(getTableColSettingsWithCookie('index', 'result' + str(colCount['name']), 'result'))

        if not col in colCount:
            colCount[col] = 0
        else:
            colCount[col] += 1
        columns.append(getTableColSettingsWithCookie('index', col + str(colCount[col]), col))

    for heat in raceSchedule.getRows():
        heatInfo = {}
        colCount = {}
        curLane = 0
        curPos = ""
        for i in range(len(heat)):
            col = raceSchedule.getColumnName(i)
            if not col in colCount:
                colCount[col] = 0
            else:
                colCount[col] += 1

            heatInfo.update({col + str(colCount[col]): heat[i]})
            if 'car' in col:
                if not 'name' in colCount:
                    colCount['name'] = 0
                else:
                    colCount['name'] += 1
                curLane = colCount['name'] + 1
                heatInfo[str(curLane)] = '<b>' + str(curLane) + '</b>'

                participant = registration.getParticipantFromCar(heat[i])
                if len(participant) > 0:
                    heatInfo['name' + str(colCount['name'])] = participant['name'] + ' (' + participant['carNum'] + ')'
                else:
                    heatInfo['name' + str(colCount['name'])] = '?' + ' (' + heat[i] + ')'
            if 'pos' in col:
                curPos = heat[i]
            if 'time' == col:
                if '-' in curPos or curPos == ' ' or curPos == '':
                    result = '-'
                else:
                    result = curPos + ' <i>(' + heat[i] + ')</i>'
                heatInfo['result' + str(curLane - 1)] = result

        data.append(heatInfo)
    return jsonify(data)


@app.route('/api/cars', methods=['GET'])
def get_cars():

    sched = ScheduleParser.ScheduleParser(schedFilePath)
    carsRes = sched.computeCarStats()

    data = []
    for car in carsRes:
        row = {'car#': car}
        participant = registration.getParticipantFromCar(car)
        if len(participant) > 0:
            row['name'] = participant['name']
            row['den'] = participant['den']
        row.update(carsRes[car])
        data.append(row)

    return jsonify(data)

@app.route('/cars')
def cars():
    data = []

    # other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options

    raceSchedule = CsvReader.CSVReader('csv/raceSchedule.csv')

    columns = [getTableColSettingsWithCookie('cars', 'car#', 'car#'),
               getTableColSettingsWithCookie('cars', 'name', 'name'),
               getTableColSettingsWithCookie('cars', 'den', 'den'),
               getTableColSettingsWithCookie('cars', 'min', 'min'),
               getTableColSettingsWithCookie('cars', 'avg', 'avg'),
               getTableColSettingsWithCookie('cars', 'totalPoints', 'totalPoints'),
               getTableColSettingsWithCookie('cars', 'totalTime', 'totalTime'),
               getTableColSettingsWithCookie('cars', 'stdev', 'stdev')]

    count = 0
    for h in raceSchedule.getHeader():
        if 'car' in h:
            count = count + 1
            columns.append(getTableColSettingsWithCookie('cars', 'heat#' + str(count), 'heat#'))
            columns.append(getTableColSettingsWithCookie('cars', 'pos' + str(count), 'pos'))
            columns.append(getTableColSettingsWithCookie('cars', 'time' + str(count), 'time'))

    return render_template("cars.html",
      columns=columns,
      title='Welcome to the Pinewood Derby!')

@app.route('/')
def homepage():
    raceSchedule = CsvReader.CSVReader('csv/raceSchedule.csv')

    timeIndexes = []
    fastestTimes = []
    for i in range(0, len(raceSchedule.getHeader())):
        if 'time' in raceSchedule.getHeader()[i] and not 'timestamp' in raceSchedule.getHeader()[i]:
            timeIndexes.append(i)
            fastestTimes.append(999999)

    for heat in raceSchedule.getRows():
        for i in range(len(timeIndexes)):
            try:
                fastestTimes[i] = min(fastestTimes[i], float(heat[timeIndexes[i]]))
            except:
                pass

    fastestTimesStr = 'Fastest times: '
    for f in range(len(fastestTimes)):
        if fastestTimes[f] < 999:
            fastestTimesStr = fastestTimesStr + ' Lane ' + str(f+1) + ': ' + "{:.3f}".format(fastestTimes[f])

    columns = []

    colCount = {}
    for col in raceSchedule.getHeader():

        if 'car' in col:
            if not 'name' in colCount:
                colCount['name'] = 0
            else:
                colCount['name'] += 1

            columns.append(getTableColSettingsWithCookie('index', str(colCount['name'] + 1),
                                                         '<b>' + str(colCount['name'] + 1) + '</b>'))
            columns.append(getTableColSettingsWithCookie('index', 'name' + str(colCount['name']), 'name'))
            columns.append(getTableColSettingsWithCookie('index', 'result' + str(colCount['name']), 'result'))

        if not col in colCount:
            colCount[col] = 0
        else:
            colCount[col] += 1
        columns.append(getTableColSettingsWithCookie('index', col + str(colCount[col]), col))

    return render_template("index.html",
                           title = "Pinewood Derby",
                           columns=columns,
                           fastestTime=fastestTimesStr
                           )



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

#used to get save settings for which columns are turned on and off
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


if __name__ == "__main__":
    Bootstrap(app)
    app.run(host='0.0.0.0')