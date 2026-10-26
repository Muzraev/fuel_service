PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0)
);

CREATE TABLE IF NOT EXISTS fuels (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0)
);

CREATE TABLE IF NOT EXISTS consumptions (
    id INTEGER PRIMARY KEY,
    car_id INTEGER NOT NULL UNIQUE REFERENCES cars(id),
    liters_per_100km REAL NOT NULL CHECK (liters_per_100km > 0)
);

CREATE TABLE IF NOT EXISTS refuelings (
    id INTEGER PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(id),
    fuel_id INTEGER NOT NULL REFERENCES fuels(id),
    fuel_liters REAL NOT NULL CHECK (fuel_liters > 0),
    price_per_liter REAL NOT NULL CHECK (price_per_liter > 0)
);

CREATE INDEX IF NOT EXISTS refuelings_car ON refuelings(car_id);
CREATE INDEX IF NOT EXISTS refuelings_fuel ON refuelings(fuel_id);
