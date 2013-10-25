import re
import sys
import json
import urllib2
import argparse


parser = argparse.ArgumentParser(description='Download tvp.pl video')
parser.add_argument('url', action='store', metavar='URL')

args = parser.parse_args()

try:
    response = urllib2.urlopen(args.url)
    html = response.read()
    match = re.search (r"object_id:'(.*)'", html)
    if match:
        id = match.group(1)
        response = urllib2.urlopen('http://www.tvp.pl/shared/cdn/tokenizer_v2.php?object_id=%s' % id)
        result = json.loads(response.read())

        url = result.get('url')
        title = result.get('title')
        file_name = '%s.wmv' % title

        print "Saving to %s ..." % file_name

        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            p = float(file_size_dl) / file_size
            status = "Downloading: {0} Bytes: {1}, {2}  [{3:.2%}]".format(url, file_size, file_size_dl, p)
            status = status + chr(8)*(len(status)+1)
            print status

        f.close()

except urllib2.HTTPError, e:
    if e.code == 404:
        print "invalid url: ", e.url
    else:
        raise
