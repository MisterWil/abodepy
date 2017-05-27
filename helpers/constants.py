'''
constants.py
Generates constants for use in blinkpy
'''
import os

MAJOR_VERSION = 0
MINOR_VERSION = 1
PATCH_VERSION = '0.dev'

__version__ = '{}.{}.{}'.format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

REQUIRED_PYTHON_VER = (3, 4, 2)

PROJECT_NAME = 'abodepy'
PROJECT_PACKAGE_NAME = 'abodepy'
PROJECT_LICENSE = 'MIT'
PROJECT_AUTHOR = 'Wil Schrader'
PROJECT_COPYRIGHT = ' 2017, {}'.format(PROJECT_AUTHOR)
PROJECT_URL = 'https://github.com/MisterWil/abodepy'
PROJECT_EMAIL = 'wilrader@gmail.com'
PROJECT_DESCRIPTION = ('An Abode alarm Python library '
                       'running on Python 3.')
PROJECT_LONG_DESCRIPTION = ('abodepy is an open-source '
                            'unofficial API for the Abode alarm '
                            'system with the intention for easy '
                            'integration into various home '
                            'automation platforms.')
if os.path.exists('README.rst'):
    PROJECT_LONG_DESCRIPTION = open('README.rst').read()
PROJECT_CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.4',
    'Topic :: Home Automation'
]

PROJECT_GITHUB_USERNAME = 'MisterWil'
PROJECT_GITHUB_REPOSITORY = 'abodepy'

PYPI_URL = 'https://pypi.python.org/pypi/{}'.format(PROJECT_PACKAGE_NAME)

'''
URLS
'''
BLINK_URL = 'immedia-semi.com'
LOGIN_URL = 'https://prod.' + BLINK_URL + '/login'
LOGIN_BACKUP_URL = 'https://rest.piri/' + BLINK_URL + '/login'
BASE_URL = 'https://prod.' + BLINK_URL
DEFAULT_URL = 'prod.' + BLINK_URL

'''
Dictionaries
'''
ONLINE = {'online': True, 'offline': False}