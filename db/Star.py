from db.DbQuery import DBQuery
import astronomy

__author__ = 'kitru'

class Star(DBQuery):
    """ manage operations with stars in DB """

    def __init__(self, dbManager):
        super(Star, self).__init__(dbManager.getDb(), dbManager.getLog())

    def starExists(self, name):
        """ Check DB for record with same name """
        star = self.getStarByName(name)
        if star:
            return True
        else:
            return False

    def saveStar(self, name, ra, dec):
        """ Saves star object into database
        Attr:
             ra -  in string (hours:MIN:SEC)
             dec - in string (DEG:MIN:SEC)
        can throw DbException """
        ra, dec = astronomy.str2rad(str(ra), str(dec))
        sql = "INSERT INTO `star` (`id`,`name`,`ra`,`dec`) VALUES (default, %(name)s,%(ra)s,%(dec)s)"
        args = {'name': name, 'ra': float(ra), 'dec': float(dec)}
        self.insert(sql, args)

    def updateStar(self, name, ra, dec):
        """ Updates star object in database
        Attr:
             ra -  in string (hours:MIN:SEC)
             dec - in string (DEG:MIN:SEC)
         can throw DbException """
        ra, dec = astronomy.str2rad(str(ra), str(dec))
        sql = "update `star` set`ra`=%(ra)s, `dec`=%(dec)s WHERE `name`=%(name)s"
        args = {'name': name, 'ra': float(ra), 'dec': float(dec)}
        self.update(sql, args)

    def deleteStar(self, star):
        """Deletes star object from database
        Attr:
             ra -  in string (hours:MIN:SEC)
             dec - in string (DEG:MIN:SEC)
         can throw DbException """
        sql = "DELETE FROM `star` WHERE `name`=%(name)s"
        args = {'name': star['name']}
        self.delete(sql, args)

    def getStarByName(self, name):
        """ Take star from database by name
        return:
             Star name and position in suitable form for customer (: separated)
             If star does not exist, return None
        can throw DbException """
        sql = "SELECT `id`,`name`,`ra`,`dec` FROM `star` WHERE name=%(name)s"
        args = {'name': name}
        star = self.selectOne(sql, args)
        if star:
            return self.parseStar(star)
        else:
            return None

    def getStars(self, name):
        """ Returns list of star objects(name,ra,dec)
        Fetchs all rows with similar star name like name%
        Star name and position in suitable form for customer
        can throw DbException """
        stars = self.getStarsByPartName(name)
        resp = []
        for star in stars:
            resp.append(self.parseStar(star))
        return resp

    def getStarsByPartName(self, name):
        """ looks for all like name%   """
        name = name.encode('utf-8')
        sql = "SELECT `id`,`name`,`ra`,`dec` FROM `star` WHERE name LIKE %(name)s ORDER BY `name`  LIMIT 100"
        args = {'name': (name + '%')}
        return self.selectAll(sql, args)

    def parseStar(self, star):
        """ Convert row from DB into dictionary
        Attr:
          star - one record from DB
        Return:
           dic('id','name','ra','dec')
        """
        id = star[0]
        name = star[1]
        ra, dec = astronomy.rad2str(star[2], star[3])
        return {'id': id, 'name': name, 'ra': ra, 'dec': dec}
  