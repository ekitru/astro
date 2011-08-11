__author__ = 'kitru'


if __name__ == '__main__':
    import ephem

    print('yulian date is correct',ephem.julian_date())     #correct

    telescope = ephem.Observer()
    telescope.date = ephem.now()
    telescope.long =  ephem.degrees('26.46008849143982')
    telescope.lat = ephem.degrees('58.26574454393915')
    telescope.elevation = 320
    telescope.temp = 25;
    print('telescope time',telescope.date)
    print('local sidereal time',telescope.sidereal_time())  #correct
    print('UTC',ephem.now())
    print('local time', str(ephem.localtime(ephem.now())))

    star = ephem.star('Arcturus')
    star.compute(telescope)
    print(star.a_ra, star.a_dec)
    print(star.g_ra, star.g_dec)
    print(star.ra, star.dec)
    print(star.alt)

