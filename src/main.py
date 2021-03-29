import os
from core.database import Database
from core.logger import log
import pandas  as pd
import numpy
import requests
from core.sparqlinfo import getTvShowInfo, getMovieInfo


db = Database()

sqlDir = os.getcwd() + "/src/migrations/"

log.info("Database creation ...")
db.executeScriptFile(sqlDir + "create-database.sql")
log.info("Database created !")

# select the created database
db.selectDB('movie_warehouse')

log.info("Tables creation ...")
db.executeScriptFile(sqlDir + "create-tables.sql")
log.info("Tables created !")

def normalizeGenre(genre):
    return genre.strip().split(',')[0].split(' ')[0].lower()
datasetDir = os.getcwd() + "/src/datasets/"

primecols = ['Name of the show', 'Year of release', 'Language', 'Genre', 'No of seasons available']
primedata = pd.read_csv(datasetDir + "primevideo.csv", usecols = primecols)
primedata = primedata.rename(columns= {
                                        'Name of the show': 'title',
                                        'Year of release': 'yearOfRelease',
                                        'Language':'language',
                                        'Genre': 'genre',
                                        'No of seasons available':'nbSeason'})
primedata = primedata[primedata["genre"].notnull()]
genreCols = primedata["genre"].unique()
uniqueGenreCol = []
for genre in genreCols:
    value = normalizeGenre(genre)
    uniqueGenreCol = numpy.append(uniqueGenreCol, value)
    
uniqueGenreCol = numpy.unique(uniqueGenreCol)

for genre in uniqueGenreCol:
    query = ("INSERT IGNORE INTO category (name) VALUES(%s)")
    value = (genre,)
    db.execute(query, value)

movies = primedata.itertuples()
# for movie in movies:
#     print(movie.nbSeason)

# print(getTvShowInfo('Major Crimes'))
print(getMovieInfo('Lifeline'))
