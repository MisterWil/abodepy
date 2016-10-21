import requests
import json
import sys
import uuid
import logging

from .notification import NotificationRegistry

BASE_URL = 'https://my.goabode.com/'

LOGIN_URL = BASE_URL + 'api/auth2/login'
LOGOUT_URL = BASE_URL + 'api/v1/logout'

PANEL_URL = BASE_URL + 'api/v1/panel'
PANEL_MODE_URL = BASE_URL + 'api/v1/panel/mode/$AREA$/$MODE$'

DEVICES_URL = BASE_URL + 'api/v1/devices'
DEVICE_URL = BASE_URL + 'api/v1/devices/$DEVID$'

AREAS_URL = BASE_URL + 'api/v1/areas'

_ABODE_CONTROLLER = None

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

def init_controller(username, password):
    """Initialize a controller.
    Provides a single global controller for applications that can't do this
    themselves
    """
    # pylint: disable=global-statement
    global _ABODE_CONTROLLER
    created = False
    if _ABODE_CONTROLLER is None:
        _ABODE_CONTROLLER = AbodeController(username, password)
        created = True
    return [_ABODE_CONTROLLER, created]


def get_controller():
    """Return the global controller from init_controller."""
    return _ABODE_CONTROLLER

class AbodeController():

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

        # If we got debug passed, we'll print out diagnostics.
        if self.debug:
            LOG.setLevel(logging.DEBUG)

        if get_devices:
            self.get_devices()

    def login(self):
        if not self.username or not self.password:
            self.abort("You must provide a username and password.")

        self.token = None

        login_data = {
            'id': self.username,
            'password': self.password
        }

        response = self.session.post(LOGIN_URL, data=login_data)
        response_object = json.loads(response.text)

        if response.status_code != 200:
            self.abort(response_object['message']);

        LOG.debug("Login Response: %s" % response.text)

        self.token = response_object['token']
        self.panel = response_object['panel']
        self.user = response_object['user']

        self.notification_registery = NotificationRegistry(self, self.debug)

        return True

    def logout(self):
        if self.token:
            header_data = {
                'ABODE-API-KEY': self.token
            }

            response = self.session.post(LOGOUT_URL, headers=header_data)

            LOG.debug("Logout Response: %s" % response.text)

            self.token = None
            self.panel = None
            self.user = None

        return True

    def start(self):
        self.notification_registery.start()

    def stop(self):
        self.notification_registery.stop()

    def register(self, device, callback):
        if not isinstance(device, AbodeDevice):
            dev_id = device
            device = self.get_device(device)

        if not device:
            LOG.warn("Failed to register callback. Value '%s' is not a device or device id." % dev_id)
            return

        self.notification_registery.register(device, callback)

    def send_request(self, method, url, headers = {}, data = {}, retry=False):
        if not self.token:
            self.login()

        headers['ABODE-API-KEY'] = self.token

        response = getattr(self.session, method)(url, headers=headers, data=data)

        if response and response.status_code == 200:
            return response
        elif retry == False:
            self.token = None
            return self.send_request(method, url, headers, data, True)

        self.abort("Repeated %s request failed for url: %s" % (method, url))

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
                self.name = 'Abode ' + self.type + ' ' + self.device_id
            else:
                self.name = 'Abode Device ' + self.device_id

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

        Only updates if it already exists in the device.
        """

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
            self.abode_controller.abort("Unable to get abode switch status for device %s." % self.device_id)

        val = val.lower()

        return val not in ('off')

class AbodeAlarm(AbodeSwitch):
    """Class to represent the Abode alarm as a device that can be switched on and off."""

    def set_mode(self, mode, area='1'):
        """Set Abode alarm mode."""
        if not mode or mode.lower() not in ('home', 'away', 'standby'):
            self.abode_controller.abort("Mode must be one of 'home', 'away', or 'standby'.")

        mode = mode.lower()

        LOG.debug("Setting Abode Alarm Mode To: %s" % mode)

        url = PANEL_MODE_URL.replace('$AREA$', area)
        url = url.replace('$MODE$', mode)

        response = self.send_request("put", url)
        response_object = json.loads(response.text)

        LOG.debug("Set Alarm Home Response: %s" % response.text)

        LOG.info("Abode Alarm Mode Set To: %s" % response_object['mode'])

        return response_object['mode']

    def set_home(self, area='1'):
        """Arm Abode to home mode."""
        return self.set_mode('home', area)

    def set_away(self, area='1'):
        """Arm Abode to home mode."""
        return self.set_mode('away', area)

    def set_standby(self, area='1'):
        """Arm Abode to stay mode."""
        return self.set_mode('standby', area)

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
            self.abode_controller.abort("Unable to get abode alarm mode for area %s." % area)

        val = val.lower()

        return val != 'standby'

    def refresh(self):
        response_object = AbodeDevice.refresh(self, PANEL_URL)

        self.abode_controller.panel.update(response_object)

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

        val = self.get_value('mode').get('area_'+area, None)

        if not val:
            self.abode_controller.abort("Unable to get abode alarm mode for area %s." % area)

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
            self.abode_controller.abort("Unable to get Abode lock status for device %s." % self.device_id)

        val = val.lower()

        return val not in ('lockclosed')
