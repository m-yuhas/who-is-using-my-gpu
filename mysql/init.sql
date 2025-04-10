CREATE USER 'foo' IDENTIFIED BY 'bar';


CREATE DATABASE IF NOT EXISTS gpustats;
USE gpustats;

CREATE TABLE IF NOT EXISTS gpustats(
    timestamp TIMESTAMP,
    hostname VARCHAR(16),
    gpuid INTEGER,
    type VARCHAR(32),
	fanspeed INTEGER,
	temperature INTEGER,
	mode INTEGER,
	powerused INTEGER,
	powertotal INTEGER,
	memoryused INTEGER,
	memorytotal INTEGER,
	procs JSON
);

GRANT SELECT, INSERT ON gpustats.gpustats TO 'foo'@'%';

