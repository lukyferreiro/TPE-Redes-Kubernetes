\COPY players(name, team, age, height, weight, college, country, draft_year, draft_round)
FROM '/docker-entrypoint-initdb.d/players.csv'
DELIMITER ','
CSV HEADER;