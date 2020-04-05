import sys
import glob
import serial
import logger


def serial_ports():
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


if __name__ == '__main__':
    log = logger.logger()

    file = open('serialPortLog.txt', 'w+')
    s = serial.Serial('/dev/tty.usbmodem14201')
    print(s.name)
    while True:
        l = str(s.readline())
        times = [0] * 4
        for u in l.split(' '):
            if '=' in u:
                vals = u.split('=')
                if 'A' in vals[0]:
                    times[0] = float(vals[1])
                if 'B' in vals[0]:
                    times[1] = float(vals[1])
                if 'C' in vals[0]:
                    times[2] = float(vals[1])
                if 'D' in vals[0]:
                    times[3] = float(vals[1])
                    log.logRace(times)
                    print(times)


        print(l)
        file.write(l)

    s.close()
    file.close()