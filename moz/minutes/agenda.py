#!/usr/bin/env python
# encoding: utf-8
"""
agenda.py
Will create an agenda to be discussed for next meeting


Created by Karl Dubost on 2015-04-02.
Copyright (c) 2015 La Grange. All rights reserved.
MIT License
"""

import sys
from datetime import date, timedelta
# import bugsweeksummary
# import extractfeedtitle
import minutes

MAIL_TEMPLATE = '''
--MAIL SUBJECT-------------------------------------------------
[Agenda] {human_date} Web Compatibility Meeting
--MAIL BODY----------------------------------------------------
# Web Compatibility Meeting on {meeting_date} at 13:00 UTC
## Agenda (preliminary)

{minutes}

More items: https://etherpad.mozilla.org/webcompat
Last Week:  https://wiki.mozilla.org/Compatibility/Mobile/{previous_week}
Schedule:   <http://timesched.pocoo.org/?date={meeting_date}&tz=us:san-francisco:ca,us:austin:tx,ca:toronto,utc!,fr:paris,tw:taipei,jp:tokyo,nz:auckland&range=780,840>

---------------------------------------------------------------
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
    # Fetch the content online
    SERVER_URL = 'https://public.etherpad-mozilla.org'
    raw_content, encoding = minutes.etherpad_content(SERVER_URL, 'webcompat', 'txt')
    # Extract the Multimarkdon part of the body
    md_content = minutes.extract_minutes(raw_content)
    minutes_txt = minutes.parse_minutes(md_content['text'], 'email')
    return minutes_txt


def email_markup():
    '''return the final wiki markup'''
    mtoday = meeting_date()
    dformat = "%d %B %Y"
    human_date = date.today().strftime(dformat)
    if human_date.startswith('0'):
        human_date = human_date[1:]
    today_iso = mtoday.isoformat()
    print('Preparing Meeting Minutes')
    meet_minutes = meeting_minutes()
    print('Preparing email')
    return MAIL_TEMPLATE.format(
        human_date=human_date,
        meeting_date=today_iso,
        previous_week=previous_meeting(mtoday),
        minutes=meet_minutes
        )


def main():
    '''core program'''
    print(email_markup())


if __name__ == "__main__":
    sys.exit(main())
