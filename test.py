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

    print('yulian date is correct',ephem.julian_date())     #correct

    telescope = ephem.Observer()
    telescope.date = ephem.now()
    telescope.long =  ephem.degrees('26.46008849143982')
    telescope.lat = ephem.degrees('58.26574454393915')
    telescope.elevation = 320
    telescope.temp = 25;


    print('telescope',telescope)
    print('local sidereal time',telescope.sidereal_time())  #correct

    star = ephem.star('Arcturus')
    star.compute(telescope)
    print(star.a_ra, star.a_dec)
    print(star.g_ra, star.g_dec)
    print(star.ra, star.dec)
    print(star.alt)

