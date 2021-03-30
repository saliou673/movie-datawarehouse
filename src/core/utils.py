
#Get country id from array.
def getCountryId(countries, name):
    for country in countries:
        if(country[1].strip().lower() == name.lower()):
            return country[0]

    return -1

#Get country id from array.
def getCategoryId(categories, name):
    for category in categories:
        if(category[1].lower() == name.lower()):
            return category[0]

    return -1

def normalizeGenre(genre):
    return genre.strip().split(',')[0].split(' ')[0].lower()


# Get the last part of a uri and replace underscore by space.
def splitAndReplace(value):
    arr = value.split('/')
    return arr[len(arr) - 1].replace("_", " ")

def insertMovie(values, db):
    query = ("""INSERT INTO movie(title, release_date, duration, main_actor,
                id_writer, id_country, id_category, movie_source, movie_type) 
                VALUES(%s, %s,%s,%s,%s,%s,%s, %s, %s)""")
   
    db.execute(query, values)

def insertTvShow(values, db):
    query = ("""INSERT INTO movie (title, release_date, filming_time, 
                number_of_seasons, number_of_episodes,
                main_actor, id_writer, id_country, id_category,
                movie_source, movie_type)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

    db.execute(query, values)
