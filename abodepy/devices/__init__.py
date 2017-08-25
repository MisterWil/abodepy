"""Init file for devices directory."""
import json
import logging

from abodepy.exceptions import AbodeException

import abodepy.helpers.constants as CONST
import abodepy.helpers.errors as ERROR

_LOGGER = logging.getLogger(__name__)


def new_device(device_json, abode):
    """Create new device object for the given type."""
    from abodepy.devices.binary_sensor import AbodeBinarySensor
    from abodepy.devices.cover import AbodeCover
    from abodepy.devices.lock import AbodeLock
    from abodepy.devices.switch import AbodeSwitch

    if device_json['type_tag'] is None:
        return None

    device_type = device_json['type_tag'].lower()

    return {
        CONST.DEVICE_GLASS_BREAK: AbodeBinarySensor(device_json, abode),
        CONST.DEVICE_KEYPAD: AbodeBinarySensor(device_json, abode),
        CONST.DEVICE_DOOR_CONTACT: AbodeBinarySensor(device_json, abode),
        CONST.DEVICE_STATUS_DISPLAY: AbodeBinarySensor(device_json, abode),
        CONST.DEVICE_MOTION_CAMERA: AbodeBinarySensor(device_json, abode),
        CONST.DEVICE_DOOR_LOCK: AbodeLock(device_json, abode),
        CONST.DEVICE_POWER_SWITCH_SENSOR: AbodeSwitch(device_json, abode),
        CONST.DEVICE_POWER_SWITCH_METER: AbodeSwitch(device_json, abode),
        CONST.DEVICE_WATER_SENSOR: AbodeBinarySensor(device_json, abode),
        CONST.DEVICE_SECURE_BARRIER: AbodeCover(device_json, abode),
    }.get(device_type, AbodeDevice(device_json, abode))


class AbodeDevice(object):
    """Class to represent each Abode device."""

    def __init__(self, json_obj, abode):
        """Set up Abode device."""
        self._json_state = json_obj
        self._device_id = json_obj.get('id')
        self._name = json_obj.get('name')
        self._type = json_obj.get('type')
        self._type_tag = json_obj.get('type_tag')
        self._abode = abode

        if not self._name:
            self._name = self._type + ' ' + self._device_id

    def set_status(self, status):
        """Set device status."""
        if self._json_state['control_url']:
            url = CONST.BASE_URL + self._json_state['control_url']

            status_data = {
                'status': str(status)
            }

            response = self._abode.send_request(
                method="put", url=url, data=status_data)
            response_object = json.loads(response.text)

            _LOGGER.debug("Set Status Response: %s", response.text)

            if response_object['id'] != self.device_id:
                raise AbodeException((ERROR.SET_STATUS_DEV_ID))

            if response_object['status'] != str(status):
                raise AbodeException((ERROR.SET_STATUS_STATE))

            # Note: Status result is of int type, not of new status of device.
            # Seriously, why would you do that?
            # So, can't set status here must be done at device level.

            _LOGGER.info("Set device %s status to: %s", self.device_id, status)

            return True

        return False

    def set_level(self, level):
        """Set device level."""
        if self._json_state['control_url']:
            url = CONST.BASE_URL + self._json_state['control_url']

            level_data = {
                'level': str(level)
            }

            response = self._abode.send_request(
                "put", url, data=level_data)
            response_object = json.loads(response.text)

            _LOGGER.debug("Set Level Response: %s", response.text)

            if response_object['id'] != self.device_id:
                raise AbodeException((ERROR.SET_STATUS_DEV_ID))

            if response_object['level'] != str(level):
                raise AbodeException((ERROR.SET_STATUS_STATE))

            # TODO: Figure out where level is indicated in device json object

            _LOGGER.info("Set device %s level to: %s", self.device_id, level)

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

        response = self._abode.send_request(method="get", url=url)
        response_object = json.loads(response.text)

        _LOGGER.debug("Device Refresh Response: %s", response.text)

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
        # 'tempered' - Typo in API?
        return int(self.get_value('faults').get('tempered', '0')) == 1

    @property
    def name(self):
        """Get the name of this device."""
        return self._name

    @property
    def friendly_type(self):
        """Get the type of this device."""
        return self._type

    @property
    def type(self):
        """Get the type tag of this device."""
        return self._type_tag

    @property
    def device_id(self):
        """Get the device id."""
        return self._device_id
