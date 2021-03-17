CREATE TABLE IF NOT EXISTS test1(
    id INT PRIMARY KEY,
    name varchar(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS test2(
    id INT PRIMARY KEY,
    name varchar(20) NOT NULL,
    test1_id INT REFERENCES test1(id)
)