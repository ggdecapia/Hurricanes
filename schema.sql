-- Create tables for raw data to be loaded into
CREATE TABLE hurricanes (
	index INT PRIMARY KEY,
	id INT,	
	name TEXT,
	date_stamp INT,
	time_stamp INT,
	status TEXT,
	latitude FLOAT,
	longitude FLOAT,
	wind INT,
	min_pressure INT,
	new_latitude FLOAT,
	new_longitude FLOAT,
	city TEXT,
	country TEXT,
    ocean TEXT,
    category INT
);

