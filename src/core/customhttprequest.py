import requests

# Get countries from restcountries api and upload it
# in the database.
def uploadCountries(db):
    countries = requests.get("https://restcountries.eu/rest/v2/all").json()
    for country in countries:
        query = ("""INSERT IGNORE INTO country (name, alphacode, capital,
                region, language) VALUES(%s, %s, %s, %s, %s)""")
        value = (country['name'], country['alpha3Code'], country['capital'],
                    country['region'], country['languages'][0]['name'],)
        db.execute(query, value)