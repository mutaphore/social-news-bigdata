#!/usr/local/bin/python

import os, sys
import csv
import requests

BASE_URL = "https://hacker-news.firebaseio.com/v0"
ITEM = BASE_URL + "/item/{0}.json"
MAXITEM = BASE_URL + "/maxitem.json"

def get_request(url, text=True):
    "Make GET request to the API for a single item. Set text to False to return dict"
    r = requests.get(url)
    if r.status_code == 200:
        return r.text if text else r.json()
    else:
        print "Failed: status_code " + r.status_code
        return None


def main():
    fieldnames = ["by", "descendants", "id", "kids", "score", "time", "title", "type", "url"]
    with open("output.csv", "w") as csvfile:
        max_id = get_request(MAXITEM)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(get_request(ITEM.format(1), text=False))


if __name__ == '__main__':
    main()
