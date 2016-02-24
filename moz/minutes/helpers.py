#!/usr/bin/env python
# encoding: utf-8
"""
helpers.py
Some modules to help with this project


Created by Karl Dubost on 2016-02-24.
Copyright (c) 2016 La Grange. All rights reserved.
MIT License
"""
import requests
def fetch_content(uri):
    '''Fetch the URI and returns the raw content and its encoding'''
    content = requests.get(uri)
    return content.text, content.encoding
def main():
    '''core program'''
    pass

if __name__ == "__main__":
    sys.exit(main())
