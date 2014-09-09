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

MINUTES_TEMPLATE = '''
* [[Compatibility/Mobile|Mobile Web Compatibility]] Meeting - {meeting_date}
* [[Compatibility/Mobile#Minutes_and_Progress_Reports|Minutes]]:
[[Compatibility/Mobile/{previous_week}|Previous {previous_week}]]

== Minutes ==
{minutes}
=== Heads Up ===
create_summary_here

== Broken Voices of the Web ==
{broken_voices}
{bugs_summary}
'''


def meeting_date(mdate=None):
    '''return the meeting date if not given'''
    if not mdate:
        return date.today()


def previous_meeting(mtoday):
    '''return the date of the previous meeting'''
    return (mtoday - timedelta(days=7)).isoformat()


def meeting_minutes():
    '''Create the meeting minutes'''
    minutes = None
    return minutes


def wiki_markup():
    '''return the final wiki markup'''
    mtoday = meeting_date()
    today_iso = mtoday.isoformat()

    return MINUTES_TEMPLATE.format(
        meeting_date=today_iso,
        previous_week=previous_meeting(mtoday),
        minutes=meeting_minutes(),
        broken_voices=extractfeedtitle.broken_voices(),
        bugs_summary=bugsweeksummary.summary()
        )


def main():
    '''core program'''
    print wiki_markup()


if __name__ == "__main__":
    sys.exit(main())
