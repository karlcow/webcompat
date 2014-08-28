#!/usr/bin/env python
# encoding: utf-8
"""
bugsweeksummary.py

Created by Karl Dubost on 2014-08-27.
Copyright (c) 2014 La Grange. All rights reserved.
MIT License
"""

import requests
import json
import sys

WIKI_TEMPLATE = '''
== Web Compatibility Progress ==
=== FIXED (no DUPLICATE) ===

{fixed_bugs}

=== NEW ===

{open_bugs}

'''
URL = 'https://bugzilla.mozilla.org/rest/bug?product=Tech%20Evangelism'
BUGID_URL = 'https://bugzilla.mozilla.org/show_bug.cgi?id='
COMPONENTS = ['Desktop', 'Mobile']
URL_COMPONENTS = ''.join(['&component=%s' % i for i in COMPONENTS])
FIELDS = ['id', 'url', 'summary', 'status', 'resolution',
          'creation_time', 'cf_last_resolved', 'component']
URL_FIELDS = '&include_fields='+','.join(['%s' % i for i in FIELDS])
DAYS = 8


def build_uri(bugtype, datespan):
    '''returns a string representing the URI to request.'''
    if bugtype == 'fixed':
        status = ['RESOLVED', 'VERIFIED', 'CLOSED']
        date_field = 'cf_last_resolved'
        # not interested by duplicates
        resolution = ['FIXED', 'INVALID', 'WONTFIX', 'WORKSFORME']
        url_resolution = ''.join(['&resolution=%s' % i for i in resolution])
    elif bugtype == 'open':
        status = ['NEW', 'ASSIGNED', 'UNCONFIRMED']
        date_field = '%5BBug%20creation%5D'
        url_resolution = ''
    else:
        print '%s is not a valid bugtype' % bugtype
        exit(1)
    # Creating the query part of the URL
    url_status = ''.join(['&bug_status=%s' % i for i in status])
    date_from = '-%sd' % datespan
    date_to = 'Now'
    url_date = '&chfield={0}&chfieldfrom={1}&chfieldto={2}'.format(
        date_field,
        date_from,
        date_to)
    return '{url}{components}{status}{resol}{datespan}{fields}'.format(
        url=URL,
        components=URL_COMPONENTS,
        status=url_status,
        resol=url_resolution,
        datespan=url_date,
        fields=URL_FIELDS)


def bugs_request(bugtype, datespan=DAYS):
    '''return a JSON object with the list of bugs
    default time span is one week'''
    url = build_uri(bugtype, datespan)
    bugs_json_array = requests.get(url)
    return bugs_json_array.text


def wiki_markup(bug):
    '''output the Mediawiki markup for Web Compatibility'''
    # Clean up the square brackets to not interfere with wiki links
    clean_summary = bug['summary'].replace('[', '(').replace(']', ')')
    # Common markup
    generic_markup = '{component} [{bugid_url}{id} {summary}]'.format(
        component=bug['component'],
        bugid_url=BUGID_URL,
        id=bug['id'],
        summary=clean_summary
        )
    # Depend on the type of bugs
    if bug['resolution']:
        markup = '* {date} {generic_markup} {resolution}'.format(
            generic_markup=generic_markup,
            date=bug['cf_last_resolved'][:10],
            resolution=bug['resolution'])
    else:
        markup = '* {date} {generic_markup}'.format(
            generic_markup=generic_markup,
            date=bug['creation_time'][:10])
    return markup


def main():
    '''core program'''
    # New bugs
    openbugs = json.loads(bugs_request('open', DAYS))['bugs']
    markupo = '\n'.join(sorted([wiki_markup(bug) for bug in openbugs]))
    # Fixed bugs
    fixedbugs = json.loads(bugs_request('fixed', DAYS))['bugs']
    markupf = '\n'.join(sorted([wiki_markup(bug) for bug in fixedbugs]))
    # Printing the text
    print WIKI_TEMPLATE.format(
        fixed_bugs=markupf,
        open_bugs=markupo
        )


if __name__ == "__main__":
    sys.exit(main())
