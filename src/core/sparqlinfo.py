import requests

def getTvShowInfo(title):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://dbpedia.org/sparql',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('default-graph-uri', 'http://dbpedia.org'),
        ('query', """SELECT distinct 
                    ?movie 
                    ?releaseDate (xsd:string(?countryIsoCode ) as ?countryIsoCode)
                    ?countryName
                    ?language
                    ?writterName
                    ?writterBirthDate
                    ?writterNationality
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
                        ?creator dbo:birthDate ?writterBirthDate;
                                 dbp:name ?writterName;
                                 dbp:nationality ?writterNationality.
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