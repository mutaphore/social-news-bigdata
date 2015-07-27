-- This query joins the crawled dataset with api output dataset 

-- HN API output fields: id,deleted,type,by,time,text,dead,parent,kids,url,score,title,parts,descendants
-- HN crawled data fields: item_id,url,num_links,num_images,num_scripts,num_styles,headers
-- Target table fields: id,url,score,num_links,num_images,num_scripts,num_styles,headers


CREATE EXTERNAL TABLE hn_api_crawl (id int, url string, score int, num_links int, num_images int, num_scripts int, num_styles int, headers string)

