#!/usr/bin/env python
# encoding: utf-8
"""
minutes.py

Created by Karl Dubost on 2014-09-25.
Copyright (c) 2014 La Grange. All rights reserved.
MIT License

We want:

1. Import
https://etherpad.mozilla.org/ep/pad/export/webcompat/latest?format=txt
2. Extract the effective minutes from the text
3. Extract the date
4. Convert the text to the appropriate format
"""

import requests
import sys
WIKI_TEMPLATE = '''== Minutes =='''
URL = 'https://etherpad.mozilla.org/ep/pad/export/webcompat/latest?format=txt'
SERVER_URL = 'https://etherpad.mozilla.org'
def etherpad_content(server_uri, pad_name, pad_format='txt'):
    '''Fetch the text version of the etherpad.'''
    url = '{0}/ep/pad/export/{1}/latest?format={2}'.format(server_uri,
                                                           pad_name,
                                                           pad_format)
    content = requests.get(url)
    return content.text
def main():
    '''core program'''
    # Fetch the content online
    raw_content = etherpad_content(SERVER_URL, 'webcompat', 'txt')
if __name__ == "__main__":
    sys.exit(main())
