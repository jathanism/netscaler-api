#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command
import os
import sys

__version__ = "0.2.3"

if sys.version_info[:2] < (2, 4):
    print "This package requires Python 2.4+. Sorry!"
    sys.exit(-11)

class CleanCommand(Command):
    description = "cleans up non-package files. (dist, build, etc.)"
    user_options = []
    def initialize_options(self):
        self.files = None
    def finalize_options(self):
        self.files = './build ./dist ./MANIFEST ./*.pyc examples/*.pyc ./*.egg-info'
    def run(self):
        print 'Cleaning: %s' % self.files
        os.system('rm -rf ' + self.files)

setup(
    name = 'netscaler-api',
    version = __version__,
    url = 'http://github.com/jathanism/netscaler-api/',
    license = 'BSD',
    description = "NetScaler API is a Python interface for interacting with Citrix NetScaler application delivery controllers, utilizing the SOAP API to execute commands.",
    author = 'Jathan McCollum',
    author_email = 'jathan@gmail.com',
    py_modules = ['netscaler'],
    install_requires=['suds>=0.3.9'],
    keywords = [
            'Networking', 'Automation', 'library', 'Security', 'NetScaler', 'API', 'SOAP',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Education :: Testing',
        'Topic :: Internet',
        'Topic :: Security',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Operating System',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    cmdclass = {
        'clean': CleanCommand,
    }
)
