import os
from core.database import Database
from core.logger import log
import pandas  as pd
import plotly.express as px
import numpy
import requests
from core.sparqlinfo import getTvShowInfo, getMovieInfo
from core.customhttprequest import uploadCountries
from core.primeupload import primeUpload
from core.netflixupload import nextflixUpload
from core.disneyupload import disneyUpload


db = Database()
sqlDir = os.getcwd() + "/src/migrations/"

log.info("Database creation ...")
db.executeScriptFile(sqlDir + "create-database.sql")
log.info("Database created !")

# select the created database
db.selectDB('movie_warehouse2')

log.info("Tables creation ...")
db.executeScriptFile(sqlDir + "create-tables.sql")
log.info("Tables created !")


#Countries upload
uploadCountries(db)

query = ("select id_country, name from country")
countries = db.execute(query)
countries = numpy.array(countries)


datasetDir = os.getcwd() + "/src/datasets/"

primeUpload(datasetDir + "primevideo.csv", countries, db)

nextflixUpload(datasetDir + "netflix.csv", countries, db)
disneyUpload(datasetDir + "disneyplus.csv", countries, db)

# Add and compute year  column on movie.
db.executeScriptFile(sqlDir + "add-compute-year.sql")



query =("""
select co.name as pays, c.name as 'category', count(m.id_movie) as nb_film,
        GROUPING(co.name,c.name) as groupin from category c, country co, movie m
        where m.id_country=co.id_country and m.id_category=c.id_category
        group by co.name, c.name with rollup;
""")

query = """select count(c.id_category) as category, c.name as name from movie m, category c, country co where 
            m.id_category=c.id_category and m.id_country=co.id_country 
            and co.name='United Kingdom of Great Britain and Northern'
            group by c.name
            order by count(c.id_category) desc"""
df = pd.read_sql(query, db.connection)
fig = px.histogram(df, x="category", color="name")
fig.show()
print("The results", df)
