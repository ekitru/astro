__author__ = 'kitru'

if __name__ == '__main__':
    import ephem

    print('yulian date is correct', ephem.julian_date())     #correct

    telescope = ephem.Observer()
    telescope.date = ephem.now()
    telescope.long = ephem.degrees('26.46008849143982')
    telescope.lat = ephem.degrees('58.26574454393915')
    telescope.elevation = 320
    telescope.temp = 25;
    print('telescope time', telescope.date)
    print('local sidereal time', telescope.sidereal_time())  #correct
    print('UTC', ephem.now())
    print('local time', str(ephem.localtime(ephem.now())))

    star = ephem.star('Arcturus')
    star.compute(telescope)
    print(star.a_ra, star.a_dec)
    print(star.g_ra, star.g_dec)
    print(star.ra, star.dec)
    print(star.alt)

    deg = ephem.degrees(2.231)
    e = str(deg)
    print('deg',deg.real)

    telescope2 = ephem.Observer()
    telescope2.long =  ephem.degrees('10')
    telescope2.lat = ephem.degrees('60')
    telescope2.elevation = 200

    radiant = ephem.FixedBody()
    radiant._ra = ephem.degrees('263.2')
    radiant._dec = ephem.degrees('55.8')
    radiant.compute(telescope2)

    print radiant.alt, radiant.az
    print(radiant.ra, radiant.dec )
