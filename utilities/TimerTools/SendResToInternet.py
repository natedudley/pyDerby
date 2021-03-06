import os
import time
from google.cloud import firestore
from classes import ScheduleParser
from classes import Register


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/jennifedudley/PycharmProjects/pyDerby/keys/pack668-c79d7f783b7a.json"
schedFilePath = '../../csv/raceSchedule.csv'
regFilePath = '../../csv/registration.csv'
lastUpdate = 0

datastore_client = firestore.Client()

def addNames(res):
    for row in res['data']:
        for r in row:
            if 'car' in r:
                carNum = row[r]
                name = registration.getParticipantDisplayNameFromCar(carNum)
                info = name + ' (' + carNum + ')'
                row[r] = info

def addSortingOption(res):
    for col in res['columns']:
        col['sortable'] = True

while True:
    if not os.path.exists(schedFilePath):
        print('could not find: ' + schedFilePath + ' current working director: ' + os.getcwd())
        break
    try:
        moddate = os.stat(schedFilePath)[8]
        if moddate - lastUpdate > 1:
            sched = ScheduleParser.ScheduleParser(schedFilePath)
            registration = Register.Register(regFilePath)
            scheduleRes = sched.getBasicSchedule(True)
            carsRes = sched.getBasicCars(True)
            addNames(carsRes)
            addSortingOption(carsRes)
            #carsRes['data'] = sorted(carsRes['data'], key=lambda i: i['total'])

            curHeatRes = sched.CurrentHeat()

            key = datastore_client.collection('Derby').document('Schedule')
            key.set(scheduleRes)
            key = datastore_client.collection('Derby').document('Cars')
            key.set(carsRes)

            if len(curHeatRes['data']) > 0:
                addNames(curHeatRes)
                key = datastore_client.collection('Derby').document('CurrentHeat')
                key.set(curHeatRes)

            #doc = datastore_client.collection('Derby').document('Schedule')
            #test= doc.get().to_dict()

            print("updated")
            lastUpdate = moddate
    except Exception as e:
        print(e)




    print('.')
    time.sleep(3)