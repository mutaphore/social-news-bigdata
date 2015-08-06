-- This query joins the crawled dataset with api output dataset 

-- HN API output fields: id,deleted,type,by,time,text,dead,parent,kids,url,score,title,parts,descendants
-- HN crawled data fields: item_id,url,num_links,num_images,num_scripts,num_styles,headers
-- Target table fields: id,url,score,num_links,num_images,num_scripts,num_styles,headers

CREATE EXTERNAL TABLE IF NOT EXISTS hn_crawl_data (
    item_id int, 
    url string, 
    num_links int, 
    num_images int, 
    num_scripts int, 
    num_styles int, 
    headers string
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION 's3://deweichen/hackernews/emr_output/processed_crawl_data/';

CREATE EXTERNAL TABLE IF NOT EXISTS hn_api_data (
	id int, 
	type string, 
	author string, 
	time int, 
	text string, 
	url string, 
	score int, 
	title string, 
	descendants int
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION 's3://deweichen/hackernews/emr_output/processed_api_data/';

CREATE EXTERNAL TABLE IF NOT EXISTS join_results (
	id int,
	url string,
	score int,
	num_links int, 
    num_images int, 
    num_scripts int, 
    num_styles int, 
    headers string
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION 's3://deweichen/hackernews/emr_output/api_crawl_join_results/';

INSERT OVERWRITE TABLE join_results
SELECT hn_api_data.id, hn_api_data.url, hn_api_data.score, hn_crawl_data.num_links, 
hn_crawl_data.num_images, hn_crawl_data.num_scripts, hn_crawl_data.num_styles, hn_crawl_data.headers
FROM hn_crawl_data JOIN hn_api_data
ON hn_crawl_data.item_id = hn_api_data.id;
