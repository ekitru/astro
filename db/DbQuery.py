import threading
from Exceptions import DbException

class DBQuery(object):
    """ Simple db helper, makes easier data manipulations. Thread safe  """

    def __init__(self, db, logger):
        super(DBQuery, self).__init__()
        self._logger = logger
        self._db = db
        self.cursor = db.cursor()
        self._mutex = threading.RLock()

    def __del__(self):
        self.close()

    def selectOne(self, sql, args=None, where=None):
        with self._mutex:
            try:
                if where:
                    sql = sql + " WHERE " + where
                self.cursor.execute(sql, args)
                return self.cursor.fetchone()
            except Exception as error:
                raise DbException(error.args, self._logger)

    def selectAll(self, sql, args=None, where=None):
        with self._mutex:
            try:
                if where:
                    sql = sql + " WHERE " + where
                self.cursor.execute(sql, args)
                return self.cursor.fetchall()
            except Exception as error:
                raise DbException(error.args, self._logger)

    def insert(self, sql, args):
        """ Insert single row value
        Return: last row number  """
        with self._mutex:
            try:
                self.cursor.execute(sql, args)
                self._db.commit()
                return self.cursor.lastrowid
            except Exception as error:
                self._db.rollback()
                raise DbException(error.args, self._logger)

    def update(self, sql, args):
        with self._mutex:
            try:
                self.cursor.execute(sql, args)
                self._db.commit()
            except Exception as error:
                self._db.rollback()
                raise DbException(error.args, self._logger)

    def delete(self, sql, args):
        with self._mutex:
            try:
                self.cursor.execute(sql, args)
                self._db.commit()
            except Exception as error:
                self._db.rollback()
                raise DbException(error.args, self._logger)

    def close(self):
        """ Close cursor if not closed. Also will be called during object deleting """
        if self._db:
            self._logger.debug("Close cursor")
            self.cursor.close()
        else:
            self._logger.debug("Cursor already closed")