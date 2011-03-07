# url, line, line number, syllables, ...
# in memory hash of seen urls
# doc per line
# query strings?
import urllib2
import urlparse

import pymongo
from BeautifulSoup import BeautifulSoup

# sync URL hashtable with mongo
# given a url
# parse, add each line to mongo

connection = pymongo.Connection()
db = connection.wings_test
pages = db.pages

seen_urls = {}
url_queue = []
start_url = 'http://www.google.com/Top/Arts/'

url_queue.append(start_url)
iterations = 10

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

while len(url_queue) > 0 and iterations > 0:
    url = url_queue.pop(0)

    try:
        data = opener.open(url).read()
    except (urllib2.HTTPError, ValueError, urllib2.URLError):
        print "Got an HTTP error for %s, continuing" % url
        continue
    parsed_url = urlparse.urlparse(url)
    (scheme, root, path) = (parsed_url.scheme, parsed_url.netloc, parsed_url.path)
    # parse content
    soup = BeautifulSoup(data)
    page = {
        'url':url,
        # XXX
    }
    pages.insert(page)
    seen_urls[url] = True
    for link in soup.findAll('a'):
        if not link.has_key('href'):
            continue

        link = link['href']
        base = scheme + '://' + root
        if link.startswith('/'):
            link = urlparse.urljoin(base, link)
        elif link.startswith('http://'):
            pass
        else:
            absolute = urlparse.urljoin(base, path)
            link = urlparse.urljoin(absolute, link)

        if not seen_urls.get(link):
            url_queue.append(link)
    iterations -= 1

print seen_urls
