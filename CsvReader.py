

class CSVReader:
    fileName = ""
    rows = []
    header = []

    def __init__(self, fileName):
        self.fileName = fileName
        file = open(fileName, 'r')
        lines = file.readlines()
        file.close()
        self.rows = []
        self.header = []

        for l in lines:
            vals = l.split((','))
            for i in range(len(vals)):
                vals[i] = vals[i].strip()

            self.rows.append(vals)

        if len(self.rows) > 0:
            self.header = self.rows[0]

        if len(self.rows) > 1:
            self.rows = self.rows[1:]

    def getHeader(self):
        return self.header

    def getRows(self):
        return self.rows

    def getColumnName(self, index):
        res = ''
        if index >= 0 and index < len(self.header):
            res = self.header[index]
        return res