#!/usr/bin/python

import re
import sys
import csv

reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
for row in reader:
    #clean the fields
    clean_fields = []
    for field in row:
        field = re.sub(",", "", field)
        if field == "":
            field = "[EMPTY_FIELD]"
        clean_fields.append(field)
    print "\t".join(clean_fields)