CREATE DATABASE orangedb;

USE orangedb;

CREATE TABLE delay (
    ID int NOT NULL AUTO_INCREMENT,
    source_ip varchar(20),
    destination_ip varchar(20),
    metric float,
    PRIMARY KEY (ID)
);

CREATE TABLE rtt (
    ID int NOT NULL AUTO_INCREMENT,
    source_ip varchar(20),
    destination_ip varchar(20),
    metric float,
    PRIMARY KEY (ID)
);

CREATE USER 'admin'@'localhost' IDENTIFIED BY 'homework5';
CREATE USER 'admin'@'%' IDENTIFIED BY 'homework5';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
