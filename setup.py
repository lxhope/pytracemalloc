#!/usr/bin/env python

# Todo list to prepare a release:
#  - run unit tests
#  - update VERSION in _tracemalloc.c and setup.py
#  - reset option in setup.py: DEBUG=False
#  - set release date in the README.rst file
#  - git commit -a
#  - git tag -a pytracemalloc-VERSION
#  - git push --tags
#  - python setup.py register sdist upload
#
# After the release:
#  - set version to n+1
#  - add a new empty section in the changelog for version n+1
#  - git commit
#  - git push

from __future__ import with_statement
from distutils.core import setup, Extension
import ctypes
import os
import subprocess
import sys

# Define TRACE_RAW_MALLOC  (experimental option): yes, I like to call
# PyGILState_Ensure() when the GIL is released, to track PyMem_RawMalloc() and
# PyMem_RawRealloc() memory!
TRACE_RAW_MALLOC = True

# Debug pytracemalloc
DEBUG = True

VERSION = '1.0dev'

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Topic :: Security',
    'Topic :: Software Development :: Debuggers',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

def pkg_config(name, arg, strip_prefix=0):
    args = ['pkg-config', name, arg]
    process = subprocess.Popen(args,
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    stdout, stderr = process.communicate()
    exitcode = process.wait()
    if exitcode:
        sys.exit(exitcode)
    args = stdout.strip().split()
    if strip_prefix:
        args = [item[strip_prefix:] for item in args]
    return args

def main():
    pythonapi = ctypes.cdll.LoadLibrary(None)
    if not hasattr(pythonapi, 'PyMem_SetAllocator'):
        print("PyMem_SetAllocator: missing, %s has not been patched" % sys.executable)
        sys.exit(1)
    else:
        print("PyMem_SetAllocator: present")

    cflags = []
    if TRACE_RAW_MALLOC:
        cflags.append('-DTRACE_RAW_MALLOC')
    if not DEBUG:
        cflags.append('-DNDEBUG')

    with open('README.rst') as f:
        long_description = f.read().strip()

    ext = Extension(
        '_tracemalloc',
        ['_tracemalloc.c'],
        libraries=libraries,
        extra_compile_args = cflags)

    options = {
        'name': 'pytracemalloc',
        'version': VERSION,
        'license': 'MIT license',
        'description': 'Track memory allocations per Python file',
        'long_description': long_description,
        'url': 'http://www.wyplay.com/',
        'download_url': 'https://github.com/wyplay/pytracemalloc',
        'author': 'Victor Stinner',
        'author_email': 'vstinner@wyplay.com',
        'ext_modules': [ext],
        'classifiers': CLASSIFIERS,
        'py_modules': ["tracemalloc"],
    }
    setup(**options)

if __name__ == "__main__":
    main()

