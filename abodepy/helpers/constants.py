"""AbodePy constants."""
import os

MAJOR_VERSION = 1
MINOR_VERSION = 2
PATCH_VERSION = '0'

__version__ = '{}.{}.{}'.format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

REQUIRED_PYTHON_VER = (3, 6, 0)

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
    with open('README.rst') as f:
        PROJECT_LONG_DESCRIPTION = f.read()
PROJECT_CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.6',
    'Topic :: Home Automation'
]

PROJECT_GITHUB_USERNAME = 'MisterWil'
PROJECT_GITHUB_REPOSITORY = 'abodepy'

PYPI_URL = 'https://pypi.python.org/pypi/{}'.format(PROJECT_PACKAGE_NAME)

CACHE_PATH = './abode.pickle'
COOKIES = "cookies"

ID = 'id'
PASSWORD = 'password'
UUID = 'uuid'
MFA_CODE = 'mfa_code'

# URLS
BASE_URL = 'https://my.goabode.com/'

LOGIN_URL = BASE_URL + 'api/auth2/login'
LOGOUT_URL = BASE_URL + 'api/v1/logout'

OAUTH_TOKEN_URL = BASE_URL + 'api/auth2/claims'

PARAMS_URL = BASE_URL + 'api/v1/devices_beta/'

PANEL_URL = BASE_URL + 'api/v1/panel'

INTEGRATIONS_URL = BASE_URL + 'integrations/v1/devices/'


def get_panel_mode_url(area, mode):
    """Create panel URL."""
    return BASE_URL + 'api/v1/panel/mode/' + area + '/' + mode


DEVICES_URL = BASE_URL + 'api/v1/devices'
DEVICE_URL = BASE_URL + 'api/v1/devices/$DEVID$'

AREAS_URL = BASE_URL + 'api/v1/areas'

SETTINGS_URL = BASE_URL + 'api/v1/panel/setting'
SOUNDS_URL = BASE_URL + 'api/v1/sounds'
SIREN_URL = BASE_URL + 'api/v1/siren'

AUTOMATION_URL = BASE_URL + 'integrations/v1/automations/'
AUTOMATION_ID_URL = AUTOMATION_URL + '$AUTOMATIONID$/'
AUTOMATION_APPLY_URL = AUTOMATION_ID_URL + 'apply'

TIMELINE_IMAGES_ID_URL = BASE_URL + \
    'api/v1/timeline?device_id=$DEVID$&dir=next' + \
    '&event_label=Image+Capture&size=1'

# NOTIFICATION CONSTANTS
SOCKETIO_URL = 'wss://my.goabode.com/socket.io/'

SOCKETIO_HEADERS = {
    'Origin': 'https://my.goabode.com/',
}

DEVICE_UPDATE_EVENT = 'com.goabode.device.update'
GATEWAY_MODE_EVENT = 'com.goabode.gateway.mode'
TIMELINE_EVENT = 'com.goabode.gateway.timeline'
AUTOMATION_EVENT = 'com.goabode.automation'

# DICTIONARIES
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

COLOR_MODE_ON = 0
COLOR_MODE_OFF = 2

# GENERIC ABODE DEVICE TYPES
TYPE_ALARM = "alarm"
TYPE_CAMERA = "camera"
TYPE_CONNECTIVITY = "connectivity"
TYPE_COVER = "cover"
TYPE_LIGHT = "light"
TYPE_LOCK = "lock"
TYPE_MOISTURE = "moisture"
TYPE_MOTION = "motion"
TYPE_OCCUPANCY = "occupancy"
TYPE_OPENING = "door"
TYPE_SENSOR = "sensor"
TYPE_SWITCH = "switch"
TYPE_VALVE = "valve"

TYPE_UNKNOWN_SENSOR = "unknown_sensor"

BINARY_SENSOR_TYPES = [TYPE_CONNECTIVITY, TYPE_MOISTURE, TYPE_MOTION,
                       TYPE_OCCUPANCY, TYPE_OPENING]

# DEVICE TYPE_TAGS
# Alarm
DEVICE_ALARM = 'device_type.alarm'

# Binary Sensors - Connectivity
DEVICE_GLASS_BREAK = 'device_type.glass'
DEVICE_KEYPAD = 'device_type.keypad'
DEVICE_REMOTE_CONTROLLER = 'device_type.remote_controller'
DEVICE_SIREN = 'device_type.siren'
DEVICE_STATUS_DISPLAY = 'device_type.bx'

# Binary Sensors - Opening
DEVICE_DOOR_CONTACT = 'device_type.door_contact'

# Cameras
DEVICE_MOTION_CAMERA = 'device_type.ir_camera'
DEVICE_MOTION_VIDEO_CAMERA = 'device_type.ir_camcoder'
DEVICE_IP_CAM = 'device_type.ipcam'
DEVICE_OUTDOOR_MOTION_CAMERA = 'device_type.out_view'

# Covers
DEVICE_SECURE_BARRIER = 'device_type.secure_barrier'

# Dimmers
DEVICE_DIMMER = 'device_type.dimmer'
DEVICE_DIMMER_METER = 'device_type.dimmer_meter'
DEVICE_HUE = 'device_type.hue'

# Locks
DEVICE_DOOR_LOCK = 'device_type.door_lock'

# Moisture
DEVICE_WATER_SENSOR = 'device_type.water_sensor'

# Switches
DEVICE_SWITCH = 'device_type.switch'
DEVICE_NIGHT_SWITCH = 'device_type.night_switch'
DEVICE_POWER_SWITCH_SENSOR = 'device_type.power_switch_sensor'
DEVICE_POWER_SWITCH_METER = 'device_type.power_switch_meter'

# Water Valve
DEVICE_VALVE = 'device_type.valve'

# Unknown Sensor
# These device types are all considered 'occupancy' but could apparently
# also be multi-sensors based on their json.
DEVICE_ROOM_SENSOR = 'device_type.room_sensor'
DEVICE_TEMPERATURE_SENSOR = 'device_type.temperature_sensor'
DEVICE_MULTI_SENSOR = 'device_type.lm'  # LM = LIGHT MOTION?
DEVICE_PIR = 'device_type.pir'  # Passive Infrared Occupancy?
DEVICE_POVS = 'device_type.povs'

STATUSES_KEY = 'statuses'
TEMP_STATUS_KEY = 'temperature'
LUX_STATUS_KEY = 'lux'
HUMI_STATUS_KEY = 'humidity'
SENSOR_KEYS = [TEMP_STATUS_KEY, LUX_STATUS_KEY, HUMI_STATUS_KEY]

UNIT_CELSIUS = '°C'
UNIT_FAHRENHEIT = '°F'
UNIT_PERCENT = '%'
UNIT_LUX = 'lx'
LUX = 'lux'

BRIGHTNESS_KEY = 'statusEx'


def get_generic_type(type_tag):
    """Map type tag to generic type."""
    return {
        # Alarm
        DEVICE_ALARM: TYPE_ALARM,

        # Binary Sensors - Connectivity
        DEVICE_GLASS_BREAK: TYPE_CONNECTIVITY,
        DEVICE_KEYPAD: TYPE_CONNECTIVITY,
        DEVICE_REMOTE_CONTROLLER: TYPE_CONNECTIVITY,
        DEVICE_SIREN: TYPE_CONNECTIVITY,
        DEVICE_STATUS_DISPLAY: TYPE_CONNECTIVITY,

        # Binary Sensors - Opening
        DEVICE_DOOR_CONTACT: TYPE_OPENING,

        # Cameras
        DEVICE_MOTION_CAMERA: TYPE_CAMERA,
        DEVICE_MOTION_VIDEO_CAMERA: TYPE_CAMERA,
        DEVICE_IP_CAM: TYPE_CAMERA,
        DEVICE_OUTDOOR_MOTION_CAMERA: TYPE_CAMERA,

        # Covers
        DEVICE_SECURE_BARRIER: TYPE_COVER,

        # Lights (Dimmers)
        DEVICE_DIMMER: TYPE_LIGHT,
        DEVICE_DIMMER_METER: TYPE_LIGHT,
        DEVICE_HUE: TYPE_LIGHT,

        # Locks
        DEVICE_DOOR_LOCK: TYPE_LOCK,

        # Moisture
        DEVICE_WATER_SENSOR: TYPE_CONNECTIVITY,

        # Switches
        DEVICE_SWITCH: TYPE_SWITCH,
        DEVICE_NIGHT_SWITCH: TYPE_SWITCH,
        DEVICE_POWER_SWITCH_SENSOR: TYPE_SWITCH,
        DEVICE_POWER_SWITCH_METER: TYPE_SWITCH,

        # Water Valve
        DEVICE_VALVE: TYPE_VALVE,

        # Unknown Sensors
        # More data needed to determine type
        DEVICE_ROOM_SENSOR: TYPE_UNKNOWN_SENSOR,
        DEVICE_TEMPERATURE_SENSOR: TYPE_UNKNOWN_SENSOR,
        DEVICE_MULTI_SENSOR: TYPE_UNKNOWN_SENSOR,
        DEVICE_PIR: TYPE_UNKNOWN_SENSOR,
        DEVICE_POVS: TYPE_UNKNOWN_SENSOR,
    }.get(type_tag.lower(), None)


# Constants to be used to fill our imaginary alarm device
ALARM_NAME = "Abode Alarm"
ALARM_DEVICE_ID = "area_"
ALARM_TYPE = "Alarm"

# SETTINGS
SETTING_CAMERA_RESOLUTION = 'ircamera_resolution_t'
SETTING_CAMERA_GRAYSCALE = 'ircamera_gray_t'
SETTING_SILENCE_SOUNDS = 'beeper_mute'

PANEL_SETTINGS = [SETTING_CAMERA_RESOLUTION, SETTING_CAMERA_GRAYSCALE,
                  SETTING_SILENCE_SOUNDS]

SETTING_ENTRY_DELAY_AWAY = 'away_entry_delay'
SETTING_EXIT_DELAY_AWAY = 'away_exit_delay'
SETTING_ENTRY_DELAY_HOME = 'home_entry_delay'
SETTING_EXIT_DELAY_HOME = 'home_exit_delay'

AREA_SETTINGS = [SETTING_ENTRY_DELAY_AWAY, SETTING_EXIT_DELAY_AWAY,
                 SETTING_ENTRY_DELAY_HOME, SETTING_EXIT_DELAY_HOME]

SETTING_DOOR_CHIME = 'door_chime'
SETTING_WARNING_BEEP = 'warning_beep'
SETTING_ENTRY_BEEP_AWAY = 'entry_beep_away'
SETTING_EXIT_BEEP_AWAY = 'exit_beep_away'
SETTING_ENTRY_BEEP_HOME = 'entry_beep_home'
SETTING_EXIT_BEEP_HOME = 'exit_beep_home'
SETTING_CONFIRM_SOUND = 'confirm_snd'
SETTING_ALARM_LENGTH = 'alarm_len'
SETTING_FINAL_BEEPS = 'final_beep'

SOUND_SETTINGS = [SETTING_DOOR_CHIME, SETTING_WARNING_BEEP,
                  SETTING_ENTRY_BEEP_AWAY, SETTING_EXIT_BEEP_AWAY,
                  SETTING_ENTRY_BEEP_HOME, SETTING_EXIT_BEEP_HOME,
                  SETTING_CONFIRM_SOUND, SETTING_ALARM_LENGTH,
                  SETTING_FINAL_BEEPS]

SETTING_SIREN_ENTRY_EXIT_SOUNDS = "entry"
SETTING_SIREN_TAMPER_SOUNDS = "tamper"
SETTING_SIREN_CONFIRM_SOUNDS = "confirm"

SIREN_SETTINGS = [SETTING_SIREN_ENTRY_EXIT_SOUNDS, SETTING_SIREN_TAMPER_SOUNDS,
                  SETTING_SIREN_CONFIRM_SOUNDS]

ALL_SETTINGS = PANEL_SETTINGS + AREA_SETTINGS + SOUND_SETTINGS + SIREN_SETTINGS


# SETTING VALUES
SETTING_CAMERA_RES_320_240 = '0'
SETTING_CAMERA_RES_640_480 = '2'

SETTING_ALL_CAMERA_RES = [SETTING_CAMERA_RES_320_240,
                          SETTING_CAMERA_RES_640_480]

SETTING_DISABLE = '0'
SETTING_ENABLE = '1'

SETTING_DISABLE_ENABLE = [SETTING_DISABLE, SETTING_ENABLE]

SETTING_ENTRY_EXIT_DELAY_DISABLE = '0'
SETTING_ENTRY_EXIT_DELAY_10SEC = '10'
SETTING_ENTRY_EXIT_DELAY_20SEC = '20'
SETTING_ENTRY_EXIT_DELAY_30SEC = '30'
SETTING_ENTRY_EXIT_DELAY_1MIN = '60'
SETTING_ENTRY_EXIT_DELAY_2MIN = '120'
SETTING_ENTRY_EXIT_DELAY_3MIN = '180'
SETTING_ENTRY_EXIT_DELAY_4MIN = '240'

ALL_SETTING_ENTRY_EXIT_DELAY = [SETTING_ENTRY_EXIT_DELAY_DISABLE,
                                SETTING_ENTRY_EXIT_DELAY_10SEC,
                                SETTING_ENTRY_EXIT_DELAY_20SEC,
                                SETTING_ENTRY_EXIT_DELAY_30SEC,
                                SETTING_ENTRY_EXIT_DELAY_1MIN,
                                SETTING_ENTRY_EXIT_DELAY_2MIN,
                                SETTING_ENTRY_EXIT_DELAY_3MIN,
                                SETTING_ENTRY_EXIT_DELAY_4MIN]

VALID_SETTING_EXIT_AWAY = [SETTING_ENTRY_EXIT_DELAY_30SEC,
                           SETTING_ENTRY_EXIT_DELAY_1MIN,
                           SETTING_ENTRY_EXIT_DELAY_2MIN,
                           SETTING_ENTRY_EXIT_DELAY_3MIN,
                           SETTING_ENTRY_EXIT_DELAY_4MIN]

SETTING_SOUND_OFF = 'none'
SETTING_SOUND_LOW = 'normal'
SETTING_SOUND_HIGH = 'loud'

ALL_SETTING_SOUND = [SETTING_SOUND_OFF, SETTING_SOUND_LOW, SETTING_SOUND_HIGH]

VALID_SOUND_SETTINGS = [SETTING_DOOR_CHIME, SETTING_WARNING_BEEP,
                        SETTING_ENTRY_BEEP_AWAY, SETTING_EXIT_BEEP_AWAY,
                        SETTING_ENTRY_BEEP_HOME, SETTING_EXIT_BEEP_HOME,
                        SETTING_CONFIRM_SOUND]

SETTING_ALARM_LENGTH_DISABLE = '0'
SETTING_ALARM_LENGTH_1MIN = '60'
SETTING_ALARM_LENGTH_2MIN = '120'
SETTING_ALARM_LENGTH_3MIN = '180'
SETTING_ALARM_LENGTH_4MIN = '240'
SETTING_ALARM_LENGTH_5MIN = '300'
SETTING_ALARM_LENGTH_6MIN = '360'
SETTING_ALARM_LENGTH_7MIN = '420'
SETTING_ALARM_LENGTH_8MIN = '480'
SETTING_ALARM_LENGTH_9MIN = '540'
SETTING_ALARM_LENGTH_10MIN = '600'
SETTING_ALARM_LENGTH_11MIN = '660'
SETTING_ALARM_LENGTH_12MIN = '720'
SETTING_ALARM_LENGTH_13MIN = '780'
SETTING_ALARM_LENGTH_14MIN = '840'
SETTING_ALARM_LENGTH_15MIN = '900'

ALL_SETTING_ALARM_LENGTH = [SETTING_ALARM_LENGTH_DISABLE,
                            SETTING_ALARM_LENGTH_1MIN,
                            SETTING_ALARM_LENGTH_2MIN,
                            SETTING_ALARM_LENGTH_3MIN,
                            SETTING_ALARM_LENGTH_4MIN,
                            SETTING_ALARM_LENGTH_5MIN,
                            SETTING_ALARM_LENGTH_6MIN,
                            SETTING_ALARM_LENGTH_7MIN,
                            SETTING_ALARM_LENGTH_8MIN,
                            SETTING_ALARM_LENGTH_9MIN,
                            SETTING_ALARM_LENGTH_10MIN,
                            SETTING_ALARM_LENGTH_11MIN,
                            SETTING_ALARM_LENGTH_12MIN,
                            SETTING_ALARM_LENGTH_13MIN,
                            SETTING_ALARM_LENGTH_14MIN,
                            SETTING_ALARM_LENGTH_15MIN]

SETTING_FINAL_BEEPS_DISABLE = '0'
SETTING_FINAL_BEEPS_3SEC = '3'
SETTING_FINAL_BEEPS_4SEC = '4'
SETTING_FINAL_BEEPS_5SEC = '5'
SETTING_FINAL_BEEPS_6SEC = '6'
SETTING_FINAL_BEEPS_7SEC = '7'
SETTING_FINAL_BEEPS_8SEC = '8'
SETTING_FINAL_BEEPS_9SEC = '9'
SETTING_FINAL_BEEPS_10SEC = '10'

ALL_SETTING_FINAL_BEEPS = [SETTING_FINAL_BEEPS_DISABLE,
                           SETTING_FINAL_BEEPS_3SEC, SETTING_FINAL_BEEPS_4SEC,
                           SETTING_FINAL_BEEPS_5SEC, SETTING_FINAL_BEEPS_6SEC,
                           SETTING_FINAL_BEEPS_7SEC, SETTING_FINAL_BEEPS_8SEC,
                           SETTING_FINAL_BEEPS_9SEC, SETTING_FINAL_BEEPS_10SEC]
