USE mysql;
CREATE USER 'bot'@'localhost' IDENTIFIED BY 'password';
CREATE USER 'bot'@'%' IDENTIFIED BY 'password';
GRANT ALL ON *.* TO 'bot'@'localhost';
GRANT ALL ON *.* TO 'bot'@'%';
FLUSH PRIVILEGES;
