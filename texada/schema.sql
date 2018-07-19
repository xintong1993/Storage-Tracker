CREATE TABLE `product` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `description` VARCHAR(255) NOT NULL,
	`datetime` VARCHAR(255) NOT NULL,
	`longitude` FLOAT NOT NULL,
    `latitude` FLOAT NOT NULL,
	`elevation` INT NOT NULL,
	PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
