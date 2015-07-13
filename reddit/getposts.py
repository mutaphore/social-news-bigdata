# to run this script, install praw first: pip install praw
import praw
import csv
from pprint import pprint

r = praw.Reddit(user_agent='my_cool_application')
submissions = r.get_subreddit('technology').get_top(limit=2000)

with open('output.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')

    spamwriter.writerow(['id', 'title', 'url', 'score', 'author', 'num_comments','created_utc'])

    for post in submissions:
    	#pprint(vars(post))
        spamwriter.writerow([post.id, (post.title).encode('utf-8'), post.url,post.score, post.author, post.num_comments, post.created_utc])
