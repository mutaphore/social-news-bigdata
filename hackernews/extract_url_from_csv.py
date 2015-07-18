#!/usr/local/bin/python
import os
import sys
import csv

def extract_url(csv_filepath, output_filepath):
	"Extracts urls from a csv file"
	infile = open(csv_filepath, "rb")
	outfile = open(output_filepath, "wb")
	reader = csv.DictReader(infile)
	for row in reader:
		if not row['url']:
			print "url not found"
			continue
		outfile.write(row['url'] + '\n')
	infile.close()
	outfile.close()


if __name__ == '__main__':
	extract_url("output_0.csv", "urls.txt")	