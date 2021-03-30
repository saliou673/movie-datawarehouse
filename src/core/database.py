import mysql.connector as connector
from mysql.connector import Error
from core.logger import log
from config import databaseConfig

class Database:
    def __init__(self,):
        self.connect()
        self.lastInsertId = -1
        log.info("Connected to server !")


    # Connect to the database
    def connect(self):
        try:
            self.connection = connector.connect(**databaseConfig)
        except Error as e:
            log.error("Error while connecting to MySQL", e)
    
    # Execute select query
    def execute (self, query, values=()):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        self.lastInsertId = cursor.lastrowid
        cursor.close()
        return result

    #Execute SQL script
    def executeScriptFile(self, filename):
        self.connect()
        sqlFile = open(filename)
        sqlString = sqlFile.read()
        cursor = self.connection.cursor().execute(sqlString, multi=True)
        cursor.close()

    # Select database
    def selectDB(self, dbname):
        databaseConfig['database'] = dbname
        self.connect()
    
    def getLastInsertId(self):
        return self.lastInsertId
        