#!/usr/bin/env python

"""Handle minifying all javascript files in the build directory by walking

$ jsmin_all.py $lp_js_root

"""

from __future__ import absolute_import, print_function

import argparse
import os
import re
import sys

from .jsmin import JavascriptMinify

MIN_FILECHANGE = '-min.js'

__all__ = ['main', 'minify', 'minify_stream']


def dirwalk(dir):
    """Walk a directory tree, using a generator of files"""
    for f in os.listdir(dir):
        fullpath = os.path.join(dir, f)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            for x in dirwalk(fullpath):  # recurse into subdir
                if x.endswith('.js'):
                    yield x
        else:
            if fullpath.endswith('.js'):
                yield fullpath


def is_min(filename):
    """Check if this file is alrady a minified file"""
    return filename.endswith('min.js')


def minify(filename):
    """Given a filename, handle minifying it as -min.js"""
    if not is_min(filename):
        new_filename = re.sub(".js$", MIN_FILECHANGE, filename)

        with open(filename) as shrink_me:
            with open(new_filename, 'w') as tobemin:
                jsm = JavascriptMinify()
                jsm.minify(shrink_me, tobemin)


def minify_stream(instream, outstream):
    """Given an input/output stream, minify the JS"""
    jsm = JavascriptMinify()
    jsm.minify(instream, outstream)


def _parse_args():
    """Process args with argparse"""
    desc = """Minify Javascript.

    You can either pass --path/-p or read from stdin.
    """

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--path', '-p',
        dest='path',
        action='store',
        default=None,
        required=False,
        help='Specify the path to minimize (directory or file)')
    args = parser.parse_args()
    return args


def main():
    args = _parse_args()

    if args.path:
        root = args.path

        if os.path.isfile(root):
            minify(root)
        else:
            [minify(f) for f in dirwalk(root)]
    else:
        jsm = JavascriptMinify()
        jsm.minify(sys.stdin, sys.stdout)


if __name__ == '__main__':
    main()
