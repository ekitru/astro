from core.PLCManager import PLCManager

__author__ = 'kitru'


if __name__ == '__main__':
    plc = PLCManager()
    plc.test()
    number = float(1.23456789)
    plc.writeCoordinate(10, number)
    number = plc.readCoordinate(20)
    print(number)