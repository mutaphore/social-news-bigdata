#!/usr/bin/python

 # HN API fields: item_id,url,num_links,num_images,num_scripts,num_styles,headers,text

import re
import sys
import csv

#need this because text field is large
csv.field_size_limit(sys.maxsize)

reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
for row in reader:
    #strip comma from the fields
    clean_fields = []
    for field in row[:7]:
        field = field.replace(",", "")
        if field == "":
            field = "[EMPTY_FIELD]"
        clean_fields.append(field)
    # ignore text for now
    # text = " ".join(row[7:])
    # clean_fields.append(text)
    print "\t".join(clean_fields)