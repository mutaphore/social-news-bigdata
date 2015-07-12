#!/usr/local/bin/python

import os, sys
import csv
import re
import argparse
import requests

BASE_URL = "https://hacker-news.firebaseio.com/v0"
ITEM_URL = BASE_URL + "/item/{0}.json"
MAXITEM_URL = BASE_URL + "/maxitem.json"

def get_request(url, text=True):
    "Make GET request to the API for a single item. Set text to False to return dict"
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print "Failed: connection refused"
        return None
    r.encoding = "utf-8"
    if r.status_code == 200:
        return r.text if text else r.json()
    else:
        print "Failed: status_code " + str(r.status_code)
        return None


def main():
    max_id = int(get_request(MAXITEM_URL))
    parser = argparse.ArgumentParser(description='Make HackerNews API requests')
    parser.add_argument('-start', dest='start_id', type=int, default=1, help='Start item id')
    parser.add_argument('-end', dest='end_id', type=int, default=max_id, help='End item id')
    parser.add_argument('-o', dest='outfile', type=str, default="output.csv", help='Output file')
    args = parser.parse_args()

    fieldnames = ["id", "deleted", "type", "by", "time", "text", "dead", "parent", 
                  "kids", "url", "score", "title", "parts", "descendants"]
    with open(args.outfile, "a" if os.path.isfile(args.outfile) else "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in xrange(args.start_id, args.end_id):
            sys.stdout.write("Downloading item id %d\r" % i)
            sys.stdout.flush()
            obj = get_request(ITEM_URL.format(i), text=False)
            if not obj:
                print "Failed on item id %d" % i
                continue
            #do some clean up here
            for key, value in obj.iteritems():
                if isinstance(value, str) or isinstance(value, unicode):
                    value = re.sub(r"[\n\t]", " ", value)
                if isinstance(value, unicode):
                    obj[key] = value.encode("utf-8")
            #write to csv
            writer.writerow(obj)


if __name__ == '__main__':
    main()