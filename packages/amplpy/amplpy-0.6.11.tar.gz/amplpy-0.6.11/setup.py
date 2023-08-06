# -*- coding: utf-8 -*-
"""
AMPLPY
------

AMPL API is an interface that allows developers to access the features of the
AMPL interpreter from within a programming language. All model generation and
solver interaction is handled directly by AMPL, which leads to great stability
and speed; the library just acts as an intermediary, and the added overhead
(in terms of memory and CPU usage) depends mostly on how much data is read
back from AMPL, the size of the model as such is irrelevant. Functions for
directly assigning data to AMPL parameters and sets are provided, which can
be used instead of the normal AMPL data reading procedures.  AMPL API has been
written with usability in mind, and it is easy to access its functionalities
from C++, Java, C#, MATLAB, R and Python.

The AMPL API can function as an add-on to any existing AMPL installation. If
you do not yet have an AMPL installation on the computer where you will be
working with the API, see our
`demo page <http://ampl.com/try-ampl/download-a-free-demo/>`_
or
`trial page <http://ampl.com/try-ampl/request-a-full-trial/>`_
to download a working version that can be installed quickly.

Documentation:
``````````````

* http://amplpy.readthedocs.io
* http://ampl.com/api/nightly/python/

Repositories:
`````````````

* GitHub Repository: https://github.com/ampl/amplpy
* PyPI Repository: https://pypi.python.org/pypi/amplpy
"""
from setuptools import setup, Extension
import platform
import sys
import os

OSTYPE = platform.system()
ARCH = platform.processor()
x64 = platform.architecture()[0] == '64bit'

if ARCH == 'ppc64le':
    LIBRARY = 'ppc64le'
else:
    LIBRARY = 'amd64' if x64 else 'intel32'

if OSTYPE == 'Darwin':
    LIBRARY_EXT = '.dylib'
elif OSTYPE == 'Linux':
    LIBRARY_EXT = '.so'
else:
    LIBRARY_EXT = '.dll'

CPP_BASE = os.path.join('amplpy', 'amplpython', 'cppinterface')
LIBRARY_BASE = os.path.join(CPP_BASE, 'lib')
LIBRARY_DIR = os.path.join(LIBRARY_BASE, LIBRARY)


def ls_dir(base_dir):
    """List files recursively."""
    return [
        os.path.join(dirpath, fname)
        for (dirpath, dirnames, files) in os.walk(base_dir)
        for fname in files
    ]


def package_content():
    all_files = ls_dir('amplpy/')
    if 'sdist' in sys.argv:
        lst = all_files
    else:
        source_only = [
            fpath for fpath in all_files
            if not fpath.startswith(LIBRARY_BASE)
        ]
        library_only = [
            fpath for fpath in all_files
            if fpath.startswith(LIBRARY_DIR)
            if LIBRARY_EXT in fpath[fpath.rfind('/'):]
        ]
        lst = source_only + library_only
    return [
        fpath.replace('amplpy/', '', 1)
        for fpath in lst
    ]


def make_relative_rpath(path):
    if OSTYPE == 'Darwin':
        return '-Wl,-rpath,@loader_path/' + path
    elif OSTYPE == 'Linux':
        return '-Wl,-rpath,$ORIGIN/' + path
    else:
        return ''


def compile_args():
    if OSTYPE == 'Windows':
        return ['/TP /EHsc']
    elif OSTYPE == 'Linux':
        ignore_gcc8_warnings = [
            '-Wno-stringop-truncation', 
            '-Wno-catch-value'
        ]
        return ['-std=c++11'] + ignore_gcc8_warnings
    else:
        return []


setup(
    name='amplpy',
    version='0.6.11',
    description='Python API for AMPL',
    long_description=__doc__,
    license='BSD-3',
    platforms='any',
    author='Filipe Brandão',
    author_email='fdabrandao@ampl.com',
    url='http://ampl.com/',
    download_url='https://github.com/ampl/amplpy',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: C++',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=['amplpy'],
    ext_modules=[Extension(
        '_amplpython',
        libraries=['ampl'],
        library_dirs=[os.path.join(LIBRARY_BASE, LIBRARY)],
        include_dirs=[os.path.join(CPP_BASE, 'include')],
        extra_compile_args=compile_args(),
        extra_link_args=[
            make_relative_rpath(os.path.join(LIBRARY_BASE, LIBRARY))
        ],
        sources=[
            os.path.join(CPP_BASE, 'amplpythonPYTHON_wrap.cxx')
        ],
    )],
    package_data={'': package_content()},
    install_requires=['future >= 0.15.0']
)
