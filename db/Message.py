from db.DbQuery import DBQuery

__author__ = 'kitru'

class Message(DBQuery):
    """ manage operations with messages in DB """

    def __init__(self, dbManager):
        super(Message, self).__init__(dbManager.getDb(), dbManager.getLogger())

    def setNew(self, text):
        """ return added message id
        can throw DbException """
        sql = "INSERT INTO `message` (`id`,`text`) VALUES (default, %(text)s)"
        args = {'text': text}
        return self.insert(sql, args)

    def getLastId(self):
        """ return last stored message id, if there is no return empty string
        can throw DbException """
        if self._getLastRow():
            return self._getLastRow()[0]

    def getLastMsg(self):
        """ return last stored message, if there is no return empty string
        can throw DbException """
        if self._getLastRow():
            return self._getLastRow()[1]
        else:
            return ""

    def _getLastRow(self):
        """ Last row is the newest message in DB
        can throw DbException """
        sql = "SELECT `id`,`text` FROM `message` ORDER BY `id` DESC LIMIT 1"
        return self.selectOne(sql)