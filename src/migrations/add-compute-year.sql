alter table movie add column year int(4) default null;
update movie set year=year(release_date);