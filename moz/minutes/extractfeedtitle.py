#!/usr/bin/env python
# encoding: utf-8
"""
extractfeedtitle.py

Created by Karl Dubost on 2013-12-16.
Copyright (c) 2013 La Grange. All rights reserved.
MIT License
"""

import feedparser
from datetime import date
from datetime import datetime

URL = 'http://planet.webcompat.com/atom.xml'
today = date.today()
todayobj = datetime.combine(today, datetime.min.time())

feed = feedparser.parse(URL)
for item in feed['items']:
    postdate = item['date']
    shortdate = postdate[0:10]
    dateobj = datetime.strptime(postdate, '%Y-%m-%dT%H:%M:%SZ')
    publishedago = todayobj-dateobj
    if publishedago.days < 7:
        postlink = item['link']
        title = item['title']
        title = title.replace('[', '(')
        title = title.replace(']', ')')
        print "* %s - [%s %s]" % (shortdate, postlink, title)
