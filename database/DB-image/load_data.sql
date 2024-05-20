\COPY players(player_name, team_abbreviation, age, player_height, player_weight, college, country, draft_year, draft_round)
FROM '/docker-entrypoint-initdb.d/players.csv'
DELIMITER ','
CSV HEADER;