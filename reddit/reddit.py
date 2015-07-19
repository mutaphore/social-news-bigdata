#!/usr/local/bin/python
# to run this script, install praw first: pip install praw
import time
import praw
import csv
import sys
import codecs, cStringIO
from pprint import pprint


class UnicodeDictWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.fieldnames = fieldnames
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writeheader(self):
        self.writer.writerow(self.fieldnames)

    def writerow(self, row):
        self.writer.writerow([row[x].encode("utf-8") for x in self.fieldnames])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)




def getSubmissions(afterid):
    try:
        submissions = r.get_content(url='http://www.reddit.com/top', params={'after': afterid, 'limit':1000, 't':'all'});
    except HTTPException:
        print 'Retry'
        time.sleep(2)
        submissions = r.get_content(url='http://www.reddit.com/top', params={'after': afterid, 'limit':1000, 't':'all'});

    return submissions


r = praw.Reddit(user_agent='my_cool_application')

spamwriter = UnicodeDictWriter(open('output.csv','a'), 
    ['id', 
    'score', 
    'title', 
    'url', 
    'author',
    'num_comments',
    'created_utc',
    'subreddit',
    'domain'
    ])

spamwriter.writeheader();

#spamwriter.writerow(['id', 'title', 'url', 'score', 'author', 'num_comments','created_utc','subreddit'])

numposts = 10000000
postcounter = 0
afterid = ''
# afterid = '3dpzt1'

while postcounter < numposts:

    submissions = getSubmissions(afterid)

    for post in submissions:
        print str(postcounter) + ', ' + str(post.score) + ',' + post.id + ',' + post.title +  ',' + post.url
        #spamwriter.writerow([post.id, post.title, post.url,post.score, str(post.author), post.num_comments, post.created_utc, post.subreddit])

        #pprint(vars(post.author))

        spamwriter.writerow({
            'id':post.id, 
            'score': str(post.score),
            'title': post.title,
            'url' : post.url,
            'author': post.author.name if hasattr(post.author, 'name') else 'noauthorfound', 
            'num_comments': str(post.num_comments),
            'created_utc': str(post.created_utc),
            'subreddit': post.subreddit.display_name,
	    'domain' : post.domain
            })

        afterid = post.id
        postcounter += 1






'''
with open('output1.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')

    spamwriter.writerow(['id', 'title', 'url', 'score', 'author', 'num_comments','created_utc'])

    for post in submissions:
        #pprint(vars(post))
        spamwriter.writerow([post.id, (post.title).encode('utf-8'), post.url,post.score, post.author, post.num_comments, post.created_utc])

'''

