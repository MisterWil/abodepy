#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
abodepy by Wil Schrader - An Abode alarm Python library.

https://github.com/MisterWil/abodepy

Influenced by blinkpy, because I'm a python noob:
https://github.com/fronzbot/blinkpy/

Published under the MIT license - See LICENSE file for more details.
"Blink Wire-Free HS Home Monitoring & Alert Systems" is a trademark
owned by Immedia Inc., see www.blinkforhome.com for more information.
I am in no way affiliated with Blink, nor Immedia Inc.
"""

import collections
import json
import logging
import threading
import requests

from socketIO_client import SocketIO, LoggingNamespace

import helpers.constants as CONST
import helpers.errors as ERROR


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


# pylint: disable=super-init-not-called
class AbodeException(Exception):
    """Class to throw general abode exception."""

    def __init__(self, error):
        """Initialize AbodeException."""
        self.errcode = error[0]
        self.message = error[1]


class AbodeAuthenticationException(AbodeException):
    """Class to throw authentication exception."""

    pass


class Abode():
    """Main Abode class."""

    def __init__(self, username=None, password=None,
                 auto_login=False, get_devices=False,
                 debug=False):
        """Init Abode object."""
        self._username = username
        self._password = password
        self._session = None
        self._token = None
        self._panel = None
        self._user = None
        self._debug = debug

        self._default_alarm_mode = CONST.MODE_AWAY

        self._devices = []
        self._device_id_lookup = {}

        # Create a requests session to persist the cookies
        self._session = requests.session()

        # If debug was included, we'll print out diagnostics.
        if self._debug:
            LOG.setLevel(logging.DEBUG)

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

        LOG.debug("Login Response: %s", response.text)

        self._token = response_object['token']
        self._panel = response_object['panel']
        self._user = response_object['user']

        self.abode_events = AbodeEvents(self, self._debug)

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

            LOG.debug("Logout Response: %s", response.text)

            self._session = requests.session()
            self._token = None
            self._panel = None
            self._user = None

            self._devices = []
            self._device_id_lookup = {}

        return True

    def start(self):
        """Start the Abode event listener."""
        self.abode_events.start()

    def stop(self):
        """Stop the Abode Event listener."""
        self.abode_events.stop()

    def register(self, device, callback):
        """Register a device to the Event listener."""
        if not isinstance(device, AbodeDevice):
            dev_id = device
            device = self.get_device(dev_id)

        if not device:
            raise AbodeException(ERROR.INVALID_DEVICE_ID)

        return self.abode_events.register(device, callback)

    def send_request(self, method, url, headers=None,
                     data=None, is_retry=False):
        """Send requests to Abode."""
        if not self._token:
            self.login()

        if not headers:
            headers = {}

        headers['ABODE-API-KEY'] = self._token

        response = getattr(self._session, method)(
            url, headers=headers, data=data)

        if response and response.status_code == 200:
            return response
        if not is_retry:
            # Delete our current token and try again -- will force a login
            # attempt.
            self._token = None

            return self.send_request(method, url, headers, data, True)

        raise AbodeException((ERROR.REQUEST))

    def __new_device(self, device_json):
        """Create new device object based on device_type."""
        if device_json['type_tag'] is None:
            return None

        device_type = device_json['type_tag'].lower()

        return {
            'device_type.door_lock': AbodeLock(device_json, self),
            'device_type.door_contact': AbodeBinarySensor(device_json, self),
            'device_type.glass': AbodeBinarySensor(device_json, self),
            'device_type.power_switch_sensor': AbodeSwitch(device_json, self),
        }.get(device_type, AbodeDevice(device_json, self))

    def get_devices(self, category_filter=None):
        """Get all devices from Abode."""
        response = self.send_request("get", CONST.DEVICES_URL)
        response_object = json.loads(response.text)

        if response_object and not isinstance(response_object, (tuple, list)):
            response_object = [response_object]

        LOG.debug("Get Devices Response: %s", response.text)

        # Clear the device libraries
        self._devices = []
        self._device_id_lookup = {}

        # Create device objects for each device returned
        for device_json in response_object:
            device = self.__new_device(device_json)

            if device:
                self.__add_device(self.__new_device(device_json))

        # We will be treating the Abode panel itself as an armable device.
        panel_response = self.send_request("get", CONST.PANEL_URL)
        panel_json = json.loads(panel_response.text)

        self._panel.update(panel_json)

        LOG.debug("Get Mode Panel Response: %s", response.text)

        panel_json['id'] = '1'
        panel_json['type'] = 'Alarm'

        self.__add_device(AbodeAlarm(panel_json, self))

        if category_filter:
            devices = []
            for device in self._devices:
                if (device.type is not None and device.type != '' and
                        device.type in category_filter):
                    devices.append(device)
            return devices

        return self._devices

    def __add_device(self, device):
        """Add a device to the internal lookups."""
        self._devices.append(device)
        self._device_id_lookup[device.device_id] = device

    def get_device(self, device_id, refresh=False):
        """Get a single device."""
        if not self._devices:
            self.get_devices()
            refresh = False

        device = self._device_id_lookup.get(device_id)

        if device and refresh:
            device.refresh()

        return device

    def get_alarm(self, area='1', refresh=False):
        """Shortcut method to get the alarm device."""
        if not self._devices:
            self.get_devices()
            refresh = False

        return self.get_device(area, refresh)

    def set_default_mode(self, default_mode):
        """Set the default mode when alarms are turned 'on'."""
        if default_mode.lower() not in (CONST.MODE_AWAY, CONST.MODE_HOME):
            raise AbodeException(ERROR.INVALID_DEFAULT_ALARM_MODE)

        self._default_alarm_mode = default_mode.lower()

    @property
    def default_mode(self):
        """Get the default mode."""
        return self._default_alarm_mode


class AbodeDevice(object):
    """Class to represent each Abode device."""

    def __init__(self, json_obj, abode_controller):
        """Set up Abode device."""
        self._json_state = json_obj
        self._device_id = json_obj.get('id')
        self._name = json_obj.get('name')
        self._type = json_obj.get('type')
        self._abode_controller = abode_controller

        if not self._name:
            if self._type:
                self._name = self._type + ' ' + self._device_id
            else:
                self._name = 'Device ' + self._device_id

    def set_status(self, status):
        """Set device status."""
        if self._json_state['control_url']:
            url = CONST.BASE_URL + self._json_state['control_url']

            status_data = {
                'status': str(status)
            }

            response = self._abode_controller.send_request(
                method="put", url=url, data=status_data)
            response_object = json.loads(response.text)

            LOG.debug("Set Status Response: %s", response.text)

            if response_object['id'] != self.device_id:
                raise AbodeException((ERROR.SET_STATUS_DEV_ID))

            if response_object['status'] != str(status):
                raise AbodeException((ERROR.SET_STATUS_STATE))

            # Note: Status result is of int type, not of new status of device.
            # Seriously, why would you do that?
            # So, can't set status here must be done at device level.

            return True

        return False

    def set_level(self, level):
        """Set device level."""
        if self._json_state['control_url']:
            url = CONST.BASE_URL + self._json_state['control_url']

            level_data = {
                'level': str(level)
            }

            response = self._abode_controller.send_request(
                "put", url, data=level_data)
            response_object = json.loads(response.text)

            LOG.debug("Set Level Response: %s", response.text)

            if response_object['id'] != self.device_id:
                raise AbodeException((ERROR.SET_STATUS_DEV_ID))

            if response_object['level'] != str(level):
                raise AbodeException((ERROR.SET_STATUS_STATE))

            # TODO: Figure out where level is indicated in device json object

            return True

        return False

    def get_value(self, name):
        """Get a value from the json object.

        This is the common data and is the best place to get state
        from if it has the data you require.
        This data is updated by the subscription service.
        """
        return self._json_state.get(name.lower(), {})

    def refresh(self, url=CONST.DEVICE_URL):
        """Refresh the devices json object data.

        Only needed if you're not using the notification service.
        """
        url = url.replace('$DEVID$', self.device_id)

        response = self._abode_controller.send_request(method="get", url=url)
        response_object = json.loads(response.text)

        LOG.debug("Device Refresh Response: %s", response.text)

        if response_object and not isinstance(response_object, (tuple, list)):
            response_object = [response_object]

        if response_object:
            for device in response_object:
                self.update(device)
        else:
            raise AbodeException(ERROR.REFRESH)

        return response_object

    def update(self, json_state):
        """Update the json data from a dictionary.

        Only updates if it already exists in the device.
        """
        self._json_state.update(
            {k: json_state[k] for k in json_state if self._json_state.get(k)})

    @property
    def status(self):
        """Shortcut to get the generic status of a device."""
        return self.get_value('status')

    @property
    def battery_low(self):
        """Is battery level low."""
        return int(self.get_value('faults').get('low_battery', '0')) == 1

    @property
    def no_response(self):
        """Is the device responding."""
        return int(self.get_value('faults').get('no_response', '0')) == 1

    @property
    def out_of_order(self):
        """Is the device out of order."""
        return int(self.get_value('faults').get('out_of_order', '0')) == 1

    @property
    def tampered(self):
        """Has the device been tampered with."""
        return int(self.get_value('faults').get('tempered', '0')) == 1

    @property
    def name(self):
        """Get the name of this device."""
        return self._name

    @property
    def type(self):
        """Get the type of this device."""
        return self._type

    @property
    def device_id(self):
        """Get the device id."""
        return self._device_id


class AbodeSwitch(AbodeDevice):
    """Class to add switch functionality."""

    def switch_on(self):
        """Turn the switch on."""
        success = self.set_status('1')

        if success:
            self._json_state['status'] = CONST.STATUS_ON

        return success

    def switch_off(self):
        """Turn the switch off."""
        success = self.set_status('0')

        if success:
            self._json_state['status'] = CONST.STATUS_OFF

        return success

    @property
    def is_on(self):
        """Get switch state."""
        return self.status not in CONST.STATUS_OFF


class AbodeSensor(AbodeDevice):
    """Class to represent a supported sensor."""


class AbodeBinarySensor(AbodeDevice):
    """Class to represent an on / off, online/offline sensor."""

    @property
    def is_on(self):
        """Get sensor on off state."""
        return self.status in (CONST.STATUS_ONLINE, CONST.STATUS_CLOSED)


class AbodeLock(AbodeDevice):
    """Class to represent a door lock."""

    def lock(self):
        """Lock the device."""
        success = self.set_status('1')

        if success:
            self._json_state['status'] = CONST.STATUS_LOCKCLOSED

        return success

    def unlock(self):
        """Unlock the device."""
        success = self.set_status('0')

        if success:
            self._json_state['status'] = CONST.STATUS_LOCKOPEN

        return success

    @property
    def is_locked(self):
        """Get locked state."""
        # Err on side of caution; assume if lock isn't explicitly
        # 'LockClosed' then it's open
        return self.status in CONST.STATUS_LOCKCLOSED


class AbodeAlarm(AbodeSwitch):
    """Class to represent the Abode alarm as a device."""

    def set_mode(self, mode):
        """Set Abode alarm mode."""
        if not mode:
            raise AbodeException(ERROR.MISSING_ALARM_MODE)
        elif mode.lower() not in CONST.ALL_MODES:
            raise AbodeException(ERROR.INVALID_ALARM_MODE)

        mode = mode.lower()

        LOG.debug("Setting Abode Alarm Mode To: %s", mode)

        response = self._abode_controller.send_request(
            "put", CONST.PANEL_MODE_URL(self.device_id, mode))

        if not response or response.status_code != 200:
            raise AbodeException(ERROR.SET_MODE)

        LOG.debug("Set Alarm Home Response: %s", response.text)

        response_object = json.loads(response.text)

        if response_object['area'] != self.device_id:
            raise AbodeException(ERROR.SET_MODE_AREA)

        if response_object['mode'] != mode:
            raise AbodeException(ERROR.SET_MODE_MODE)

        LOG.debug("Abode Alarm Mode Set To: %s", response_object['mode'])

        self._json_state['mode'][('area_' +
                                  self.device_id)] = response_object['mode']

        return True

    def set_home(self):
        """Arm Abode to home mode."""
        return self.set_mode(CONST.MODE_HOME)

    def set_away(self):
        """Arm Abode to home mode."""
        return self.set_mode(CONST.MODE_AWAY)

    def set_standby(self):
        """Arm Abode to stay mode."""
        return self.set_mode(CONST.MODE_STANDBY)

    def switch_on(self):
        """Arm Abode to default mode."""
        return self.set_mode(self._abode_controller.default_mode)

    def switch_off(self):
        """Arm Abode to home mode."""
        return self.set_standby()

    def refresh(self, url=CONST.PANEL_URL):
        """Refresh the alarm device."""
        response_object = AbodeDevice.refresh(self, url)
        # pylint: disable=W0212
        self._abode_controller._panel.update(response_object[0])

        return response_object

    @property
    def is_on(self):
        """Is alarm armed."""
        return self.mode in (CONST.MODE_HOME, CONST.MODE_AWAY)

    @property
    def mode(self):
        """Get alarm mode."""
        mode = self.get_value('mode').get('area_' + self.device_id, None)

        if not mode:
            raise AbodeException(ERROR.MISSING_ALARM_MODE)
        elif mode.lower() not in CONST.ALL_MODES:
            raise AbodeException(ERROR.INVALID_ALARM_MODE)

        return mode.lower()

    @property
    def status(self):
        """To match existing property."""
        return self.mode

    @property
    def battery(self):
        """Return true if base station on battery backup."""
        return int(self._json_state.get('battery', '0')) == 1

    @property
    def is_cellular(self):
        """Return true if base station on cellular backup."""
        return int(self._json_state.get('is_cellular', '0')) == 1


class AbodeEvents(object):
    """Class for subscribing to abode events."""

    def __init__(self, abode, debug=False):
        """Init event subscription class."""
        self._abode = abode
        self._devices = collections.defaultdict(list)
        self._callbacks = collections.defaultdict(list)
        self._thread = None
        self._socketio = None

        if debug:
            LOG.setLevel(logging.DEBUG)

    def register(self, device, callback):
        """Register a callback.

        device: device to be updated by subscription
        callback: callback for notification of changes
        """
        if not device or not isinstance(device, AbodeDevice):
            raise AbodeException(ERROR.EVENT_DEVICE_INVALID)

        LOG.debug("Subscribing to events for device: %s (%s)",
                  device.name, device.device_id)

        self._devices[device.device_id].append(device)
        self._callbacks[device].append((callback))

        return True

    def _on_device_update(self, devid):
        if devid is None:
            return

        LOG.debug("Device Update Received: %s", devid)

        device = self._abode.get_device(devid, True)

        for callback in self._callbacks.get(device, ()):
            callback(device)

    def _on_mode_change(self, mode):
        if mode is None:
            return

        if not mode or mode.lower() not in CONST.ALL_MODES:
            raise AbodeException(ERROR.INVALID_ALARM_MODE)

        LOG.debug("Alarm Mode Change Received: %s", mode)

        alarm_device = self._abode.get_alarm(refresh=True)

        # At the time of development, refreshing after mode change notification
        # didn't seem to get the latest update immediately. As such, we will
        # force the mode status now to match the notification.
        # pylint: disable=W0212
        alarm_device._json_state['mode']['area_1'] = mode

        for callback in self._callbacks.get(alarm_device, ()):
            callback(alarm_device)

    def join(self):
        """Don't allow the main thread to terminate until we have."""
        self._thread.join()

    def start(self):
        """Start a thread to handle Abode blocked SocketIO notifications."""
        if not self._thread:
            self._thread = threading.Thread(target=self._run_socketio_thread,
                                            name='Abode SocketIO Thread')
            self._thread.deamon = True
            self._thread.start()
            LOG.debug("Terminated started")

    def stop(self):
        """Tell the subscription thread to terminate."""
        if self._thread:
            # pylint: disable=W0212
            self._socketio._close()
            self.join()
            self._thread = None
            self._socketio = None
            LOG.debug("Terminated thread")

    def _run_socketio_thread(self):
        # pylint: disable=W0212
        self._socketio = SocketIO(
            CONST.SOCKETIO_URL, 443, LoggingNamespace,
            headers=CONST.SOCKETIO_HEADERS,
            cookies=self._abode._session.cookies.get_dict())

        self._socketio.on(CONST.DEVICE_UPDATE_EVENT, self._on_device_update)
        self._socketio.on(CONST.GATEWAY_MODE_EVENT, self._on_mode_change)

        LOG.debug("Starting Abode SocketIO Notification Service")

        self._socketio.wait()

        LOG.debug("Shutdown Abode SocketIO Notification Service")
