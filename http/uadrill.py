#!/usr/bin/env python2.7
# encoding: utf-8
"""
uadrill.py

Created by Karl Dubost on 2013-08-16.
Copyright (c) 2013 Grange. All rights reserved.
MIT License
"""

import logging
import urllib2
import urlparse
import requests

logging.basicConfig(filename='log-survey.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class UriCheck:
    """Some control about URIs from the file"""

    def __init__(self):
        self.uri = ""

    def ishttpURI(self, uri):
        """Given a URI,
        returns True if http or https
        returns False if not http or https"""
        req = urllib2.Request(uri)
        if req.get_type() in ['http', 'https']:
            return True
        else:
            return False

class HttpRequests:
    """Handling HTTP Requests depending on the URI, and User Agent String"""

    def __init__(self):
        self.content = ""
        self.statuscode = ""

    def getRequest(self, uri, uastring):
        """Given a URI and a UA String,
        returns a list with uri, newlocation, statuscode, content"""
        headers = {'User-Agent': uastring}
        r = requests.get(uri, headers=headers)
        statuscode = r.status_code
        responseheaders = r.headers
        history = r.history
        return statuscode, responseheaders, history

    def getContent(self, uri, useragentstring):
        """Return the content associated with an uri"""
        headers = {'User-Agent': useragentstring}
        r = requests.get(uri, headers=headers)
        # r.history contains a list of the different redirections
        # if needed later.
        finaluri = r.url
        responsetext = r.text
        responseheaders = r.headers
        # first test if it's a string
        try:
            isinstance(responsetext, basestring)
        # Log type errors
        except TypeError as e:
            logging.debug("getContent - %s - %s" % (uri, e.message))
        else:
            # then test if it's unicode and convert it
            if isinstance(responsetext, unicode):
                htmltext = responsetext.encode('utf-8')
            # or if not it is just the common text
            elif isinstance(responsetext, str):
                htmltext = responsetext
        return htmltext, finaluri, responseheaders

def main():
    """sequence of actions"""
    uc = UriCheck()
    req = HttpRequests()
    # This needs to be command line input, probably either a list of uri from a file
    # or one uri on the cli
    URILIST = ['http://www.lemonde.fr/', 'http://www.ebay.com/']
    # This needs to be command line input
    UALIST = ['Mozilla/5.0 (Android; Mobile; rv:18.0) Gecko/18.0 Firefox/18.0', ]
    ua = UALIST[0]
    for uri in URILIST:
        uri = uri.strip()
        if uc.ishttpURI(uri):
            logging.info("%s %s" % (uri, ua))
        else:
            logging.debug("%s %s" % (uri, ua))
            uri.next()
        try:
            htmltext, finaluri, responseheaders = req.getContent(uri, ua)
        except requests.exceptions.ConnectionError as e:
            # we are catching network connection error and record them.
            logging.info("Connection error: %s" % (e.message))
        print responseheaders

# >>> r = requests.get('http://github.com', allow_redirects=False)
# We need to be able each redirect and see their content. It's not only a matter of following them blindly.
# We want to be able to trace each steps just the body, just the headers hH, or everything



if __name__ == '__main__':
    main()

