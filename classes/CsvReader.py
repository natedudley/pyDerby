import os.path
from os import path

class CSVReader:
    fileName = ""
    rows = []
    header = []

    def __init__(self, fileName):
        self.fileName = fileName

        if path.exists(fileName):
            file = open(fileName, 'r')
            lines = file.readlines()
            file.close()
        else:
            lines = []

        self.rows = []
        self.header = []

        for l in lines:
            vals = l.split((','))
            for i in range(len(vals)):
                vals[i] = vals[i].strip()


            self.rows.append(vals)

        self.headerToIndex = {}
        if len(self.rows) > 0:
            self.header = self.rows[0]
            for i in range(len(self.header)):
                self.headerToIndex[self.header[i]] = i

        if len(self.rows) > 0:
            self.rows = self.rows[1:]
        else:
            self.rows = []

    def getHeader(self):
        return self.header

    def getRows(self):
        return self.rows

    def getColumnName(self, index):
        res = ''
        if index >= 0 and index < len(self.header):
            res = self.header[index]
        return res

    def nameToIndex(self, name):
        res = -1;
        if name in self.headerToIndex:
            res = self.headerToIndex[name]
        return res