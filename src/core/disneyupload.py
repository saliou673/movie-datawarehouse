import os
from core.database import Database
from core.logger import log
import pandas  as pd
import numpy
import requests
from core.sparqlinfo import getTvShowInfo, getMovieInfo
from core.customhttprequest import uploadCountries
from core.utils import getCountryId, getCategoryId, normalizeGenre, splitAndReplace, insertMovie, insertTvShow, insertBaseMovie


def disneyUpload(filename, countries, db):
    netflixcols = ['type', 'title', 'genre']
    netflixdata = pd.read_csv(filename, usecols = netflixcols)
    
    netflixdata = netflixdata[netflixdata["genre"].notnull()]
    genreCols = netflixdata["genre"].unique()
    uniqueGenreCol = []
    for genre in genreCols:
        value = normalizeGenre(genre)
        uniqueGenreCol = numpy.append(uniqueGenreCol, value)
        
    uniqueGenreCol = numpy.unique(uniqueGenreCol)
    
    for genre in uniqueGenreCol:
        query = ("INSERT IGNORE INTO category (name) VALUES(%s)")
        value = (genre,)
        db.execute(query, value)

    # Load categories from database
    query = ("select id_category, name from category")
    categories = db.execute(query)
    categories = numpy.array(categories)

    movies = netflixdata.itertuples()
    found = 0
    notFound = 0
    for movie in movies:
        data = getTvShowInfo(movie.title)
        if(data is None):
            data = getMovieInfo(movie.title)
            if(data is None):
                notFound+=1
            else:
                found+=1
                query = ("select id_writer from writer where name=%s")
                writerName = ''
                writerBirthPlace = ''
                writerBirthDate = None
                if('writerName' not in data.keys()):
                    writerName = splitAndReplace(data['writer']['value'])
                else:
                    writerName =  data['writerName']['value']
                    writerBirthPlace = splitAndReplace(data['writerBirthPlace']['value'])
                    if(len(data['writerBirthDate']['value']) >= 10):
                        writerBirthDate = data['writerBirthDate']['value']

                values = (writerName, )
                response = db.execute(query, values)
                idWriter = -1
            
                if(response != []):
                    idWriter = response[0][0]
                else:
                    query = ("""INSERT INTO writer(name, birthDate, birthPlace)
                                VALUES(%s, %s, %s)""")
                    values = (writerName, writerBirthDate, writerBirthPlace)
                    db.execute(query, values)
                    idWriter = db.getLastInsertId()
                
                idCategory = getCategoryId(categories, normalizeGenre(movie.genre))
                print("<" + movie.genre + ">", "<" + normalizeGenre(movie.genre) + ">", idCategory)
                country = data['country']
                countryName = country['value']
                if(country['type'] != 'literal'):
                    countryName = splitAndReplace(countryName)


                print("********************************>>>>>>>>>>>< country = ", "<" + countryName + ">",len(countryName))
            
                if(countryName.strip() in ('U.S.', 'US', 'United States')):
                    countryName = 'United States of America'
                elif(countryName in ('United Kingdom', 'UK')):
                    countryName = 'United Kingdom of Great Britain and Northern'
                idCountry = getCountryId(countries, countryName)
                print("================++++++++> the id", idCountry, len(countryName), "<" + countryName + ">")
                if(idCountry == -1):
                    idCountry = 240

                releaseDate = None
                if('releaseDate' in data.keys()):
                    releaseDate = data['releaseDate']['value']

                idMovie = insertBaseMovie(movie.title, idCategory, db)

                values = (releaseDate, data['duration']['value'],
                            data['nbPrincipalActors']['value'], idWriter,
                            idCountry, idMovie, 'disneyplus','movie',)
                insertMovie(values, db)
            
        else: # tv show
            found+=1
            query = ("select id_writer from writer where name=%s")
            writerName = ''
            writerBirthPlace = ''
            writerBirthDate = None
            if('writerName' not in data.keys()):
                writerName = splitAndReplace(data['writer']['value'])
            else:
                writerName =  data['writerName']['value']
                writerBirthPlace = splitAndReplace(data['writerBirthPlace']['value'])
                if(len(data['writerBirthDate']['value']) >= 10):
                        writerBirthDate = data['writerBirthDate']['value']

            values = (writerName, )
            response = db.execute(query, values)
            idWriter = -1
            
            if(response != []):
                idWriter = response[0][0]
            else:
                query = ("""INSERT INTO writer(name, birthDate, birthPlace)
                            VALUES(%s, %s, %s)""")
                values = (writerName, writerBirthDate, writerBirthPlace)
                db.execute(query, values)
                idWriter = db.getLastInsertId()
            
            idCategory = getCategoryId(categories, normalizeGenre(movie.genre))
            country = data['country']
            countryName = country['value']
            if(country['type'] != 'literal'):
                countryName = splitAndReplace(countryName)
            
            if(countryName in ('U.S.', 'US', 'United States')):
                countryName = 'United States of America'
            elif(countryName in ('United Kingdom', 'UK')):
                countryName = 'United Kingdom of Great Britain and Northern'
            idCountry = getCountryId(countries, countryName)
            if(idCountry == -1):
                idCountry = 240

            releaseDate = None
            if('releaseDate' in data.keys()):
                releaseDate = data['releaseDate']['value']

            shootingDuration = None
            if('shootingDuration' in data.keys()):
                shootingDuration = data['shootingDuration']['value']
                    
            idMovie = insertBaseMovie(movie.title, idCategory, db)

            values = (releaseDate, shootingDuration, data['numberOfSeasons']['value'],
                        data['numberOfEpisodes']['value'], data['nbPrincipalActors']['value'],
                        idWriter,idCountry, idMovie, 'disneyplus','tvshow',)
            insertTvShow(values, db)
        
        print("=================================<  \"", movie.title, " \":", found,
        "found and ", notFound, " not found > =================")