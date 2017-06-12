"""
constants.py

Generates constants for use in abodepy
"""
import os

MAJOR_VERSION = 0
MINOR_VERSION = 5
PATCH_VERSION = '1'

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
BASE_URL = 'https://my.goabode.com/'

LOGIN_URL = BASE_URL + 'api/auth2/login'
LOGOUT_URL = BASE_URL + 'api/v1/logout'

PANEL_URL = BASE_URL + 'api/v1/panel'


def PANEL_MODE_URL(area, mode):
    return BASE_URL + 'api/v1/panel/mode/' + area + '/' + mode


DEVICES_URL = BASE_URL + 'api/v1/devices'
DEVICE_URL = BASE_URL + 'api/v1/devices/$DEVID$'

AREAS_URL = BASE_URL + 'api/v1/areas'

'''
NOTIFICATION CONSTANTS
'''
SOCKETIO_URL = 'https://my.goabode.com'

SOCKETIO_HEADERS = {
    'Origin': 'https://my.goabode.com'
    }

DEVICE_UPDATE_EVENT = 'com.goabode.device.update'
GATEWAY_MODE_EVENT = 'com.goabode.gateway.mode'

'''
DICTIONARIES
'''
MODE_STANDBY = 'standby'
MODE_HOME = 'home'
MODE_AWAY = 'away'

ALL_MODES = [MODE_STANDBY, MODE_HOME, MODE_AWAY]

ALL_MODES_STR = ", ".join(ALL_MODES)

ARMED = {'home': True, 'away': True, 'standby': False}

STATUS_ONLINE = 'Online'
STATUS_OFFLINE = 'Offline'

STATUS_OPEN = 'Open'
STATUS_OPEN_INT = 1
STATUS_CLOSED = 'Closed'
STATUS_CLOSED_INT = 0

STATUS_LOCKOPEN = 'LockOpen'
STATUS_LOCKOPEN_INT = 0
STATUS_LOCKCLOSED = 'LockClosed'
STATUS_LOCKCLOSED_INT = 1

STATUS_ON = 'On'
STATUS_ON_INT = 1
STATUS_OFF = 'Off'
STATUS_OFF_INT = 0
