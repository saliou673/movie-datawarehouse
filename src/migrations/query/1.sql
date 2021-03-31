-- 1. Affiche la liste des films de chaque pays par catégorie
select co.name as pays, c.name as 'category', count(m.id_movie) as nb_film,
        GROUPING(co.name,c.name) as groupin from category c, country co, movie m
        where m.id_country=co.id_country and m.id_category=c.id_category
        group by co.name, c.name with rollup;