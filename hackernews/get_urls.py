#!/usr/local/bin

import csv
import os
import sys
import requests
import argparse

def is_good_url(url):
    #basic checks
    if not url or url[-4:] == ".pdf" or url[-4:] == ".jpg":
        return False
    #check the response
    try:
        r = requests.get(url, timeout=5)
    except:
        e = sys.exc_info()[0]
        print "Error: %s" % e
        return False
    if r.status_code != 200:
        return False
    return True


def get_urls(infile, outfile):
    out = open(outfile, "w")
    out.write("id,url\n")
    with open(infile, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sys.stdout.write("Working on item id {0}: {1}\n".format(row['id'], row['url']))
            if is_good_url(row['url']):
                out.write(row['id'] + "," + row['url'] + "\n")
    out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parses item id and url from csv to a file')
    parser.add_argument('-i', dest='infile', type=str, default="output_3_storyitems.csv", help='Input file')
    parser.add_argument('-o', dest='outfile', type=str, default="output_3_urls.csv", help='Output file')
    args = parser.parse_args()
    get_urls(args.infile, args.outfile)

