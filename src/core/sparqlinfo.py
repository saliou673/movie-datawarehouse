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
                        ?language
                        ?releaseDate
                        ?completionDate
                        ?country
                        ?numberOfEpisodes
                        ?numberOfSeasons 
                        (ceil(xsd:float(?completionDate-?releaseDate)/(24*60*60*365)) as ?shootingDuration) # en annee
                        (count(?principalActors) as ?nbPrincipalActors)
                        ?writer
                        ?writerName
                        ?writerBirthDate
                        ?writerBirthPlace
                        WHERE{
                            ?movie rdf:type dbo:TelevisionShow;
                                    dbp:name  \"""" + title + """\"@en;
                                    dbp:country ?country;
                                    dbo:numberOfEpisodes ?numberOfEpisodes;
                                    dbo:numberOfSeasons ?numberOfSeasons;
                                    dbp:starring ?principalActors;
                                    dbp:creator ?writer;
                                   dbp:language ?language
                            OPTIONAL {
                                    ?writer dbo:birthDate ?writerBirthDate;
                                                  dbp:name ?writerName;
                                                  dbp:birthPlace ?writerBirthPlace.
                            }.
                           OPTIONAL {?movie  dbo:completionDate ?completionDate;
                                             dbo:releaseDate ?releaseDate}
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
                        ?country
                        ?writer
                        ?writerName
                        ?writerBirthDate
                        ?writerBirthPlace
                        WHERE{

                        ?movie rdf:type dbo:Film;
                                    dbp:name  \"""" + title + """\"@en;
                                    dbo:runtime ?duration;
                                    dbp:gross ?benefice;
                                    dbo:starring  ?acteurs;
                                    dbp:language ?language;
                                    dbp:country ?country;
                                    dbo:writer ?writer.
                       OPTIONAL {
                                           ?writer dbp:birthDate ?writerBirthDate;
                                                       dbp:name  ?writerName;
                                                       dbp:birthPlace ?writerBirthPlace}.
                        OPTIONAL {?movie dbo:released ?releaseDate}.
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