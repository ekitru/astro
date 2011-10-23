from core.PLCManager import PLCManager

__author__ = 'kitru'


if __name__ == '__main__':
    plc = PLCManager()
    plc.test()
#    plc.writeNumber32bit(100, 5)
#    number = plc.readNumber32bit(100)

    number = float(-1.23456789)
    plc.writeCoordinate(100, number)
    number = plc.readCoordinate(100)
    print('number',number)
