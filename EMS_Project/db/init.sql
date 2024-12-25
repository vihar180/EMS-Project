CREATE TABLE employees (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    position VARCHAR(255),
    date_joined DATE,
    password VARCHAR(255) NOT NULL
);
