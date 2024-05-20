CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    name TEXT,
    full_name TEXT,
    birth_date DATE,
    age INT,
    height_cm DECIMAL,
    weight_kgs DECIMAL,
    positions TEXT,
    nationality TEXT,
    overall_rating INT,
    potential INT,
    value_euro BIGINT,
    wage_euro INT,
    preferred_foot TEXT,
    international_reputation INT,
    weak_foot INT,
    skill_moves INT,
    body_type TEXT,
    release_clause_euro BIGINT,
    national_team TEXT,
    national_rating INT,
    national_team_position TEXT,
    national_jersey_number INT,
    crossing INT,
    finishing INT,
    heading_accuracy INT,
    short_passing INT,
    volleys INT,
    dribbling INT,
    curve INT,
    freekick_accuracy INT,
    long_passing INT,
    ball_control INT,
    acceleration INT,
    sprint_speed INT,
    agility INT,
    reactions INT,
    balance INT,
    shot_power INT,
    jumping INT,
    stamina INT,
    strength INT,
    long_shots INT,
    aggression INT,
    interceptions INT,
    positioning INT,
    vision INT,
    penalties INT,
    composure INT,
    marking INT,
    standing_tackle INT,
    sliding_tackle INT
);

COPY players(name, full_name, birth_date, age, height_cm, weight_kgs, positions, nationality, overall_rating, potential, value_euro, wage_euro, preferred_foot, international_reputation, weak_foot, skill_moves, body_type, release_clause_euro, national_team, national_rating, national_team_position, national_jersey_number, crossing, finishing, heading_accuracy, short_passing, volleys, dribbling, curve, freekick_accuracy, long_passing, ball_control, acceleration, sprint_speed, agility, reactions, balance, shot_power, jumping, stamina, strength, long_shots, aggression, interceptions, positioning, vision, penalties, composure, marking, standing_tackle, sliding_tackle)
FROM '/docker-entrypoint-initdb.d/players.csv' DELIMITER ',' CSV HEADER;
