#!/usr/bin/python

 # HN fields: id,deleted,type,by,time,text,dead,parent,kids,url,score,title,parts,descendants

import re
import sys
import csv

reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
for row in reader:
    #strip comma from the fields
    for field in row:
        field = re.sub(",", "", field)
    #take only the following fields:
    #id, type, author(by), time, text, url, score, title, descendants
    new_fields = [row[0], row[2], row[3], row[4], row[5], row[9], row[10], row[11], row[13]]
    print "\t".join(new_fields)