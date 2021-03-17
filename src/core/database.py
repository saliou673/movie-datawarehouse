import mysql.connector as connector
from mysql.connector import Error
from core.logger import log
from config import databaseConfig

class Database:
    def __init__(self,):
        self.connect()
        log.info("Connected to server !")


    def connect(self):
        try:
            connection = connector.connect(**databaseConfig)
            if connection.is_connected():
                self.connection = connection
                self.cursor = connection.cursor()
        except Error as e:
            log.error("Error while connecting to MySQL", e)
    
    # Execute select query
    def query (self, query, parameters):
        return self.cursor.execute(query)

    #Execute SQL script
    def executeScriptFile(self, filename):
        sqlFile = open(filename)
        sqlString = sqlFile.read()
        self.cursor.execute(sqlString, multi=True)

    def selectDB(self, dbname):
        databaseConfig['database'] = dbname;
        self.connect()
        