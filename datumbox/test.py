#!/usr/bin/python

import sys
import requests
import re

from DatumBox import DatumBox

def stripTags(text):
  scripts = re.compile(r'<script.*?/script>')
  css = re.compile(r'<style.*?/style>')
  tags = re.compile(r'<.*?>')

  text = scripts.sub(' ', text)
  text = css.sub(' ', text)
  text = tags.sub(' ', text)

  return text


request = requests.get(sys.argv[1])
content = request.text
#content = '<script>sddd</script><style sdfsafs>sfsdfsfs</style>my text<be>betkk</be>'
content = content.encode('utf-8')
print content
raw_content = stripTags(content)
print raw_content

db = DatumBox('9eb37f7399b4d074c5b83358f24ba626')
res = db.twitter_sentiment_analysis(raw_content)
print res


