#!/usr/bin/env python
# encoding: utf-8
"""
minutes_skeleton.py
Will generate the minutes for the week.


Created by Karl Dubost on 2014-09-02.
Copyright (c) 2014 La Grange. All rights reserved.
MIT License
"""

import sys
from datetime import date, timedelta
import bugsweeksummary
import extractfeedtitle
import minutes

MINUTES_TEMPLATE = '''
* [[Compatibility|Web Compatibility]] Meeting - {meeting_date}
* [[Compatibility/Meetings|Minutes]]: [[Compatibility/Meetings/{previous_week}|Previous {previous_week}]]

== Minutes ==
{minutes}

== Broken Voices of the Web ==
{broken_voices}
{bugs_summary}
'''  # nopep8


def meeting_date(mdate=None):
    '''return the meeting date if not given'''
    if not mdate:
        return date.today()


def previous_meeting(mtoday):
    '''return the date of the previous meeting'''
    return (mtoday - timedelta(days=7)).isoformat()


def meeting_minutes():
    '''Create the meeting minutes'''
    minutes_txt = minutes.main()
    return minutes_txt


def wiki_markup():
    '''return the final wiki markup'''
    mtoday = meeting_date()
    today_iso = mtoday.isoformat()
    print('Preparing Meeting Minutes')
    meet_minutes = meeting_minutes()
    print('Preparing blogs summary')
    blogs = extractfeedtitle.broken_voices()
    print('Preparing bugs summary')
    bugs = bugsweeksummary.summary()
    return MINUTES_TEMPLATE.format(
        meeting_date=today_iso,
        previous_week=previous_meeting(mtoday),
        minutes=meet_minutes,
        broken_voices=blogs,
        bugs_summary=bugs)


def main():
    '''core program'''
    print(wiki_markup())


if __name__ == "__main__":
    sys.exit(main())
