import os
from core.database import Database
from core.logger import log
import pandas  as pd
import numpy
import requests
from core.sparqlinfo import getTvShowInfo, getMovieInfo
from core.customhttprequest import uploadCountries
from core.primeupload import primeUpload
from core.netflixupload import nextflixUpload


db = Database()
"""
sqlDir = os.getcwd() + "/src/migrations/"

log.info("Database creation ...")
db.executeScriptFile(sqlDir + "create-database.sql")
log.info("Database created !")

# select the created database
db.selectDB('movie_warehouse')

log.info("Tables creation ...")
db.executeScriptFile(sqlDir + "create-tables.sql")
log.info("Tables created !")
#todo: uncomment
#Countries upload
uploadCountries(db)
"""

db.selectDB('movie_warehouse') # todo: remove it
query = ("select id_country, name from country")
countries = db.execute(query)
countries = numpy.array(countries)


datasetDir = os.getcwd() + "/src/datasets/"

#primeUpload(datasetDir + "primevideo.csv", countries, db)

nextflixUpload(datasetDir + "netflix.csv", countries, db)
