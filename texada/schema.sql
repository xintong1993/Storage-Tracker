DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS location_record;

CREATE TABLE `product` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `description` VARCHAR(255) NOT NULL,

	PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `location_record` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `product_id` INT NOT NULL,
    `datetime` VARCHAR(255) NOT NULL,
    `longitude` FLOAT NOT NULL,
    `latitude` FLOAT NOT NULL,
    `elevation` INT NOT NULL,

    PRIMARY KEY ( `id` ),
    FOREIGN KEY ( `product_id` ) REFERENCES `product`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

