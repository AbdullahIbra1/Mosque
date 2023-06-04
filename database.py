import sqlite3
from tkinter import *
class Db:
    def __init__(self,dbname,table):
        self.dbname=dbname
        self.table=table
        self.conn=sqlite3.connect(self.dbname)
        self.cur=self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS mosques
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         Type        CHAR(50),
         Address         TEXT   NOT NULL,
         Coordinate      TEXT   NOT NULL,
         IMAM_NAME       TEXT   NOT NULL);''')

    def Display_All(self):
        self.cur.execute("SELECT * from mosques ORDER BY ID ASC")
        data = self.cur.fetchall()
        return data
    def search(self,name):
        self.cur.execute("SELECT * from mosques where NAME=  ? ",(name,))
        data= self.cur.fetchall()
        self.conn.commit()
        return data
    
    def Insert(self,ID,name,type,address,coordinates,imam_name):
        
        self.cur.execute("INSERT INTO mosques VALUES (?,?,?,?,?,?)",(ID,name,type,address,coordinates,imam_name))
        self.conn.commit()

    def Delete(self,ID):
        self.cur.execute("DELETE FROM mosques WHERE ID = ?",(ID,))
        self.conn.commit()
    def update_Imam(self,imamname,name):
        self.cur.execute("UPDATE mosques SET IMAM_NAME = ? WHERE NAME = ? ",(imamname,name))
        self.conn.commit()
    def __del__(self):
        self.conn.close()
    
