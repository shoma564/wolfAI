CREATE DATABASE slack;
USE slack;

CREATE TABLE slack (
  id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  webhook_url CHAR(100),
  Channel_name CHAR(100),
  Channel_id CHAR(100),
  token CHAR(100),
  user CHAR(100),
  sub_date CHAR(100)
);

CREATE TABLE characters (
  game_id	INT,
  char_id INT,
  name CHAR(100),
  position INT,
  player INT,
  life INT,
  FOREIGN KEY(game_id) REFERENCES slack(id)
);

CREATE TABLE games (
  game_id	INT,
  day INT,
  phase INT,
  FOREIGN KEY(game_id) REFERENCES slack(id)
);

CREATE TABLE talks (
  game_id	INT,
  day INT,
  src INT,
  dst INT,
  text_id INT,
  opt INT,
  role INT,
  FOREIGN KEY(game_id) REFERENCES slack(id)
);

CREATE TABLE deduces (
  game_id	INT,
  char_id INT,
  target INT,
  deduce_wolf INT,
  deduce_villager INT,
  deduce_seer INT,
  trust INT,
  life INT,
  FOREIGN KEY(game_id) REFERENCES slack(id)
);
