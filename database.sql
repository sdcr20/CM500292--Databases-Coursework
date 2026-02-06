CREATE TABLE IF NOT EXISTS destination (
    destination_id INTEGER NOT_NULL AUTO_INCREMENT,
    name TEXT NOT_NULL,
    city TEXT NOT_NULL,
    country TEXT NOT_NULL,
    timezone TEXT NOT_NULL,
    PRIMARY KEY (destination_id));

CREATE TABLE IF NOT EXISTS pilot (
    pilot_id INTEGER NOT_NULL AUTO_INCREMENT,
    name TEXT NOT_NULL,
    licence_number INTEGER NOT_NULL UNIQUE,
    aircraft_rating TEXT,
    base_id INTEGER NOT_NULL,
    PRIMARY KEY (pilot_id)
    FOREIGN KEY (base_id) REFERENCES destination(destination_id));

CREATE TABLE IF NOT EXISTS flight (
    flight_id INTEGER NOT_NULL AUTO_INCREMENT,
    flight_number TEXT NOT_NULL,
    departure_id INTEGER NOT_NULL,
    arrival_id INTEGER NOT_NULL,
    pilot_id INTEGER NOT_NULL,
    departure_time TEXT NOT_NULL,   -- Store as ISO 8601 string
    arrival_time TEXT NOT_NULL,     -- Store as ISO 8601 string
    PRIMARY KEY (flight_id),
    FOREIGN KEY (departure_id) REFERENCES destination(destination_id),
    FOREIGN KEY (arrival_id) REFERENCES destination(destination_id),
    FOREIGN KEY (pilot_id) REFERENCES pilot(pilot_id));
    
INSERT INTO destination (name, city, country, timezone)
VALUES




INSERT INTO pilot (name, licence_number, aircraft_rating, base_id)
VALUES




INSERT INTO flight (flight_number, departure_id, arrival_id, pilot_id, departure_time, arrival_time)
VALUES