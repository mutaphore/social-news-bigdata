#!/usr/bin/python

import re
import sys
import csv

reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
for row in reader:
    #clean the title field
    row[2] = re.sub(",", "", row[2])
    print "\t".join(row)