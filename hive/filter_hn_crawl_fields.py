#!/usr/bin/python

 # HN API fields: item_id,url,num_links,num_images,num_scripts,num_styles,headers,text

import re
import sys
import csv

reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
for row in reader:
    #strip comma from the fields
    clean_fields = []
    for field in row:
        field = field.replace(",", "")
        if field == "":
            field = "[EMPTY_FIELD]"
        clean_fields.append(field)
    print "\t".join(clean_fields)