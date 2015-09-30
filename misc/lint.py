#!/usr/bin/env python3
"""Check for tabs and trailing whitespace in text files in all subdirs.

Any other automatic checks should be in this file too.
"""

import os
from os.path import *
import sys

text_extensions = ('rst', 'md', 'txt', 'html', 'css', 'js')

def lint(path):
    """Run linters on all files, print problem files."""
    print('Checking for tabs or trailing whitespace...')
    failed = False
    for root, _, files in os.walk(path):
        for f in files:
            fname = join(root, f)
            if '_build' in fname or not any(
                    fname.endswith(ext) for ext in text_extensions):
                continue
            with open(fname, encoding='utf-8') as fh:
                if '\t' in fh.read():
                    failed = True
                    print('ERROR:  tabs found in {}'.format(fname))
                if any(line.replace('\n', '') != line.rstrip()
                       for line in fh.readlines()):
                    failed = True
                    print('ERROR:  trailing whitespace in {}'.format(fname))
                fh.seek(0)
                for i, line in enumerate(fh.readlines()):
                    if len(line) > 81:
                        failed = True
                        print('ERROR:  {}:{} - line too long'.format(
                              fname, i + 1))
    if failed:
        print('Use your text editor to convert tabs to spaces, wrap lines '
              'or trim trailing whitespace with minimal effort.')
        sys.exit(failed)
    print('All files are OK')


if __name__ == '__main__':
    # lint everything in the parent directory, wherever the script is run from.
    p = relpath(join(dirname(__file__), '..'))
    lint(p)
