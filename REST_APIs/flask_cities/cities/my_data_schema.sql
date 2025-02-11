 --
-- Table structure for table country
--

CREATE TABLE if not exists country (
  country_id SMALLINT NOT NULL,
  country VARCHAR(50) NOT NULL,
  last_update TIMESTAMP,
  PRIMARY KEY  (country_id)
)
;


CREATE TABLE if not exists city (
  city_id int NOT NULL,
  city VARCHAR(50) NOT NULL,
  country_id SMALLINT NOT NULL,
  last_update TIMESTAMP NOT NULL,
  PRIMARY KEY  (city_id),
  CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE NO ACTION ON UPDATE CASCADE
)
;


CREATE TABLE if not exists visit(
  visit_id int NOT NULL,
  counter int NOT NULL,
  PRIMARY KEY(visit_id)
)
;

