#!/usr/bin/python

import re
import sys
import csv

reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
for row in reader:
    #clean the fields
    for field in row:
        field = re.sub(",", "", field)
    print "\t".join(row)