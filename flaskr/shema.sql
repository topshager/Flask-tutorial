DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

create table user
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT unique not null,
  password TEXT not null
);
CREATE TABLE post
(
  id INTEGER primary key AUTOINCREMENT,
  author_id INTEGER not null,
  created TIMESTAMP NOT NULL DEFUALT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN kEY (AUTHOR_ID) REFERENCES user (id)
);
