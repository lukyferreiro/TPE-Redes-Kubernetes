CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY NOT NULL,
    player_name TEXT,
    team_abbreviation TEXT,
    age INT,
    player_height DECIMAL,
    player_weight DECIMAL,
    college TEXT,
    country TEXT,
    draft_year INT,
    draft_round INT
);