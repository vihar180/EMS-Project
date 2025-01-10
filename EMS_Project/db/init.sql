CREATE DATABASE IF NOT EXISTS employees;
USE employees;
CREATE TABLE IF NOT EXISTS employees (
    employee_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    position VARCHAR(50),
    date_joined DATE,
    password VARCHAR(255)
);

