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
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print "ConnectionError on url %r" % url
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
            if is_good_url(row['url']):
                out.write(row['id'] + "," + row['url'] + "\n")
    out.close()


if __name__ == '__main__':
    get_urls("output_3_storyitems.csv", "output_3_urls.csv")

