-- HN fields: id,deleted,type,by,time,text,dead,parent,kids,url,score,title,parts,descendants

CREATE EXTERNAL TABLE records (record_line string)
LOCATION '/user/cloudera/hiveInputHn/';

CREATE EXTERNAL TABLE hn_data (id int, type string, author string, time int, text string, 
    url string, score int, title string, descendants int)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

ADD file /home/cloudera/bigdata_project/hive/filter_hn_fields.py;

INSERT INTO TABLE hn_data
SELECT TRANSFORM(record_line)
USING 'filter_hn_fields.py' AS id, type, author, time, text, url, score, title, descendants
FROM records;