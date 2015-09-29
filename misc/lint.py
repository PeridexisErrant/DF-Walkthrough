#!/usr/bin/env python3
"""Check for tabs and trailing whitespace in text files in all subdirs.

Any other automatic checks should be in this file too.
"""

import os
import sys

text_extensions = ('rst', 'md', 'txt', 'html', 'css', 'js')


def lint():
    """Run linters on all files, print problem files."""
    print('Checking for tabs or trailing whitespace...')
    failed = False
    for root, _, files in os.walk('.'):
        for f in files:
            fname = os.path.join(root, f)
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
    if failed:
        print('Use your text editor to convert tabs to spaces '
              'or trim trailing whitespace with minimal effort.')
        sys.exit(failed)
    print('All files are OK')


if __name__ == '__main__':
    lint()
