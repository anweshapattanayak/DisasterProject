DROP TABLE IF EXISTS requests CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS resources CASCADE;
DROP TABLE IF EXISTS disasters CASCADE;
DROP TABLE IF EXISTS volunteers CASCADE;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    email VARCHAR UNIQUE,
    password VARCHAR,
    role VARCHAR
);

CREATE TABLE resources(
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    quantity INT
);

CREATE TABLE requests(
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    resource_id INT REFERENCES resources(id),
    quantity INT,
    priority VARCHAR,
    status VARCHAR DEFAULT 'pending',
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE disasters(
    id SERIAL PRIMARY KEY,
    location VARCHAR,
    type VARCHAR,
    severity VARCHAR
);

CREATE TABLE volunteers(
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    skill VARCHAR,
    status VARCHAR DEFAULT 'available'
);

INSERT INTO users(name,email,password,role)
VALUES('Admin','admin@gmail.com','admin123','admin');

INSERT INTO resources(name,quantity)
VALUES('Food',100),('Water',200),('Medicine',150);