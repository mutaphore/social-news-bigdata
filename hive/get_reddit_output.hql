-- This query removes duplicates, invalid rows and then output result to a local directory

-- Reddit fields: id, score, title, url, author, num_comments, created_utc, subreddit, domain

DROP TABLE records;
DROP TABLE reddit_data;
DROP TABLE reddit_data_distinct;


-- Get the initial records
CREATE EXTERNAL TABLE records (record_line string)
LOCATION '/user/ph53/hiveInputReddit/';

-- Use this if records table already created:
-- LOAD DATA INPATH '/user/ph53/hiveInputReddit/'
-- INTO TABLE records;

CREATE EXTERNAL TABLE reddit_data (id string, score int, title string, url string, author string, num_comments int, created_utc float, subreddit string, domain string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

ADD file /home/ph53/bigdata_project/hive/remove_fields_comma.py;

-- Strip commas in the title field so we could use comma as delimiter of fields
INSERT OVERWRITE TABLE reddit_data
SELECT TRANSFORM(record_line)
USING 'remove_fields_comma.py' AS id, score, title, url, author, num_comments, created_utc, subreddit, domain
FROM records;

-- Filter distinct data
CREATE EXTERNAL TABLE reddit_data_distinct (id string, score int, title string, url string, author string, num_comments int, created_utc float, subreddit string, domain string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

INSERT OVERWRITE TABLE reddit_data_distinct
SELECT DISTINCT * 
FROM reddit_data;

-- Filter invalid rows
INSERT OVERWRITE TABLE reddit_data
SELECT * 
FROM reddit_data_distinct
WHERE created_utc is not NULL;


-- Output data to local directory
INSERT OVERWRITE LOCAL DIRECTORY '/home/ph53/bigdata_project/reddit/cleaned_data_from_hive'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT * FROM reddit_data
ORDER BY created_utc;
