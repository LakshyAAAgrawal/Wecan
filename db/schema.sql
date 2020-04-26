CREATE TABLE `ORGANISATION_DATA` (
	`organisation_id` INT(11) NOT NULL,
	`organisation_name` varchar(30),
	`organisation_city` varchar(30),
	`organisation_country` varchar(30),
	`organisation_address` varchar(100),
	`organisation_contact` varchar(20),
	`organisation_timezone` varchar(50) NOT NULL,
	PRIMARY KEY (`organisation_id`)
);

CREATE TABLE `USER_DATA` (
	`user_id` INT(11) NOT NULL AUTO_INCREMENT,
	`organisation_id` INT(11),
	`full_name` varchar(50),
	`email` varchar(50),
	`telegram_id` varchar(50),
	PRIMARY KEY (`user_id`)
);

CREATE TABLE `BOARD_DATA` (
	`board_id` INT(11) NOT NULL AUTO_INCREMENT,
	`board_name` varchar(50),
	`board_admin` INT(11),
	PRIMARY KEY (`board_id`)
);

CREATE TABLE `LIST_DATA` (
	`list_id` INT(11) NOT NULL AUTO_INCREMENT,
	`list_name` varchar(50),
	`board_id` INT(11),
	`list_admin` INT(11),
	`list_label` varchar(50),
	PRIMARY KEY (`list_id`)
);

CREATE TABLE `CARD_DATA` (
	`card_id` INT(11) NOT NULL AUTO_INCREMENT,
	`card_name` varchar(50),
	`list_id` INT(11),
	`card_admin` INT(11),
	`multimedia` blob(50),
	`card_text` varchar(240) NOT NULL,
	`card_modification_date` DATETIME NOT NULL,
	`card_creation_datetime` DATETIME NOT NULL,
	PRIMARY KEY (`card_id`)
);

CREATE TABLE `ACTION_LOG` (
	`card_id` INT(11),
	`user_id` INT(11),
	`action_date_time` DATETIME,
	`timezone` varchar(50),
	`list_id_moved_from` INT(11) NOT NULL,
	`list_id_moved_to` INT(11) NOT NULL
);

CREATE TABLE `CARD_COMMENT` (
	`comment_id` INT(11) NOT NULL AUTO_INCREMENT,
	`user_id` INT(11),
	`comment_date_time` DATETIME,
	`comment_text` varchar(240),
	`card_id` INT(11) NOT NULL,
	PRIMARY KEY (`comment_id`)
);

CREATE TABLE `LIST_COMMENT` (
	`comment_id` INT(11) NOT NULL AUTO_INCREMENT,
	`user_id` INT(11),
	`comment_date_time` DATETIME,
	`comment_text` varchar(240),
	`list_id` INT(11) NOT NULL,
	PRIMARY KEY (`comment_id`)
);

CREATE TABLE `BOARD_COMMENT` (
	`comment_id` INT(11) NOT NULL AUTO_INCREMENT,
	`user_id` INT(11),
	`comment_date_time` DATETIME,
	`comment_text` varchar(240),
	`board_id` INT(11) NOT NULL,
	PRIMARY KEY (`comment_id`)
);

CREATE TABLE `Organisation_Board_mapping` (
	`organisation_id` INT(11) NOT NULL,
	`board_id` INT(11) NOT NULL
);

ALTER TABLE `USER_DATA` ADD CONSTRAINT `USER_DATA_fk0` FOREIGN KEY (`organisation_id`) REFERENCES `ORGANISATION_DATA`(`organisation_id`);

ALTER TABLE `BOARD_DATA` ADD CONSTRAINT `BOARD_DATA_fk0` FOREIGN KEY (`board_admin`) REFERENCES `USER_DATA`(`user_id`);

ALTER TABLE `LIST_DATA` ADD CONSTRAINT `LIST_DATA_fk0` FOREIGN KEY (`board_id`) REFERENCES `BOARD_DATA`(`board_id`);

ALTER TABLE `CARD_DATA` ADD CONSTRAINT `CARD_DATA_fk0` FOREIGN KEY (`list_id`) REFERENCES `LIST_DATA`(`list_id`);

ALTER TABLE `CARD_DATA` ADD CONSTRAINT `CARD_DATA_fk1` FOREIGN KEY (`card_admin`) REFERENCES `USER_DATA`(`user_id`);

ALTER TABLE `ACTION_LOG` ADD CONSTRAINT `ACTION_LOG_fk0` FOREIGN KEY (`card_id`) REFERENCES `CARD_DATA`(`card_id`);

ALTER TABLE `ACTION_LOG` ADD CONSTRAINT `ACTION_LOG_fk1` FOREIGN KEY (`user_id`) REFERENCES `USER_DATA`(`user_id`);

ALTER TABLE `CARD_COMMENT` ADD CONSTRAINT `CARD_COMMENT_fk0` FOREIGN KEY (`user_id`) REFERENCES `USER_DATA`(`user_id`);

ALTER TABLE `CARD_COMMENT` ADD CONSTRAINT `CARD_COMMENT_fk1` FOREIGN KEY (`card_id`) REFERENCES `CARD_DATA`(`card_id`);

ALTER TABLE `LIST_COMMENT` ADD CONSTRAINT `LIST_COMMENT_fk0` FOREIGN KEY (`user_id`) REFERENCES `USER_DATA`(`user_id`);

ALTER TABLE `LIST_COMMENT` ADD CONSTRAINT `LIST_COMMENT_fk1` FOREIGN KEY (`list_id`) REFERENCES `LIST_DATA`(`list_id`);

ALTER TABLE `BOARD_COMMENT` ADD CONSTRAINT `BOARD_COMMENT_fk0` FOREIGN KEY (`user_id`) REFERENCES `USER_DATA`(`user_id`);

ALTER TABLE `BOARD_COMMENT` ADD CONSTRAINT `BOARD_COMMENT_fk1` FOREIGN KEY (`board_id`) REFERENCES `BOARD_DATA`(`board_id`);

ALTER TABLE `Organisation_Board_mapping` ADD CONSTRAINT `Organisation_Board_mapping_fk0` FOREIGN KEY (`organisation_id`) REFERENCES `ORGANISATION_DATA`(`organisation_id`);

ALTER TABLE `Organisation_Board_mapping` ADD CONSTRAINT `Organisation_Board_mapping_fk1` FOREIGN KEY (`board_id`) REFERENCES `BOARD_DATA`(`board_id`);

