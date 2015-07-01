#!/usr/bin/env python
# encoding: utf-8
"""
Compute the differences in between images.

Take a list of files in a directory with BEFORE AFTER naming
and compute the difference according to a ratio.
"""

import argparse
import difflib
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


def diff_ratio(s1, s2):
    """Compute the diff ratio in between two images."""
    s = difflib.SequenceMatcher(None, s1, s2)
    return s.quick_ratio()


def image_tuple(prefix, dir_path):
    """Create a tuple of full path for images."""

    path_before = os.path.join(dir_path, prefix + '-BEFORE.png')
    path_after = os.path.join(dir_path, prefix + '-AFTER.png')
    return path_before, path_after


def main():
    """Main."""
    # Let's parse the command line
    args = cli()
    # we get the directory
    dir_path = args.dir_path
    prefix_list = images_list(dir_path)


if __name__ == "__main__":
    main()
