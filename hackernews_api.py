#!/usr/local/bin/python

import os, sys
import csv
import re
import requests

BASE_URL = "https://hacker-news.firebaseio.com/v0"
ITEM_URL = BASE_URL + "/item/{0}.json"
MAXITEM_URL = BASE_URL + "/maxitem.json"

def get_request(url, text=True):
    "Make GET request to the API for a single item. Set text to False to return dict"
    r = requests.get(url)
    r.encoding = "utf-8"
    if r.status_code == 200:
        return r.text if text else r.json()
    else:
        print "Failed: status_code " + str(r.status_code)
        return None


def main():
    fieldnames = ["id", "deleted", "type", "by", "time", "text", "dead", "parent", 
                  "kids", "url", "score", "title", "parts", "descendants"]
    path = "output.csv"
    with open("path", "a" if os.path.isfile(path) else "w") as csvfile:
        max_id = int(get_request(MAXITEM_URL))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in xrange(1, max_id):
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