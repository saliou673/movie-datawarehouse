import mysql.connector as connector
from mysql.connector import Error
class Database:
    def __init__(self, host='localhost', database='moviedb', username='saliou673', password='S@liou673'):
        try:
            connection = connector.connect(host=host,database=database, user=username, password=password)
            if connection.is_connected():
                self.connection = connection
                print("Connection reussie")
        except Error as e:
            print("Error while connecting to MySQL", e)