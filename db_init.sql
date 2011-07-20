CREATE DATABASE IF NOT EXISTS astro;

CREATE USER 'astro'@'localhost' IDENTIFIED BY '5gh6w35';
GRANT ALL ON astro.* TO 'astro'@'localhost';

CREATE TABLE IF NOT EXISTS  `astro`.`stars`
(`id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
 `name` VARCHAR(50) UNIQUE NOT NULL,
 `alfa` INTEGER NOT NULL,
 `delta` INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS `astro`.`notes`
(
 `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
 `note` VARCHAR(255) NOT NULL
);

