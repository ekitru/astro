from configuration import ConfigurationException, getDbConnection, getConfigFromFile

__author__ = 'kitru'

if __name__ == '__main__':
    try:
        config = getConfigFromFile("default.cnf")
        db = getDbConnection(config)
        cursor = db.cursor()
        cursor.execute('select version()')
        row = cursor.fetchone()
        print(row)
    except ConfigurationException as ce:
        print("Error during configuratino occure:"+ce.__str__())
    except Exception:
        print("Unexcepted error occur")

    pass
  