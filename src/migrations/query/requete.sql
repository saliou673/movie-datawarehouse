-- 1. Affiche la liste des films de chaque pays par catégorie
select co.name as pays, c.name as category, count(m.id_movie) as nb_film,
        GROUPING(co.name,c.name) as groupin from facts f, category c, country co, movie m
        where f.id_movie=m.id_movie and f.id_country=co.id_country and m.id_category=c.id_category
        group by co.name, c.name with rollup;

-- 2. Le nombre de film par réalisateur
select w.name as realisateur, count(m.id_movie) as nbFilm 
from facts f, writer w, movie m
where f.id_writer=w.id_writer and f.id_movie=m.id_movie
group by w.name with rollup
order by count(m.id_movie) desc 
limit 20;

-- 3. Le nom et la date de naissance du réalisateur le plus jeune
select w.name, MAX(w.birthdate) as dateNaissance
from facts f, movie m, writer w 
where f.id_writer=w.id_writer and f.id_movie=m.id_movie;

--4. Top 10 des séries ayant le plus de saison
select m.title as Titre, f.number_of_seasons as nb_saisons
from facts f, movie m, category c 
where m.id_category = c.id_category and m.id_movie=f.id_movie and f.movie_type='tvshow'
order by f.number_of_seasons desc
limit 10;

--5 Nombre de film par catégorie et par langue
select co.language as langue, c.name as category, count(m.id_movie) as nb_film,
        GROUPING(co.language,c.name) as groupin from facts f, category c, country co, movie m
        where f.id_movie=m.id_movie and f.id_country=co.id_country and m.id_category=c.id_category
        group by co.language, c.name with rollup;

--6 Les films/series par langue et pays avec le total sur chaque langue.
select co.language, co.name, count(f.id_movie)
from facts f, movie m, country co
where f.id_movie=m.id_movie and f.id_country=co.id_country
group by co.language, co.name  with rollup;


--7 Durée total des films par pays et par plateforme de streaming avec le total sur chaque pays.
select c.name as nom, f.movie_source as source, sum(f.duration) as time 
from facts f, country c 
where f.id_country=c.id_country and movie_type='movie'
group by name,f.movie_source with rollup
order by sum(f.duration) desc;

--8 Nombre total de film et series par plateforme de streaming et par category.
select f.movie_source, c.name as categorie , count(c.id_category)
from facts f, movie m, category c
where f.id_movie=m.id_movie and m.id_category=c.id_category
group by f.movie_source, c.name with rollup;


