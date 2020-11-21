import sys
import glob
import serial
from tkinter import *
from tkinter.ttk import *
from classes import logger
import re
import datetime

class timerGUI:
    def __init__(self, root):
        self.log = logger.logger('../../csv/raceSchedule.csv')
        self.file = open('../../backup/serialPortLog.txt', 'a+')
        # you need to update the line below with your device, I use the Arduino serial monitor to figure out the name
        try:
            self.s = serial.Serial('/dev/cu.usbmodem14101')
        except:
            try:
                self.s = serial.Serial('/dev/cu.usbserial-1420')
            except:
                self.s = None
                print("No serial device connected")
        if not self.s == None:
            self.s.timeout = 0
            print(self.s.name)
        self.timesQ = []
        self.countDownTime = datetime.datetime.now()
        self.root = root
        root.title("Timer Control")
        self.textBoxes = []
        for i in range(0, 4):
            l = Label(root, text='lane ' + str(i + 1) + ':')
            t = Entry(root, width=5)
            t.grid(column=i, row=1)
            l.grid(column=i, row=0)
            self.textBoxes.append(t)

        self.rejectButton = Button(root, text="Reject", state=DISABLED, command=self.rejectCallBack)
        self.rejectButton.grid(column=0, row=4)
        self.holdButton = Button(root, text="Hold", state=DISABLED, command=self.holdCallBack)
        self.holdButton.grid(column=1, row=4)
        self.approveButton = Button(root, text="Approve", state=DISABLED, command=self.approveCallBack)
        self.approveButton.grid(column=2, row=4)
        if self.s == None:
            self.approveButton['state'] = 'normal'
        self.countDownLabel = Label(root)
        self.countDownLabel.grid(column=3, row=4)

        self.hold = True

    def rejectCallBack(self):
        self.hold = True
        self.rejectButton['state'] = 'disabled'
        self.approveButton['state'] = 'disabled'

        times = []
        for t in range(0, len(self.textBoxes)):
            times.append(float(self.textBoxes[t].get()))
            self.textBoxes[t].delete(0, 'end')

        print('rejected: ' + str(times[0]) + ', ' + str(times[1]) + ', ' + str(times[2]) + ', ' + str(times[3]))

    def holdCallBack(self):
        self.hold = True
        self.rejectButton['state']='normal'
        self.holdButton['state']='disabled'
        return

    def approveCallBack(self):
        self.hold = True
        self.rejectButton['state'] = 'disabled'
        if not self.s == None:
            self.approveButton['state'] = 'disabled'
        self.holdButton['state'] = 'disabled'
        times = []
        for t in range(0, len(self.textBoxes)):
            try:
                times.append(float(self.textBoxes[t].get()))
            except:
                times.append(0)

            self.textBoxes[t].delete(0, 'end')

        if times[0] > 0 or times[1] > 0 or times[2] > 0 or times[3] > 0:
            self.log.logRace(times)
            print('logged: ' + str(times[0]) + ', ' + str(times[1]) + ', ' + str(times[2]) + ', ' + str(times[3]))
        else:
            print('did not log: ' + str(times[0]) + ', ' + str(times[1]) + ', ' + str(times[2]) + ', ' + str(times[3]))

    def countDown(self):
        totalSeconds = (self.countDownTime - datetime.datetime.now()).total_seconds()
        if self.hold:
            self.countDownLabel['text'] = 'hold'
            self.countDownTime = datetime.datetime.now()
        else:
            if totalSeconds > 0:
                self.countDownLabel['text'] = str(round(totalSeconds))
            else:
                self.countDownLabel['text'] = '-'


        if totalSeconds > -3:
            window.after(1000, self.countDown)
        else:
            self.approveCallBack()

    def update(self):
        if self.s == None:
            return
        try:
            l = str(self.s.readline().decode())
            self.file.write(l)
            self.file.flush()

            times = [0] * 4
            if len(l) > 0:
                for u in l.split(' '):
                    if '=' in u:
                        vals = u.split('=')
                        val = float(re.sub("[^\d.]", "", vals[1]))
                        if 'A' in vals[0]:
                            times[0] = val
                        if 'B' in vals[0]:
                            times[1] = val
                        if 'C' in vals[0]:
                            times[2] = val
                        if 'D' in vals[0]:
                            times[3] = val
                            # if the timer is turned around, times need to be reversed here.
                            self.timesQ.append(times)
                            print('queue depth: ' + str(len(self.timesQ)) + ' with ' + str(times[0]) + ', ' + str(times[1]) + ', ' + str(times[2]) + ', ' + str(times[3]))
        except Exception as e:
            print(e)

        if len(self.timesQ) > 0:
            ready = True
            for tb in self.textBoxes:
                if len(tb.get()) > 0:
                    ready = False

            if ready:
                self.hold = False
                self.countDownTime = datetime.datetime.now() + datetime.timedelta(seconds=15)
                print('starting countdown')
                self.countDown()
                self.approveButton['state'] = 'normal'
                self.holdButton['state'] = 'normal'
                times = self.timesQ.pop(0)
                for t in range(0, len(times)):
                    self.textBoxes[t].delete(0, 'end')
                    self.textBoxes[t].insert(INSERT, str(times[t]))
        window.after(1000, self.update)

    # method to display available serial ports
    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            print('.')
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

window = Tk()
tGui = timerGUI(window)
tGui.update()
window.mainloop()
tGui.s.close()
tGui.file.close()



