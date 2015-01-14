#!/usr/bin/env python
# encoding: utf-8
"""
extractfeedtitle.py

Created by Karl Dubost on 2013-12-16.
Copyright (c) 2013 La Grange. All rights reserved.
MIT License
"""

import sys
import feedparser
from datetime import date
from datetime import datetime

URL = 'http://planet.webcompat.com/atom.xml'
today = date.today()
todayobj = datetime.combine(today, datetime.min.time())
feed = feedparser.parse(URL)


def broken_voices():
    '''Create the markup for the feed of the week'''
    voice_markup = ''
    for item in feed['items']:
        postdate = item['date']
        shortdate = postdate[0:10]
        dateobj = datetime.strptime(postdate, '%Y-%m-%dT%H:%M:%SZ')
        publishedago = todayobj-dateobj
        if publishedago.days < 8:
            postlink = item['link']
            title = item['title']
            title = title.replace('[', '(')
            title = title.replace(']', ')')
            voice_markup += "* %s - [%s %s]\n" % (shortdate, postlink, title)
    return voice_markup.encode('utf-8')


def main():
    '''core program'''
    print broken_voices()


if __name__ == "__main__":
    sys.exit(main())
