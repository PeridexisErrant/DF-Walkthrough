#!/usr/bin/env python3
"""Check for tabs and trailing whitespace in text files in all subdirs.

Any other automatic checks should be in this file too.
"""

from glob import glob
from io import open
import os
from os.path import *
import sys

text_extensions = ('rst', 'md', 'txt', 'html', 'css', 'js')


def error(fname, lineno, issue):
    """Print the problem and location."""
    print('ERROR:  {}:{} - {}'.format(fname, lineno+1, issue))


def lint(path):
    """Run linters on all files, print problem files."""
    print('Checking for long lines, tabs, and trailing whitespace...')
    failed = False
    for root, _, files in os.walk(path):
        for f in files:
            fname = join(root, f)
            if '_build' in fname or not any(
                    fname.endswith(ext) for ext in text_extensions):
                continue
            with open(fname, encoding='utf-8') as fh:
                for i, line in enumerate(fh.readlines()):
                    if len(line) > 81:
                        failed = True
                        error(fname, i, 'too long')
                    if line.replace('\n', '') != line.rstrip():
                        failed = True
                        error(fname, i, 'trailing space')
                    if '\t' in line:
                        error(fname, i, 'contains tab')
    if failed:
        print('Use your text editor to convert tabs to spaces, wrap lines '
              'or trim trailing whitespace with minimal effort.')
    return failed


def unused_images(path):
    """Check that all files in image subdirs are references in the text."""
    print('Checking for unused images...')
    failed = False
    dirs = ['chapters', 'tutorials']
    for d in dirs:
        text = ''
        for fname in glob(os.path.join(d, '*.rst')):
            with open(fname, encoding='utf-8') as f:
                text += f.read()
        for img in glob(os.path.join(d, 'images', '*.*')):
            img = os.path.basename(img)
            if img == 'Thumbs.db':
                continue
            markup = '.. image:: images/{}'.format(img)
            if markup not in text:
                failed = True
                print('Error:  image not referenced, {}/{}/{}'.format(
                      d, 'images', img))
    if failed:
        print('Use or or delete these images.')
    return failed


if __name__ == '__main__':
    # lint everything in the parent directory, wherever the script is run from.
    p = relpath(join(dirname(__file__), '..'))
    sys.exit(lint(p) or unused_images(p))
