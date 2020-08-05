CREATE TABLE ORGANISATION (
organisation_id int NOT NULL auto_increment,
organisation_name varchar(64) NOT NULL,
city varchar (64) NOT NULL,
country varchar(64) NOT NULL,
country_code varchar(8) NOT NULL,
timezone varchar(64) NOT NULL,
address varchar(512) NOT NULL,
contact varchar(16) NOT NULL,
email varchar(128) NOT NULL,
PRIMARY KEY(organisation_id),
UNIQUE KEY(organisation_name)
);


CREATE TABLE USER (
user_id int NOT NULL auto_increment,
user_name varchar(64) NOT NULL,
passwd varchar (128) NOT NULL,
full_name varchar(128) NOT NULL,
email varchar(128) NOT NULL,
organisation_id int NOT NULL,
PRIMARY KEY(user_id),
UNIQUE KEY(user_name),
FOREIGN KEY (organisation_id) REFERENCES ORGANISATION(organisation_id)
);


CREATE TABLE BOARD (
board_id int NOT NULL auto_increment,
board_name varchar(128) NOT NULL,
board_admin int,
primary key(board_id),
UNIQUE KEY(board_name),
foreign key (board_admin) REFERENCES USER(user_id)
);


CREATE TABLE BOARD_USER (
	user_id int NOT NULL,
    board_id int NOT NULL,
    foreign key (board_id) references BOARD(board_id),
    foreign key (user_id) references USER(user_id)
);


CREATE TABLE TELEGRAM (
	telegram_id int NOT NULL auto_increment,
    telegram_handle varchar(128) NOT NULL,
    user_id int NOT NULL,
    unique key(user_id),
    unique key(telegram_handle),
    foreign key (user_id) references USER(user_id),
    primary key (telegram_id)
);


CREATE TABLE MULTIMEDIA (
multimedia_id int NOT NULL auto_increment,
multimedia blob NOT NULL,
primary key (multimedia_id)
);


CREATE TABLE ANNOUNCEMENT (
announcement_id int NOT NULL auto_increment,
board_id int NOT NULL,
user_id int NOT NULL,
title varchar(128) NOT NULL,
body varchar(1024) NOT NULL,
multimedia_id int NOT NULL,
creation_time datetime default now(),
foreign key (multimedia_id) references MULTIMEDIA(multimedia_id),
foreign key (board_id) references BOARD(board_id),
foreign key (user_id) references USER(user_id),
primary key (announcement_id)
);


CREATE TABLE LIST(
list_id int NOT NULL auto_increment,
board_id int NOT NULL,
list_admin int NOT NULL,
list_name varchar(128) NOT NULL,
list_label varchar(128) NOT NULL,
foreign key (board_id) references BOARD(board_id),
foreign key (list_admin) references USER(user_id),
UNIQUE KEY(list_name),
primary key (list_id)
);


CREATE TABLE CARD (
card_id int NOT NULL auto_increment,
list_id int NOT NULL,
card_admin int NOT NULL,
card_name varchar(128) NOT NULL,
text varchar(1024) NOT NULL,
multimedia_id int NOT NULL,
foreign key (multimedia_id) references MULTIMEDIA(multimedia_id),
foreign key (list_id) references LIST(list_id),
foreign key (card_admin) references USER(user_id),
UNIQUE KEY(card_name),
primary key (card_id)
);


CREATE TABLE CARD_COMMENT (
comment_id int NOT NULL auto_increment,
card_id int NOT NULL,
user_id int NOT NULL,
text varchar(1024) NOT NULL,
creation_time datetime default now(),
foreign key (card_id) references CARD(card_id),
foreign key (user_id) references USER(user_id),
primary key (comment_id)
);


CREATE TABLE DEADLINE (
	card_id int NOT NULL,
    due_date datetime default now(),
    if_completed bool not null default 0,
	foreign key (card_id) references CARD(card_id)
);


CREATE TABLE CARD_MOVE (
card_id int NOT NULL,
user_id int NOT NULL,
moved_from_list_id int NOT NULL,
moved_to_list_id int NOT NULL,
creation_time datetime default now(),
foreign key (card_id) references CARD(card_id),
foreign key (user_id) references USER(user_id),
foreign key (moved_from_list_id) references LIST(list_id),
foreign key (moved_to_list_id) references LIST(list_id)
);