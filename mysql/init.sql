DELETE FROM mysql.user WHERE user='root' AND host='%';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS gpu_db;
USE gpu_db;

CREATE TABLE IF NOT EXISTS gpu_stats(
  timestamp TIMESTAMP,
  hostname VARCHAR(16),
  id INTEGER,
  type VARCHAR(32),
  fan_speed INTEGER,
  temperature INTEGER,
  mode INTEGER,
  power_used INTEGER,
  power_total INTEGER,
  memory_used INTEGER,
  memory_total INTEGER,
  procs JSON
);

CREATE TABLE IF NOT EXISTS errors(
  timestamp TIMESTAMP,
  hostname VARCHAR(16),
  errors JSON
);

DROP USER IF EXISTS 'coordinator';
DROP USER IF EXISTS 'grafana';
FLUSH PRIVILEGES;
CREATE USER 'coordinator' IDENTIFIED BY 'bar';
CREATE USER 'grafana' IDENTIFIED BY 'bar';
GRANT SELECT, INSERT ON gpu_db.* TO 'coordinator'@'%';
GRANT SELECT ON gpu_db.* TO 'grafana'@'%';
FLUSH PRIVILEGES;
