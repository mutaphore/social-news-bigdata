#!/usr/bin/python

 # HN fields: id,deleted,type,by,time,text,dead,parent,kids,url,score,title,parts,descendants

import re
import sys
import csv

reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
for row in reader:
    #strip comma from the fields
    clean_fields = []
    for field in row:
        field = re.sub(",", "", field)
        if field == "":
            field = "[EMPTY_FIELD]"
        clean_fields.append(field)
    #take only the following fields:
    #id, type, author(by), time, text, url, score, title, descendants
    new_fields = [clean_fields[0], clean_fields[2], clean_fields[3], clean_fields[4], clean_fields[5], 
                  clean_fields[9], clean_fields[10], clean_fields[11], clean_fields[13]]
    print "\t".join(new_fields)