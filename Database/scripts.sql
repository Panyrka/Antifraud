CREATE TABLE platform_lists (
  id SERIAL NOT NULL,
  name VARCHAR(255) NOT NULL,
  last_update timestamp NOT NULL,
  PRIMARY KEY (id)
);

insert into platform_lists(name, last_update) values ('black_list_devices', CURRENT_TIMESTAMP);
insert into platform_lists(name, last_update) values ('black_list_ip', CURRENT_TIMESTAMP);
insert into platform_lists(name, last_update) values ('black_list_phones', CURRENT_TIMESTAMP);
insert into platform_lists(name, last_update) values ('black_list_account', CURRENT_TIMESTAMP);

CREATE TABLE black_list_devices (
  id SERIAL NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  valid BOOLEAN NOT NULL,
  valid_from DATE,
  valid_until DATE,
  PRIMARY KEY (id)
);

CREATE TABLE black_list_ip (
  id SERIAL NOT NULL,
  name VARCHAR(255) NOT NULL,
  description VARCHAR(255),
  valid BOOLEAN NOT NULL,
  valid_from DATE,
  valid_until DATE,
  PRIMARY KEY (id)
);

CREATE TABLE black_list_phones (
  id SERIAL NOT NULL,
  name VARCHAR(255) NOT NULL,
  description VARCHAR(255),
  valid BOOLEAN NOT NULL,
  valid_from DATE,
  valid_until DATE,
  PRIMARY KEY (id)
);

CREATE TABLE black_list_account (
  id SERIAL NOT NULL,
  name VARCHAR(255) NOT NULL,
  description VARCHAR(255),
  valid BOOLEAN NOT NULL,
  valid_from DATE,
  valid_until DATE,
  PRIMARY KEY (id)
);

insert into black_list_phones(name, valid) values ('+73332221100', True);
insert into black_list_phones(name, valid) values ('+78005553555', True);
INSERT INTO black_list_phones (name, description, valid, valid_from, valid_until)
VALUES 
  ('+1234567890', 'This number has been involved in phishing scams', true, '2023-01-01', '2023-12-31'),
  ('+9876543210', 'This number has been used for fraudulent calls', true, '2023-01-01', '2023-12-31');

insert into black_list_ip(name, valid) values ('105.10.10.2', True);
insert into black_list_devices(name, valid) values ('666777', True);
insert into black_list_account(name, valid) values ('666888', True);

CREATE TABLE profiles (
  id SERIAL NOT NULL,
  name VARCHAR(255) NOT NULL,
  key VARCHAR(30) NOT NULL,
  date_segment varchar(2) NOT NULL,
  ds_number integer not null,
  PRIMARY KEY (id)
);

insert into profiles(name, key, date_segment, ds_number) values ('clientActivity_5y', 'clientId', 'y', 5)

CREATE TABLE clientActivity_5y (
  id SERIAL NOT NULL,
  key VARCHAR(64) NOT NULL,
  amount double precision NOT NULL,
  date_segment timestamp NOT NULL,
  PRIMARY KEY (id)
);