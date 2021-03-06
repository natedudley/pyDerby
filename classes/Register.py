from threading import Lock
from datetime import datetime
from pathlib import Path
from classes import CsvReader

#Register reads the data from a text file and stores it in memory. Unlike the race schedule, the service needs a restart if you manually edit the registraton csv file
class Register:
    def __init__(self, fileName):
        self.fileName = fileName
        self.loc = Lock()
        #the csv file has to use these column names as the first row.
        self.cols = ['regId', 'name', 'displayName', 'carNum', 'den']

        #make sure no one else is using the file at the same time
        with self.loc:
            savedReg = CsvReader.CSVReader(fileName)

        self.regData = []
        self.regIDDict = {}
        self.carNumDict = {}

        for i in  range(len(savedReg.getRows())):
            r = savedReg.getRows()[i]
            participant = {}
            self.regIDDict[int(r[savedReg.nameToIndex('regId')])] = i
            self.carNumDict[r[savedReg.nameToIndex('carNum')]] = i
            for c in self.cols:
                index = savedReg.nameToIndex(c)
                if index >= 0:
                    participant[c] = r[index]
                    if 'regId' in c:
                        participant['edit'] = '<a href="/register?lookupRegId=' + participant['regId'] + '">edit</a>'
            self.regData.append(participant)

    def getParticipant(self, refId):
        if refId in self.regIDDict:
            return self.regData[self.regIDDict[refId]]
        return {}

    def getParticipantFromCar(self, carNum):
        if carNum in self.carNumDict:
            return self.regData[self.carNumDict[carNum]]
        return {}

    def getParticipantDisplayNameFromCar(self, carNumStr):
        part = self.getParticipantFromCar(carNumStr)
        if len(part) > 0:
            return part['displayName']

        return ''

    def addParticipant(self, args):
        res = []
        participant = {}
        participant['regId'] = int(args['regId'])
        participant['edit'] = '<a href="/register?lookupRegId='+ args['regId'] +'">edit</a>'
        participant['den'] = args['den']
        participant['carNum'] = args['carNum']
        if 'name' in args and len(args['name'].strip()) > 0:
            participant['name'] = args['name'].strip()
        else:
            return ['Name is missing']


        if len(participant['carNum']) < 1:
            return ['Car number is missing']

        if not participant['regId'] in self.regIDDict or self.regIDDict[participant['regId']] < 0:
            if participant['carNum'] in self.carNumDict:
                return ['Car number <b> ' + participant['carNum'] + '</b> is already in use']

            self.regIDDict[participant['regId']] = len(self.regData)
            self.carNumDict[participant['carNum']] = len(self.regData)
            self.regData.append(participant)
        else:
            i = self.regIDDict[participant['regId']]
            if participant['carNum'] != self.regData[i]['carNum']:
                if participant['carNum'] in self.carNumDict:
                    return ['Car number <b> ' + participant['carNum'] + '</b> is already in use']
                oldCarNum = self.regData[i]['carNum']
                self.regData[i]['carNum'] = participant['carNum']
                self.carNumDict.pop(oldCarNum)
                self.carNumDict[participant['carNum']] = i
            if participant['name'] != self.regData[i]['name']:
                self.regData[i]['name'] = participant['name']
            if participant['den'] != self.regData[i]['den']:
                self.regData[i]['den'] = participant['den']

        self.save()
        return res

    def uniqueDisplayName(self):
        displayNameCount ={}
        for i in range(len(self.regData)):
            firstName = self.regData[i]['name'].split(' ')[0]
            if firstName in displayNameCount:
                displayNameCount[firstName] += 1
            else:
                displayNameCount[firstName] = 1

        for i in range(len(self.regData)):
            names = self.regData[i]['name'].split(' ')
            firstName = names[0]
            lastName = ""
            if len(names) > 1:
                lastName = names[1]
            if firstName in displayNameCount and displayNameCount[firstName] > 1 and len(lastName) > 0:
                self.regData[i]['displayName'] = firstName + ' ' + lastName
            else:
                self.regData[i]['displayName'] = firstName

    def getNewRegId(self):
        res = 1
        if len(self.regIDDict) > 0:
            res = max(self.regIDDict, key=int) + 1
        self.regIDDict[res] = -1
        return res

    def getHtmlCols(self):
        columns = [{'field': 'edit', 'title': 'edit'},
                   {'field': 'regId', 'title': 'regId', 'visible': False, 'switchable': False},
                   {'field': 'name', 'title': 'name', 'sortable': True},
                   {'field': 'displayName', 'title': 'display name', 'sortable': True},
                   {'field': 'carNum', 'title': 'car#', 'sortable': True},
                   {'field': 'den', 'title': 'den', 'sortable': True}, ]
        return columns

    def getHtmlData(self):
        return self.regData

    def save(self):
        self.uniqueDisplayName()
        with self.loc:
            newPath = ''
            backupFile = 'backup/' + self.fileName + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            for p in range(len(backupFile.split('/')) - 1):
                newPath +=  backupFile.split('/')[p] + '/'
                Path(newPath).mkdir(exist_ok=True)

            file = open(self.fileName, 'w')
            fileBackup = open('backup/' + self.fileName + datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), 'w+')

            for c in self.cols:
                file.write(c + ', ')
                fileBackup.write(c + ', ')
            file.write('\n')
            fileBackup.write('\n')

            for d in self.regData:
                for c in self.cols:
                    file.write(str(d[c]) + ', ')
                    fileBackup.write(str(d[c]) + ', ')
                file.write('\n')
                fileBackup.write('\n')

            file.close()