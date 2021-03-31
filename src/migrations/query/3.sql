--3. Le nom du film fait par le réalisateur le plus jeune
select w.name, title, MAX(w.birthdate) from movie m, writer w where m.id_writer=w.id_writer;