#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
abodeby by Wil Schrader - An Abode alarm Python library.
https://github.com/MisterWil/abodepy
Influenced by blinkpy, because I'm a python noob:
https://github.com/fronzbot/blinkpy/
Published under the MIT license - See LICENSE file for more details.
"Blink Wire-Free HS Home Monitoring & Alert Systems" is a trademark
owned by Immedia Inc., see www.blinkforhome.com for more information.
I am in no way affiliated with Blink, nor Immedia Inc.
"""

import requests
import json
import sys
import uuid
import logging
from events import AbodeEvents
import helpers.errors as ERROR
from helpers.constants import (BASE_URL, LOGIN_URL,
                               LOGOUT_URL,
                               PANEL_URL, PANEL_MODE_URL,
                               DEVICES_URL, DEVICE_URL,
                               AREAS_URL, MODE_STANDBY,
                               MODE_HOME, MODE_AWAY, ALL_MODES,
                               ALL_MODES_STR, ARMED)

_ABODE_INSTANCE = None

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

def init(username, password):
    """Initialize an instance of Abode.
    Provides a single global Abode instance for applications that can't do this
    themselves
    """
    # pylint: disable=global-statement
    global _ABODE_INSTANCE
    created = False
    if _ABODE_INSTANCE is None:
        _ABODE_INSTANCE = Abode(username, password)
        created = True
    return [_ABODE_INSTANCE, created]

def get_abode():
    """Return the global abode instance from init."""
    return _ABODE_INSTANCE
    
# pylint: disable=super-init-not-called
class AbodeException(Exception):
    """Class to throw general abode exception."""

    def __init__(self, errcode):
        """Initialize AbodeException."""
        self.errid = errcode[0]
        self.message = errcode[1]


class AbodeAuthenticationException(AbodeException):
    """Class to throw authentication exception."""

    pass


class Abode():

    def __init__(self, username, password, get_devices=True, debug=False):

        # Initialize variables
        self.username = username
        self.password = password
        self.session = None
        self.token = None
        self.panel = None
        self.user = None
        self.debug = debug

        self.devices = []
        self.device_map = {}

        # Create a requests session to persist the cookies
        self.session = requests.session()

        # If debug was included, we'll print out diagnostics.
        if self.debug:
            LOG.setLevel(logging.DEBUG)

        if get_devices:
            self.get_devices()

    def login(self):
        if self.username is None or self.password is None:
            raise AbodeAuthenticationException(ERROR.AUTHENTICATE)
        if not isinstance(self.username, str):
            raise BlinkAuthenticationException(ERROR.USERNAME)
        if not isinstance(self.password, str):
            raise BlinkAuthenticationException(ERROR.PASSWORD)
        
        self.token = None

        login_data = {
            'id': self.username,
            'password': self.password
        }

        response = self.session.post(LOGIN_URL, data=login_data)
        response_object = json.loads(response.text)

        if response.status_code != 200:
            raise AbodeException((response.status_code, response_object['message']))

        LOG.debug("Login Response: %s" % response.text)

        self.token = response_object['token']
        self.panel = response_object['panel']
        self.user = response_object['user']

        self.abode_events = AbodeEvents(self, self.debug)

        return True

    def logout(self):
        if self.token:
            header_data = {
                'ABODE-API-KEY': self.token
            }

            response = self.session.post(LOGOUT_URL, headers=header_data)
            
            if response.status_code != 200:
                raise AbodeException((response.status_code, response_object['message']))

            LOG.debug("Logout Response: %s" % response.text)

            self.token = None
            self.panel = None
            self.user = None

        return True

    def start(self):
        self.abode_events.start()

    def stop(self):
        self.abode_events.stop()

    def register(self, device, callback):
        if not isinstance(device, AbodeDevice):
            dev_id = device
            device = self.get_device(dev_id)

        if not device:
            LOG.warn("Failed to register callback. Value '%s' is not a device or device id." % dev_id)
            return

        self.abode_events.register(device, callback)

    def send_request(self, method, url, headers = {}, data = {}, is_retry=False):
        if not self.token:
            self.login()

        headers['ABODE-API-KEY'] = self.token

        response = getattr(self.session, method)(url, headers=headers, data=data)

        if response and response.status_code == 200:
            return response
        elif is_retry == False:
            '''Delete our current token and try again -- will force a login attempt.'''
            self.token = None
            
            return self.send_request(method, url, headers, data, True)

        raise AbodeException((response.code, "Repeated %s request failed for url: %s" % (method, url)))

    def abort(self, msg):
        LOG.error("Aborting and Logging Out.")
        self.logout()
        raise Exception("Error: %s" % msg)

    def get_devices(self, category_filter=''):
        response = self.send_request("get", DEVICES_URL)
        response_object = json.loads(response.text)

        LOG.debug("Get Devices Response: %s" % response.text)

        self.devices = []
        self.device_map = {}

        for device_json in response_object:
            if device_json['type_tag']:
                if device_json['type_tag'].lower() == 'device_type.door_lock':
                    self.add_device(AbodeLock(device_json, self))
                elif device_json['type_tag'].lower() == 'device_type.door_contact':
                    self.add_device(AbodeBinarySensor(device_json, self))
                elif device_json['type_tag'].lower() == 'device_type.ir_camera':
                    self.add_device(AbodeDevice(device_json, self))
                elif device_json['type_tag'].lower() == 'device_type.remote_controller':
                    self.add_device(AbodeDevice(device_json, self))
                elif device_json['type_tag'].lower() == 'device_type.glass':
                    self.add_device(AbodeBinarySensor(device_json, self))
                else:
                    self.add_device(AbodeDevice(device_json, self))

        '''We will be treating the Abode panel itself as an armable device.'''
        panel_response = self.send_request("get", PANEL_URL)
        panel_json = json.loads(panel_response.text)

        self.panel.update(panel_json)

        LOG.debug("Get Mode Panel Response: %s" % response.text)

        panel_json['id'] = 'area_1'
        panel_json['type'] = 'Alarm'

        self.add_device(AbodeAlarm(panel_json, self))

        if not category_filter:
            return self.devices
        else:
            devices = []
            for device in self.devices:
                if (device.type is not None and device.type != '' and
                        device.type in category_filter):
                    devices.append(device)
            return devices

    def add_device(self, device):
        self.devices.append(device);
        self.device_map[device.device_id] = device

    def get_device(self, device_id, refresh=False):
        device = self.device_map.get(device_id)

        if device and refresh:
            device.refresh()

        return device

    def get_alarm(self, area='1', refresh=False):
        return self.get_device('area_'+area, refresh)

class AbodeDevice(object):
    """Class to represent each Abode device."""

    def __init__(self, json_obj, abode_controller):
        """Set up Abode device."""

        self.json_state = json_obj
        self.device_id = self.json_state['id']
        self.abode_controller = abode_controller
        self.name = self.json_state.get('name')
        self.type = self.json_state.get('type')

        if not self.name:
            if self.type:
                self.name = self.type + ' ' + self.device_id
            else:
                self.name = 'Device ' + self.device_id

    def set_status(self, status):
        if self.json_state['control_url']:
            url = BASE_URL + self.json_state['control_url']

            status_data = {
                'status': str(status)
            }

            response = self.abode_controller.send_request("put", url, data = status_data)
            response_object = json.loads(response.text)

            LOG.debug("Set Status Reaponse: %s" % response.text)

            if response_object['id'] != self.id:
                LOG.warning("Device status change response device ID does not match. \
                    Request Device ID: %s, Response Device ID: %s" % (self.id, response_object['id']))

                return False

            if response_object['status'] != str(status):
                LOG.warning("Device control response status does not match request. \
                    Request Status: %s, Response Status: %s" % (str(status), response_object['status']))

                return False

            return True

    def set_level(self, level):
        if self.json_state['control_url']:
            url = BASE_URL + self.json_state['control_url']

            level_data = {
                'level': str(level)
            }

            response = self.abode_controller.send_request("put", url, data = level_data)
            response_object = json.loads(response.text)

            LOG.debug("Set Level Reaponse: %s" % response.text)

            if response_object['id'] != self.id:
                LOG.warning("Device level change response device ID does not match. \
                    Request Device ID: %s, Response Device ID: %s" % (self.id, response_object['id']))

                return False

            if response_object['level'] != str(level):
                LOG.warning("Device control response level does not match request. \
                    Request Level: %s, Response Level: %s" % (str(status), response_object['status']))

                return False

            return True

    def get_value(self, name):
        """Get a value from the json object.
        This is the common data and is the best place to get state
        from if it has the data you require.
        This data is updated by the subscription service.
        """
        return self.json_state.get(name.lower(), {})
    
    def get_name(self):
        return self.name
        
    def get_type(self):
        return self.type
        
    def get_device_id(self):
        return self.device_id
    
    def get_status(self):
        """Shortcut to get the generic status of a device.
        """
        return self.get_value('status')

    def refresh(self, url=DEVICE_URL):
        """Refresh the devices json object data.

        Only needed if you're not using the notification service."""
        url = url.replace('$DEVID$', self.device_id)

        response = self.abode_controller.send_request("get", url)
        response_object = json.loads(response.text)

        LOG.debug("Device Refresh Response: %s" % response.text)

        if response_object and not isinstance(response_object, (tuple, list)):
            response_object = [response_object]

        if response_object:
            for device in response_object:
                self.update(device)
        else:
            LOG.warn("Failed to refresh device %s" % self.device_id)

        return response_object

    def update(self, json_state):
        """Update the json data from a dictionary.

        Only updates if it already exists in the device."""

        self.json_state.update({k: json_state[k] for k in json_state if self.json_state.get(k)})

    @property
    def battery_low(self):
        """Is battery level low, True or False"""
        return self.get_value('faults').get('low_battery', '0') == '1'

    @property
    def is_responding(self):
        """Is the device responding, True or False"""
        return self.get_value('faults').get('no_response', '0') == '0'

    @property
    def out_of_order(self):
        """Is the device out of order, True or False"""
        return self.get_value('faults').get('out_of_order', '0') == '1'

    @property
    def tampered(self):
        """Has the device been tampered with, True or False"""
        return self.get_value('faults').get('tempered', '0') == '1'

    @property
    def abode_name(self):
        """The name of this device, either set by Abode or infered via type and id."""
        return self.name

    @property
    def abode_device_id(self):
        """The ID Abode uses to refer to the device."""
        return self.device_id

class AbodeSwitch(AbodeDevice):
    """Class to add switch functionality."""

    def switch_on(self):
        """Turn the switch on."""
        self.set_status('1')

    def switch_off(self):
        """Turn the switch off."""
        self.set_value('0')

    def is_switched_on(self, refresh=False):
        """Get switch state.
        Refresh data from Abode if refresh is True, otherwise use local cache.
        Refresh is only needed if you're not using notifications.
        """
        if refresh:
            self.refresh()

        val = self.get_value('status')

        if not val:
            raise AbodeException(ERROR.INVALID_SWITCH_VALUE)

        val = val.lower()

        return val not in ('off')

class AbodeAlarm(AbodeSwitch):
    """Class to represent the Abode alarm as a device that can be switched on and off."""

    def set_mode(self, mode, area='1'):
        """Set Abode alarm mode."""
        if not mode or mode.lower() not in ALL_MODES:
            self.abode_controller.abort("Mode must be one of %s." % ALL_MODES_STR)

        mode = mode.lower()

        LOG.debug("Setting Abode Alarm Mode To: %s" % mode)

        url = PANEL_MODE_URL.replace('$AREA$', area)
        url = url.replace('$MODE$', mode)

        response = self.abode_controller.send_request("put", url)
        response_object = json.loads(response.text)

        LOG.debug("Set Alarm Home Response: %s" % response.text)

        LOG.debug("Abode Alarm Mode Set To: %s" % response_object['mode'])

        return response_object['mode']

    def set_home(self, area='1'):
        """Arm Abode to home mode."""
        return self.set_mode(MODE_HOME, area)

    def set_away(self, area='1'):
        """Arm Abode to home mode."""
        return self.set_mode(MODE_AWAY, area)

    def set_standby(self, area='1'):
        """Arm Abode to stay mode."""
        return self.set_mode(MODE_STANDBY, area)

    def switch_on(self, area='1'):
        """Arm Abode to home mode."""
        return self.set_mode(self.abode_controller.get_default_alarm_state(), area)

    def switch_off(self, area='1'):
        """Arm Abode to home mode."""
        return self.set_standby(area)

    def is_switched_on(self, area='1', refresh=False):
        """Get armed state.

        Refresh data from Abode if refresh is True, otherwise use local cache.
        Refresh is only needed if you're not using notifications.
        """
        if refresh:
            self.refresh()

        val = self.get_value('mode').get('area_'+area, None)

        if not val:
            raise AbodeException(ERRORS.INVALID_ALARM_VALUE)
            
        if val not in ALL_MODES:
            raise AbodeException(ERROR.INVALID_ALARM_MODE)

        val = val.lower()

        return ARMED[val];
        
    def get_mode(self, area='1', refresh=False):
        """Get alarm mode.
        
        Refresh data from Abode if refresh is True, otherwise use local cache.
        Refresh is only needed if you're not using notifications.
        """
        if refresh:
            self.refresh()
            
        mode = self.get_value('mode').get('area_'+area, None)
        
        if not mode:
            raise AbodeException(ERROR.INVALID_ALARM_MODE)
            
        mode = mode.lower()
        
        return mode;
        
    def get_status(self):
        return self.get_mode()

    def refresh(self):
        response_object = AbodeDevice.refresh(self, PANEL_URL)
        self.abode_controller.panel.update(response_object[0])
        
        return response_object;

class AbodeSensor(AbodeDevice):
    """Class to represent a supported sensor."""

class AbodeBinarySensor(AbodeDevice):
    """Class to represent an on / off sensor."""

    def is_switched_on(self, refresh=False):
        """Get sensor on off state.

        Refresh data from Abode if refresh is True, otherwise use local cache.
        Refresh is only needed if you're not using notifications.
        """
        if refresh:
            self.refresh()

        val = self.get_value('status')

        if not val:
            raise AbodeException(ERROR.INVALID_SWITCH_VALUE)

        val = val.lower()

        return val in ('online', 'closed')

class AbodeLock(AbodeDevice):
    """Class to represent a door lock."""

    def lock(self):
        """Lock the device."""
        self.set_status('1')

    def unlock(self):
        """Unlock the device."""
        self.set_status('0')

    def is_locked(self, refresh=False):
        """Get locked state.

        Refresh data from Abode if refresh is True, otherwise use local cache.
        Refresh is only needed if you're not using notifications.
        """
        if refresh:
            self.refresh()

        val = self.get_value('status')

        if not val:
            raise AbodeException(ERROR.INVALID_LOCK_VALUE)

        val = val.lower()

        return val not in ('lockclosed')
