#!/usr/local/bin/python

import os, sys
import requests

BASE_URL = "https://hacker-news.firebaseio.com/v0"
ITEM = BASE_URL + "/item/{0}.json?print=pretty"
MAXITEM = BASE_URL + "/maxitem.json?print=pretty"

def get_request(url):
	"Make GET request to the API for a single item"
	r = requests.get(url)
	if r.status_code == 200:
		return (r.json(), r.text)
	else:
		print "Failed: status_code " + r.status_code
		return (None, None)

def main():
	print get_request(ITEM.format(1))[1]

if __name__ == '__main__':
	main()
