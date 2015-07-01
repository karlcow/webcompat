#!/usr/bin/env python
# encoding: utf-8
"""
Compute the differences in between images.

Take a list of files in a directory with BEFORE AFTER naming
and compute the difference according to a ratio.
"""

import argparse
import os


def cli():
    "Parse the arguments on the commandline."
    parser = argparse.ArgumentParser(description="Compute image differences.")
    parser.add_argument('-p', action='store', dest='dir_path',
                        help='Directory path where are the files')
    args = parser.parse_args()
    return args


def images_list(dir_path):
    """Create an image list of the directory content.

    The list will collect only the filename prefix.
    """
    prefix_list = [filename[:-11] for filename in os.listdir(dir_path)
                   if filename.endswith('-BEFORE.png')]
    return prefix_list


def main():
    """Main."""
    # Let's parse the command line
    args = cli()
    # we get the directory
    dir_path = args.dir_path
    prefix_list = images_list(dir_path)


if __name__ == "__main__":
    main()
