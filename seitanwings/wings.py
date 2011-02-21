# url, line, line number, syllables, ...
# in memory hash of seen urls
# doc per line
import re
import urllib2
import urlparse

import pymongo
from BeautifulSoup import BeautifulSoup

# sync URL hashtable with mongo
# given a url
# parse, add each line to mongo

seen_urls = {}
url_queue = []
start_url = 'http://www.google.com/Top/Arts/'

url_queue.append(start_url)
iterations = 100

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

protocol = 'http://'

while len(url_queue) > 0 and iterations > 0:
    url = url_queue.pop(0)
    if seen_urls.get(url, False):
        print "Already seen %s, continuing" % url
        continue

    try:
        data = opener.open(url).read()
    except (urllib2.HTTPError, ValueError, urllib2.URLError):
        print "Got an HTTP error for %s, continuing" % url
        continue
    root = urlparse.urlparse(url).netloc
    soup = BeautifulSoup(data)
    # parse content
    # add docs to mongo
    seen_urls[url] = True
    for link in soup.findAll('a'):
        if link.has_key('href'):
            link = link['href']
            if not link.startswith('http://'):
                link = protocol + root + link
            url_queue.append(link)
    iterations -= 1

print seen_urls
