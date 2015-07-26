-- This query joins the crawled dataset with api output dataset 

-- HN API output fields: id,deleted,type,by,time,text,dead,parent,kids,url,score,title,parts,descendants
-- HN crawled data fields: item_id,url,num_links,num_images,num_scripts,num_styles,headers,text
-- Target table fields: id,url,score,num_links,num_images,num_scripts,num_styles,headers,text


CREATE EXTERNAL TABLE hn_records (record_line string);