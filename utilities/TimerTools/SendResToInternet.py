import os
import time
from google.cloud import firestore
from classes import ScheduleParser


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/jennifedudley/PycharmProjects/pyDerby/keys/pack668-c79d7f783b7a.json"
filePath = '../../csv/raceSchedule.csv'
lastUpdate = 0

datastore_client = firestore.Client()

while True:
    if not os.path.exists(filePath):
        print('could not find: ' + filePath + ' current working director: ' + os.getcwd())
        break
    try:
        moddate = os.stat(filePath)[8]
        if moddate - lastUpdate > 1:
            sched = ScheduleParser.ScheduleParser(filePath)
            scheduleRes = sched.getBasicSchedule()
            carsRes = sched.getBasicCars()

            key = datastore_client.collection('Derby').document('Schedule')
            key.set(scheduleRes)
            key = datastore_client.collection('Derby').document('Cars')
            key.set(carsRes)

            doc = datastore_client.collection('Derby').document('Schedule')
            test= doc.get().to_dict()

            print("updated")
            lastUpdate = moddate
    except Exception as e:
        print(e)




    print('.')
    time.sleep(3)