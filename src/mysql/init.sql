-- create the user to access the db
CREATE USER 'nw_user'@'localhost' IDENTIFIED BY 'Newswatch123';

CREATE DATABASE newswatch;

-- give the user created above access to the newswatch db
GRANT ALL PRIVILEGES ON newswatch.* TO 'nw_user'@'localhost';

USE newswatch;

CREATE TABLE user(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    passcode VARCHAR(255) NOT NULL
);

CREATE TABLE subscription(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    username VARCHAR(255),
    keyword VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (username) REFERENCES user(username)
);

-- create the initial user
INSERT INTO user(username, passcode) VALUES ('admin', 'Admin123');