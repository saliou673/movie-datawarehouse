import requests

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://dbpedia.org/sparql',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
}

def getTvShowInfo(title):
    params = (
        ('default-graph-uri', 'http://dbpedia.org'),
        ('query', """SELECT distinct 
                    ?movie 
                    ?releaseDate (xsd:string(?countryIsoCode ) as ?countryIsoCode)
                    ?countryName
                    ?language
                    ?writerName
                    ?writerBirthDate
                    (xsd:integer(?numberOfEpisodes) as ?numberOfEpisodes)
                    (xsd:integer(?numberOfSeasons) as ?numberOfSeasons)
                    (ceil(xsd:float(?completionDate-?releaseDate)/(24*60*60*365)) as ?shootingDuration) # en annee
                    ((?totalDuration * xsd:integer(?numberOfEpisodes)) as ?totalDuration)
                    (count(?principalActors) as ?nbPrincipalActors)
                    WHERE{
                        ?movie rdf:type dbo:TelevisionShow;
                                dbp:name \'""" + title + """\'@en;
                                dbo:releaseDate ?releaseDate;
                                dbo:completionDate ?completionDate;
                                dbo:country ?country;
                                dbo:numberOfEpisodes ?numberOfEpisodes;
                                dbo:numberOfSeasons ?numberOfSeasons;
                                dbp:starring ?principalActors;
                                dbo:runtime ?totalDuration;
                                dbo:creator ?creator.
                        ?country dbo:iso31661Code ?countryIsoCode;
                                dbp:conventionalLongName ?countryName;
                                dbp:languages ?languages.
                        ?languages dbp:name ?language.
                        ?creator dbo:birthDate ?writerBirthDate;
                                 dbp:name ?writerName;
                                 dbp:birthPlace ?birthPlace.
                        ?birthPlace dbp:pushpinLabel ?writerBirthPlace
                    }
                    LIMIT 1"""),
        ('format', 'application/sparql-results+json'),
        ('timeout', '30000'),
        ('signal_void', 'on'),
        ('signal_unconnected', 'on'),
    )

    response = requests.get('https://dbpedia.org/sparql', headers=headers, params=params)
    results = response.json()['results']['bindings']
    if(len(results) == 0):
        return None
    return results[0]


def getMovieInfo(title):
    params = (
        ('default-graph-uri', 'http://dbpedia.org'),
        ('query', """SELECT distinct 
                        ?movie 
                        ?language
                        ?duration # minutes
                        ?benefice
                        ?releaseDate
                        (count(?acteurs)  as ?nbPrincipalActors)
                        ?countryName
                        ?writerName
                        ?writerBirthDate
                        ?writerBirthPlace
                        WHERE{

                        ?movie rdf:type <http://dbpedia.org/ontology/Film>;
                                    dbp:name  \'""" + title + """\'@en;
                                    dbo:runtime ?duration;
                                    dbp:gross ?benefice;
                                    dbo:starring  ?acteurs;
                                    dbo:language ?langue;
                                    dbp:released ?releaseDate;
                                    dbp:country ?countryName;
                                    dbo:writer ?writer.
                        ?writer dbo:birthDate ?writerBirthDate;
                                    dbp:name  ?writerName;
                                    dbp:birthPlace ?writerBirthPlace.
                        ?langue foaf:name ?language.

                        }
                        LIMIT 1"""),
        ('format', 'application/sparql-results+json'),
        ('timeout', '30000'),
        ('signal_void', 'on'),
        ('signal_unconnected', 'on'),
    )

    response = requests.get('https://dbpedia.org/sparql', headers=headers, params=params)
    results = response.json()['results']['bindings']
    if(len(results) == 0):
        return None
    return results[0]