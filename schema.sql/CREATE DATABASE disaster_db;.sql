CREATE DATABASE disaster_db;

-- Run below AFTER connecting to disaster_db

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
    status VARCHAR DEFAULT 'pending'
);

INSERT INTO users(name,email,password,role)
VALUES('Admin','admin@gmail.com','admin123','admin');

INSERT INTO resources(name,quantity)
VALUES('Food',100),('Water',200);