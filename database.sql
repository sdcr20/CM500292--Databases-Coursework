CREATE TABLE IF NOT EXISTS timezone (
    code TEXT UNIQUE NOT NULL,
    utc_difference TEXT NOT NULL,  -- format ±HH:MM:SS
    acronym TEXT NOT NULL,         -- e.g. UTC, EST, CET
    long_name TEXT NOT NULL,       -- e.g. Coordinated Universal Time
    PRIMARY KEY(code));

CREATE TABLE IF NOT EXISTS destination (
    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    timezone TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS rating (
    rating_code TEXT UNIQUE NOT NULL,
    rating_name TEXT NOT NULL,
    aircraft TEXT NOT NULL,
    PRIMARY KEY (rating_code));

CREATE TABLE IF NOT EXISTS pilot (
    pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    licence_number INTEGER NOT NULL UNIQUE,
    aircraft_rating TEXT,
    base_id INTEGER NOT NULL,
    last_medical_date TEXT NOT NULL,    --Store as ISO 8601 string
    FOREIGN KEY (base_id) REFERENCES destination(destination_id),
    FOREIGN KEY (aircraft_rating) REFERENCES rating(rating_code));

CREATE TABLE IF NOT EXISTS flight (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT NOT NULL,
    departure_id INTEGER NOT NULL,
    arrival_id INTEGER NOT NULL,
    pilot_id INTEGER NOT NULL,
    departure_time_utc TEXT NOT NULL,   -- ISO 8601
    arrival_time_utc TEXT NOT NULL,     -- ISO 8601
    flight_duration_minutes INTEGER
        GENERATED ALWAYS AS(
            CAST((julianday(arrival_time_utc) - julianday(departure_time_utc)) * 1440 AS INTEGER)
        ) STORED,
    FOREIGN KEY (departure_id) REFERENCES destination(destination_id),
    FOREIGN KEY (arrival_id) REFERENCES destination(destination_id),
    FOREIGN KEY (pilot_id) REFERENCES pilot(pilot_id)
);
    
INSERT INTO timezone (code, utc_difference, acronym, long_name)
VALUES
('Z','+00:00:00','UTC','Coordinated Universal Time'),
('A','+01:00:00','CET','Central European Time'),
('B','+02:00:00','EET','Eastern European Time'),
('C','+03:00:00','MSK','Moscow Standard Time'),
('D','+04:00:00','GST','Gulf Standard Time'),
('E','+05:00:00','PKT','Pakistan Standard Time'),
('F','+06:00:00','BST','Bangladesh Standard Time'),
('G','+07:00:00','ICT','Indochina Time'),
('H','+08:00:00','CST','China Standard Time'),
('I','+09:00:00','JST','Japan Standard Time'),
('K','+10:00:00','AEST','Australian Eastern Standard Time'),
('L','+11:00:00','SBT','Solomon Islands Time'),
('M','+12:00:00','NZST','New Zealand Standard Time'),
('N','-01:00:00','CVT','Cape Verde Time'),
('O','-02:00:00','GST','South Georgia Time'),
('P','-03:00:00','ART','Argentina Time'),
('Q','-04:00:00','AST','Atlantic Standard Time'),
('R','-05:00:00','EST','Eastern Standard Time'),
('S','-06:00:00','CST','Central Standard Time'),
('T','-07:00:00','MST','Mountain Standard Time'),
('U','-08:00:00','PST','Pacific Standard Time'),
('V','-09:00:00','AKST','Alaska Standard Time'),
('W','-10:00:00','HST','Hawaii–Aleutian Standard Time'),
('X','-11:00:00','SST','Samoa Standard Time'),
('Y','-12:00:00','BIT','Baker Island Time');

SELECT * FROM timezone;

INSERT INTO destination (name, city, country, timezone)
VALUES
('London Luton Airport','London','United Kingdom','Z'),
('Amsterdam Airport Schiphol','Amsterdam','Netherlands','A'),
('Charles de Gaulle Airport','Paris','France','A'),
('Barcelona–El Prat Airport','Barcelona','Spain','A'),
('Leonardo da Vinci–Fiumicino Airport','Rome','Italy','A'),
('John Paul II Kraków–Balice Airport','Kraków','Poland','A'),
('Budapest Ferenc Liszt International Airport','Budapest','Hungary','A'),
('Václav Havel Airport Prague','Prague','Czech Republic','A'),
('Lisbon Humberto Delgado Airport','Lisbon','Portugal','Z'),
('Alicante–Elche Miguel Hernández Airport','Alicante','Spain','A');

SELECT * FROM destination;

INSERT INTO rating (rating_code, rating_name, aircraft)
VALUES

('A320','Airbus A320 Type Rating','Airbus A320'),
('A321','Airbus A321 Type Rating','Airbus A321'),
('A319','Airbus A319 Type Rating','Airbus A319'),
('A320F','Airbus A320 Family Type Rating','Airbus A320 Family'),
('B737','Boeing 737 Type Rating','Boeing 737'),
('B738','Boeing 737-800 Type Rating','Boeing 737-800'),
('E190','Embraer 190 Type Rating','Embraer 190'),
('E195','Embraer 195 Type Rating','Embraer 195'),
('ATR72','ATR 72 Type Rating','ATR 72'),
('A220','Airbus A220 Type Rating','Airbus A220');

SELECT * FROM rating;

INSERT INTO pilot (name, licence_number, aircraft_rating, base_id, last_medical_date)
VALUES

('James Thornton',200501,'A320',1,'2025-11-14'),
('Sarah Williams',200502,'A321',1,'2025-09-03'),
('Daniel Foster',200503,'A320F',1,'2025-12-01'),
('Emily Carter',200504,'A319',1,'2025-10-18'),
('Michael Hughes',200505,'B738',1,'2025-08-22'),
('Laura Bennett',200506,'A320',1,'2025-07-30'),
('Thomas Reed',200507,'E190',1,'2025-11-02'),
('Hannah Collins',200508,'E195',1,'2025-06-15'),
('Oliver Grant',200509,'B737',1,'2025-12-19'),
('Rebecca Moore',200510,'A220',1,'2025-09-27');

SELECT * FROM pilot;

INSERT INTO flight (flight_number, departure_id, arrival_id, pilot_id, departure_time_utc, arrival_time_utc)
VALUES
('LT2001', 1, 2, 1, '2026-02-18T06:30:00Z', '2026-02-18T07:45:00Z'),
('LT2002', 2, 1, 1, '2026-02-18T08:35:00Z', '2026-02-18T09:50:00Z'),

('LT2003', 1, 3, 2, '2026-02-18T07:00:00Z', '2026-02-18T08:20:00Z'),
('LT2004', 3, 1, 2, '2026-02-18T09:10:00Z', '2026-02-18T10:30:00Z'),

('LT2005', 1, 4, 3, '2026-02-18T09:15:00Z', '2026-02-18T11:30:00Z'),
('LT2006', 4, 1, 3, '2026-02-18T12:25:00Z', '2026-02-18T14:40:00Z'),

('LT2007', 1, 5, 4, '2026-02-19T06:20:00Z', '2026-02-19T09:00:00Z'),
('LT2008', 5, 1, 4, '2026-02-19T09:55:00Z', '2026-02-19T12:35:00Z'),

('LT2009', 1, 8, 5, '2026-02-19T07:10:00Z', '2026-02-19T09:05:00Z'),
('LT2010', 8, 1, 5, '2026-02-19T09:55:00Z', '2026-02-19T11:50:00Z'),

('LT2011', 1, 7, 6, '2026-02-19T12:00:00Z', '2026-02-19T14:25:00Z'),
('LT2012', 7, 1, 6, '2026-02-19T15:20:00Z', '2026-02-19T17:45:00Z'),

('LT2013', 1, 9, 7, '2026-02-20T06:10:00Z', '2026-02-20T09:00:00Z'),
('LT2014', 9, 1, 7, '2026-02-20T09:55:00Z', '2026-02-20T12:45:00Z'),

('LT2015', 1, 10, 8, '2026-02-20T13:30:00Z', '2026-02-20T16:00:00Z');

SELECT * FROM flight;