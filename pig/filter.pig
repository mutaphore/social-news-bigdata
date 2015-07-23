REGISTER ./tutorial.jar;
records = LOAD 'output.csv' USING PigStorage() AS (id:biginteger, deleted:int, type:chararray, by:chararray, time:chararray, text:chararray,dead:chararray, parent:chararray, kids:chararray, url:chararray, score:int, title:chararray, parts:chararray, descendants:int);
result = FILTER records BY type == 'story';
STORE result INTO 'filtered_output_test' USING PigStorage();
