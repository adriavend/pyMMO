__author__ = 'Adrian'

import sqlite3 as lite
import sys

class DbController:

    def __init__(self):
        self.STATEMENT_CREATE_TABLE_PLAYER = "CREATE TABLE IF NOT EXISTS Player(Id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                                             "Nickname TEXT NOT NULL, Password TEXT NOT NULL, Map INT, X INT, Y INT)"
        self.con = self.connection()
        self.init()

    def connection(self):
        try:
            conn = lite.connect('dbmmo.db')
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        return conn

    def get_cursor(self):
        return self.con.cursor()

    def init(self):
        with self.con:
            cur = self.get_cursor()
            cur.execute(self.STATEMENT_CREATE_TABLE_PLAYER)
            # cur.execute("INSERT INTO Player(Nickname, Password, Map, X, Y) VALUES('adrian', 'adrian', 1, 0, 0)")
            # self.con.commit()

    def insert(self, nickname, password, map, x, y):
        pass

    def retriev(self, nickname, password):
        cur = self.get_cursor()
        cur.execute("SELECT Id, Map FROM Player WHERE Nickname = ? AND Password = ?", (nickname, password))
        row = cur.fetchone() #Devuelve una sola fila.

        if row == None:
            return 0

        return (int(row[0]), int(row[1]))


# db = DbController()
# print db.retriev("adrian", "adrian")

# print "exito"