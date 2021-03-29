import mysql.connector as connector
from mysql.connector import Error
from core.logger import log
from config import databaseConfig

class Database:
    def __init__(self,):
        self.connect()
        log.info("Connected to server !")


    # Connect to the database
    def connect(self):
        try:
            self.connection = connector.connect(**databaseConfig)
        except Error as e:
            log.error("Error while connecting to MySQL", e)
    
    # Execute select query
    def execute (self, query, values):
        self.connect()
        cursor = self.connection.cursor().execute(query, values)
        if(cursor != None):
            cursor.close()

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
        