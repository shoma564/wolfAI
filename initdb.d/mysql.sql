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
