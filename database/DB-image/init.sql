CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT,
    team TEXT,
    age INT,
    height DECIMAL,
    weight DECIMAL,
    college TEXT,
    country TEXT,
    draft_year INT,
    draft_round INT
);