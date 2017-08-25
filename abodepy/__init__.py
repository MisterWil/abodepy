#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
abodepy by Wil Schrader - An Abode alarm Python library.

https://github.com/MisterWil/abodepy

Influenced by blinkpy, because I'm a python noob:
https://github.com/fronzbot/blinkpy/

Published under the MIT license - See LICENSE file for more details.

"Abode" is a trademark owned by Abode Systems Inc., see www.goabode.com for
more information. I am in no way affiliated with Abode.

Thank you Abode for having a relatively simple API to reverse engineer.
Hopefully in the future you'll open it up for official use.

API calls faster than 60 seconds is not recommended as it can overwhelm
Abode's servers. Leverage the cloud push event notification functionality as
much as possible. Please use this module responsibly.
"""

import json
import logging
import requests
from requests.exceptions import RequestException

from abodepy.devices import AbodeDevice
from abodepy.events import AbodeEvents
from abodepy.exceptions import AbodeAuthenticationException, AbodeException
import abodepy.devices as DEVICE
import abodepy.devices.alarm as ALARM
import abodepy.helpers.constants as CONST
import abodepy.helpers.errors as ERROR

_LOGGER = logging.getLogger(__name__)


class Abode():
    """Main Abode class."""

    def __init__(self, username=None, password=None,
                 auto_login=False, get_devices=False):
        """Init Abode object."""
        self._username = username
        self._password = password
        self._session = None
        self._token = None
        self._panel = None
        self._user = None

        self._abode_events = AbodeEvents(self)

        self._default_alarm_mode = CONST.MODE_AWAY

        self._devices = None
        self._device_id_lookup = None

        # Create a requests session to persist the cookies
        self._session = requests.session()

        if (self._username is not None and
                self._password is not None and
                auto_login):
            self.login()

        if get_devices:
            self.get_devices()

    def login(self, username=None, password=None):
        """Explicit Abode login."""
        if username is not None:
            self._username = username
        if password is not None:
            self._password = password

        if self._username is None or not isinstance(self._username, str):
            raise AbodeAuthenticationException(ERROR.USERNAME)

        if self._password is None or not isinstance(self._password, str):
            raise AbodeAuthenticationException(ERROR.PASSWORD)

        self._token = None

        login_data = {
            'id': self._username,
            'password': self._password
        }

        response = self._session.post(CONST.LOGIN_URL, data=login_data)
        response_object = json.loads(response.text)

        if response.status_code != 200:
            raise AbodeAuthenticationException((response.status_code,
                                                response_object['message']))

        _LOGGER.debug("Login Response: %s", response.text)

        self._token = response_object['token']
        self._panel = response_object['panel']
        self._user = response_object['user']

        _LOGGER.info("Login successful")

        return True

    def logout(self):
        """Explicit Abode logout."""
        if self._token:
            header_data = {
                'ABODE-API-KEY': self._token
            }

            response = self._session.post(
                CONST.LOGOUT_URL, headers=header_data)
            response_object = json.loads(response.text)

            if response.status_code != 200:
                raise AbodeAuthenticationException(
                    (response.status_code, response_object['message']))

            _LOGGER.debug("Logout Response: %s", response.text)

            self._session = requests.session()
            self._token = None
            self._panel = None
            self._user = None

            self._devices = None
            self._device_id_lookup = None

            _LOGGER.info("Logout successful")

        return True

    def start_listener(self):
        """Start the Abode event listener."""
        self._abode_events.start()

    def stop_listener(self):
        """Stop the Abode Event listener."""
        self._abode_events.stop()

    def register(self, device, callback):
        """Register a device to the Event listener."""
        if not isinstance(device, AbodeDevice):
            dev_id = device
            device = self.get_device(dev_id)

        if not device:
            raise AbodeException(ERROR.INVALID_DEVICE_ID)

        return self._abode_events.register(device, callback)

    def get_devices(self, refresh=False, type_filter=None):
        """Get all devices from Abode."""
        if refresh or self._devices is None:
            if self._devices is None:
                # Set up the device libraries
                self._devices = []
                self._device_id_lookup = {}

            _LOGGER.info("Updating all devices...")
            response = self.send_request("get", CONST.DEVICES_URL)
            response_object = json.loads(response.text)

            if (response_object and
                    not isinstance(response_object, (tuple, list))):
                response_object = [response_object]

            _LOGGER.debug("Get Devices Response: %s", response.text)

            for device_json in response_object:
                # Attempt to reuse an existing device
                device = self._device_id_lookup.get(device_json['id'])

                # No existing device, create a new one
                if device:
                    device.update(device_json)
                else:
                    self.__add_device(DEVICE.new_device(device_json, self))

            # We will be treating the Abode panel itself as an armable device.
            panel_response = self.send_request("get", CONST.PANEL_URL)
            panel_json = json.loads(panel_response.text)

            self._panel.update(panel_json)

            _LOGGER.debug("Get Mode Panel Response: %s", response.text)

            alarm_device = self._device_id_lookup.get(
                CONST.ALARM_DEVICE_ID + '1')

            if alarm_device:
                alarm_device.update(panel_json)
            else:
                self.__add_device(ALARM.create_alarm(panel_json, self))

        if type_filter:
            devices = []
            for device in self._devices:
                if (device.type is not None and
                        device.type in type_filter):
                    devices.append(device)
            return devices

        return self._devices

    def __add_device(self, device):
        """Add a device to the internal lookups."""
        self._devices.append(device)
        self._device_id_lookup[device.device_id] = device

    def get_device(self, device_id, refresh=False):
        """Get a single device."""
        if self._devices is None:
            self.get_devices()
            refresh = False

        device = self._device_id_lookup.get(device_id)

        if device and refresh:
            device.refresh()

        return device

    def get_alarm(self, area='1', refresh=False):
        """Shortcut method to get the alarm device."""
        if self._devices is None:
            self.get_devices()
            refresh = False

        return self.get_device(CONST.ALARM_DEVICE_ID + area, refresh)

    def set_default_mode(self, default_mode):
        """Set the default mode when alarms are turned 'on'."""
        if default_mode.lower() not in (CONST.MODE_AWAY, CONST.MODE_HOME):
            raise AbodeException(ERROR.INVALID_DEFAULT_ALARM_MODE)

        self._default_alarm_mode = default_mode.lower()

    def set_setting(self, setting, value, area='1', validate_value=True):
        """Set an abode system setting to a given value."""
        setting = setting.lower()

        if setting not in CONST.ALL_SETTINGS:
            raise AbodeException(ERROR.INVALID_SETTING, CONST.ALL_SETTINGS)

        if setting in CONST.PANEL_SETTINGS:
            url = CONST.SETTINGS_URL
            data = self._panel_settings(setting, value, validate_value)
        elif setting in CONST.AREA_SETTINGS:
            url = CONST.AREAS_URL
            data = self._area_settings(area, setting, value, validate_value)
        elif setting in CONST.SOUND_SETTINGS:
            url = CONST.SOUNDS_URL
            data = self._sound_settings(area, setting, value, validate_value)
        elif setting in CONST.SIREN_SETTINGS:
            url = CONST.SIREN_URL
            data = self._siren_settings(setting, value, validate_value)

        return self.send_request(method="put", url=url, data=data)

    @staticmethod
    def _panel_settings(setting, value, validate_value):
        """Will validate panel settings and values, returns data packet."""
        if validate_value:
            if (setting == CONST.SETTING_CAMERA_RESOLUTION
                    and value not in CONST.SETTING_ALL_CAMERA_RES):
                raise AbodeException(ERROR.INVALID_SETTING_VALUE,
                                     CONST.SETTING_ALL_CAMERA_RES)
            elif (setting in
                  [CONST.SETTING_CAMERA_GRAYSCALE,
                   CONST.SETTING_SILENCE_SOUNDS]
                  and value not in
                  CONST.SETTING_DISABLE_ENABLE):
                raise AbodeException(ERROR.INVALID_SETTING_VALUE,
                                     CONST.SETTING_DISABLE_ENABLE)

        return {setting: value}

    @staticmethod
    def _area_settings(area, setting, value, validate_value):
        """Will validate area settings and values, returns data packet."""
        if validate_value:
            # Exit delay has some specific limitations apparently
            if (setting == CONST.SETTING_EXIT_DELAY_AWAY
                    and value not in CONST.VALID_SETTING_EXIT_AWAY):
                raise AbodeException(ERROR.INVALID_SETTING_VALUE,
                                     CONST.VALID_SETTING_EXIT_AWAY)
            elif value not in CONST.ALL_SETTING_ENTRY_EXIT_DELAY:
                raise AbodeException(ERROR.INVALID_SETTING_VALUE,
                                     CONST.ALL_SETTING_ENTRY_EXIT_DELAY)

        return {'area': area, setting: value}

    @staticmethod
    def _sound_settings(area, setting, value, validate_value):
        """Will validate sound settings and values, returns data packet."""
        if validate_value:
            if (setting in CONST.VALID_SOUND_SETTINGS
                    and value not in CONST.ALL_SETTING_SOUND):
                raise AbodeException(ERROR.INVALID_SETTING_VALUE,
                                     CONST.ALL_SETTING_SOUND)
            elif (setting == CONST.SETTING_ALARM_LENGTH
                  and value not in CONST.ALL_SETTING_ALARM_LENGTH):
                raise AbodeException(ERROR.INVALID_SETTING_VALUE,
                                     CONST.ALL_SETTING_ALARM_LENGTH)
            elif (setting == CONST.SETTING_FINAL_BEEPS
                  and value not in CONST.ALL_SETTING_FINAL_BEEPS):
                raise AbodeException(ERROR.INVALID_SETTING_VALUE,
                                     CONST.ALL_SETTING_FINAL_BEEPS)

        return {'area': area, setting: value}

    @staticmethod
    def _siren_settings(setting, value, validate_value):
        """Will validate siren settings and values, returns data packet."""
        if validate_value:
            if value not in CONST.SETTING_DISABLE_ENABLE:
                raise AbodeException(ERROR.INVALID_SETTING_VALUE,
                                     CONST.SETTING_DISABLE_ENABLE)

        return {'action': setting, 'option': value}

    def send_request(self, method, url, headers=None,
                     data=None, is_retry=False):
        """Send requests to Abode."""
        if not self._token:
            self.login()

        if not headers:
            headers = {}

        headers['ABODE-API-KEY'] = self._token

        try:
            response = getattr(self._session, method)(
                url, headers=headers, data=data)

            if response and response.status_code == 200:
                return response
        except RequestException:
            _LOGGER.info("Abode connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login
            # attempt.
            self._token = None

            return self.send_request(method, url, headers, data, True)

        raise AbodeException((ERROR.REQUEST))

    @property
    def default_mode(self):
        """Get the default mode."""
        return self._default_alarm_mode

    def _get_session(self):
        # Perform a generic update so we know we're logged in
        self.send_request("get", CONST.PANEL_URL)

        return self._session
