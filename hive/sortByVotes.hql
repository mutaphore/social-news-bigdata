-- Fields: id, score, title, url, author, num_comments, created_utc, subreddit, domain

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

-- Distinct data
CREATE EXTERNAL TABLE reddit_data_distinct (id string, score int, title string, url string, author string, num_comments int, created_utc float, subreddit string, domain string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

INSERT INTO TABLE reddit_data_distinct
SELECT DISTINCT * 
FROM reddit_data;

-- For each id, get its max possible score
CREATE EXTERNAL TABLE id_maxscore (id string, maxscore int)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

INSERT OVERWRITE TABLE id_maxscore
SELECT reddit_data.id, MAX(reddit_data.score)
FROM reddit_data
GROUP BY reddit_data.id;

-- Final sorted data by joining with id_maxscore
CREATE EXTERNAL TABLE reddit_data_sorted (id string, score int, title string, url string, author string, num_comments int, created_utc float, subreddit string, domain string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

INSERT OVERWRITE TABLE reddit_data_sorted
SELECT * from reddit_data_distinct LEFT SEMI JOIN id_maxscore 
ON (reddit_data_distinct.id = id_maxscore.id AND reddit_data_distinct.score = id_maxscore.maxscore)
ORDER BY score DESC;
