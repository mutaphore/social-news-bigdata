#!/usr/local/bin

import csv
import os
import sys

def is_good_url(url):
	if url and url[-4:] != ".pdf" and url[-4:] != ".jpg":
		return True
	return False


def get_urls(infile, outfile):
	out = open(outfile, "w")
	out.write("id,url\n")
	with open(infile, "r") as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if is_good_url(row['url']):
				out.write(row['id'] + "," + row['url'] + "\n")
	out.close()


if __name__ == '__main__':
	get_urls("output_2_storyitems.csv", "output_2_urls.txt")

