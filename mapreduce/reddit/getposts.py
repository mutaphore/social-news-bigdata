# to run this script, install praw first: pip install praw
import time
import praw
import csv
from pprint import pprint

r = praw.Reddit(user_agent='my_cool_application')
#submissions = r.get_subreddit('technology').get_top_from_all(limit=3, place_holder='3bseel', after_field='after')
#submissions = r.get_content(url='http://www.reddit.com/r/technology', params={'after':'t3_3dpxfd', 'limit':500});
submissions = r.get_content(url='http://www.reddit.com/r/technology', params={'limit':100});

numposts = 1000
postcounter = 0
afterid = ''

while postcounter < numposts:
    for post in submissions:
        print str(postcounter) + ', ' + post.id.encode('utf-8') + ',' + post.title.encode('utf-8')
        afterid = post.id
        postcounter += 1

    print 'next run'
    time.sleep(2)
    
    try:
        submissions = r.get_content(url='http://www.reddit.com/r/technology', params={'after': 't3_'+afterid, 'limit':100});

    except:
        print 'Retry'
        submissions = r.get_content(url='http://www.reddit.com/r/technology', params={'after': 't3_'+afterid, 'limit':100});

'''
with open('output1.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')

    spamwriter.writerow(['id', 'title', 'url', 'score', 'author', 'num_comments','created_utc'])

    for post in submissions:
    	#pprint(vars(post))
        spamwriter.writerow([post.id, (post.title).encode('utf-8'), post.url,post.score, post.author, post.num_comments, post.created_utc])
'''
