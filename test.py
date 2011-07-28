__author__ = 'kitru'

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

if __name__ == 'la__main__':
    try:
        #Connect to the slave
        master = modbus_tcp.TcpMaster(host="192.168.88.46")
        master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12))
        print master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12)


        master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 44, output_value=xrange(20))
        print master.execute(1, cst.READ_HOLDING_REGISTERS, 60,1)

    except modbus_tk.modbus.ModbusError, e:
        print "Modbus error ", e.get_exception_code()
        raise e

    except Exception, e2:
        print "Error ", str(e2)
        raise e2

if __name__ == '__main__':
    import ephem

    starRA = ephem.hours("12:00:00")
    starDEC= ephem.degrees("10:10:10")
    d = ephem.Equatorial(starRA, starDEC)
    print(d.ra,d.dec)

    epoch_date = ephem.Date(ephem.J2000)
    print(epoch_date.real)
    julian_epoch_date = ephem.julian_date(epoch_date)
    print(julian_epoch_date)

    print('yulian date is correct',ephem.julian_date())     #correct

    telescope = ephem.Observer()
    telescope.long =  ephem.degrees('26.46008849143982')
    telescope.lat = ephem.degrees('58.26574454393915')
    telescope.elevation = 200
    print(telescope.sidereal_time())  #correct

