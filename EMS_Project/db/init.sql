CREATE DATABASE IF NOT EXISTS employees;
USE employees;

CREATE TABLE employees (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    date_joined DATE NOT NULL,
    password VARCHAR(255) NOT NULL
);
