-- 2. Le nombre de film par réalisateur
select w.name, count(m.id_movie) as nbFilm 
from writer w, movie m where m.id_writer=w.id_writer
group by w.name with rollup
order by count(m.id_movie) desc 
limit 20;