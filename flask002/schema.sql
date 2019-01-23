drop table if exists users;
create table users (
  id integer primary key autoincrement,
  name string not null,
  psw char(50) not null,
  email string not null,
  age integer not null,
  birthday data not null,
  face string
);