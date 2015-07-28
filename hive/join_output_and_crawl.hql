-- This query joins the crawled dataset with api output dataset 

-- HN API output fields: id,deleted,type,by,time,text,dead,parent,kids,url,score,title,parts,descendants
-- HN crawled data fields: item_id,url,num_links,num_images,num_scripts,num_styles,headers
-- Target table fields: id,url,score,num_links,num_images,num_scripts,num_styles,headers


INSERT OVERWRITE LOCAL DIRECTORY 'hn_api_crawl_join_results'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT hn_api_data_clean.id, hn_api_data_clean.url, hn_api_data_clean.score, hn_crawl_data.num_links, 
hn_crawl_data.num_images, hn_crawl_data.num_scripts, hn_crawl_data.num_styles, hn_crawl_data.headers
FROM hn_crawl_data JOIN hn_api_data_clean 
ON hn_crawl_data.item_id = hn_api_data_clean.id;
