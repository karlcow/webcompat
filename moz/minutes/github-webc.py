#!/usr/bin/env python
# encoding: utf-8
"""
github-webc.py
Extracts some data from our GitHub project


Created by Karl Dubost on 2016-02-24.
Copyright (c) 2016 La Grange. All rights reserved.
MIT License
"""

from datetime import datetime
import sys

from lxml.cssselect import CSSSelector
import helpers

LABELS_URI = 'https://github.com/webcompat/web-bugs/labels'
LABELS_LIST = ['needsinfo', 'needsdiagnosis', 'needscontact', 'contactready',
               'sitewait']
ISSUES_COUNT = 0
TEMPLATE = '''Today: {date}
{open} open issues
----------------------
needsinfo       {info}
needsdiagnosis  {diag}
needscontact    {contact}
contactready    {ready}
sitewait        {wait}
----------------------
'''


def extract_issues_count(github_html):
    '''extracts the total number of opened issues'''
    sel = CSSSelector('a[data-selected-links*=repo_issues] .counter')
    count_span = sel(github_html)[0]
    return count_span.text


def extract_labels_count(github_html, LABELS_LIST):
    '''extracts each valid label with their own count.'''
    LABELS_LIST = ['status-' + label for label in LABELS_LIST]
    sel_description = CSSSelector('.label-description')
    sel_name = CSSSelector('.label-name')
    # We remove (split) all characters after the first space
    labels_count = [count.text.split(' ', 1)[0]
                    for count in sel_description(github_html)]
    labels_name = [name.text for name in sel_name(github_html)]
    # The two lists have the same length, we zip them.
    # And we select only the ones from the LABELS_LIST
    labels = [label for label in zip(labels_name, labels_count)
              if label[0] in LABELS_LIST]
    return dict(labels)


def format_data(issues_count, labels, TEMPLATE):
    '''Returns a ready to paste list of data'''
    today = datetime.now()
    iso = today.isoformat()
    print TEMPLATE.format(date=iso,
                          open=issues_count,
                          info=labels['status-needsinfo'],
                          diag=labels['status-needsdiagnosis'],
                          contact=labels['status-needscontact'],
                          ready=labels['status-contactready'],
                          wait=labels['status-sitewait'])


def main():
    '''core program'''
    content, html_encoding = helpers.fetch_content(LABELS_URI)
    github_html = helpers.html_parse(content)
    # Some data
    issues_count = extract_issues_count(github_html)
    labels = extract_labels_count(github_html, LABELS_LIST)
    format_data(issues_count, labels, TEMPLATE)


if __name__ == "__main__":
    sys.exit(main())
