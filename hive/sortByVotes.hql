-- Get the initial records
create external table records (record_line string)
location '/user/cloudera/hiveInput/';

CREATE EXTERNAL TABLE reddit_data (id string, score int, title string, url string, author string, num_comments int, created_utc float, subreddit string, domain string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

ADD file /home/cloudera/bigdata_project/hive/remove_title_comma.py;

-- Strip commas in the title field so we could use comma as delimiter of fields
INSERT INTO TABLE reddit_data
SELECT TRANSFORM(record_line)
USING 'remove_title_comma.py' AS id, score, title, url, author, num_comments, created_utc, subreddit, domain
FROM records;

CREATE EXTERNAL TABLE reddit_data_sorted (id string, score int, title string, url string, author string, num_comments int, created_utc float, subreddit string, domain string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

-- Sort by number of votes
INSERT INTO TABLE reddit_data_sorted
SELECT * FROM reddit_data
ORDER BY score DESC;


