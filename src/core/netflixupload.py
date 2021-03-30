import os
from core.database import Database
from core.logger import log
import pandas  as pd
import numpy
import requests
from core.sparqlinfo import getTvShowInfo, getMovieInfo
from core.customhttprequest import uploadCountries
from core.utils import getCountryId, getCategoryId, normalizeGenre, splitAndReplace, insertMovie, insertTvShow

def mapNetflixToPrimeGenre(value):
    value = value.strip()
    if(value == 'dramas'):
        value = 'drama'
    elif (value == 'anime'):
        value = 'animation'
    elif (value == 'comedies'):
        value = 'comedy'
    elif (value == 'documentaries'):
        value = 'documentary'
    return value


def nextflixUpload(filename, countries, db):
    netflixcols = ['type', 'title', 'listed_in']
    netflixdata = pd.read_csv(filename, usecols = netflixcols)
    
    netflixdata = netflixdata[netflixdata["listed_in"].notnull()]
    genreCols = netflixdata["listed_in"].unique()
    uniqueGenreCol = []
    for genre in genreCols:
        value = normalizeGenre(genre)
        value = mapNetflixToPrimeGenre(value)
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
                
                idCategory = getCategoryId(categories, mapNetflixToPrimeGenre(normalizeGenre(movie.listed_in)))
                print("<" + movie.listed_in + ">", "<" + mapNetflixToPrimeGenre(normalizeGenre(movie.listed_in)) + ">", idCategory)
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

                values = (movie.title, releaseDate, data['duration']['value'],
                            data['nbPrincipalActors']['value'], idWriter,
                            idCountry, idCategory, 'netflix','movie',)
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
            
            idCategory = getCategoryId(categories, mapNetflixToPrimeGenre(normalizeGenre(movie.listed_in)))
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
                    
            query = ("""INSERT INTO movie (title, release_date, filming_time, 
                    number_of_seasons, number_of_episodes,
                    main_actor, id_writer, id_country, id_category,
                    movie_source, movie_type)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
            values = (movie.title, releaseDate, shootingDuration, data['numberOfSeasons']['value'],
                        data['numberOfEpisodes']['value'], data['nbPrincipalActors']['value'],
                        idWriter,idCountry, idCategory, 'netflix','tvshow',)
            insertTvShow(values, db)
        
        print("=================================<  \"", movie.title, " \":", found,
        "found and ", notFound, " not found > =================")