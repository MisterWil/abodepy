"""Test the Abode device classes."""
import json
import unittest

import requests_mock

import abodepy

from abodepy.devices.alarm import AbodeAlarm
from abodepy.devices.binary_sensor import AbodeBinarySensor
from abodepy.devices.cover import AbodeCover
from abodepy.devices.lock import AbodeLock
from abodepy.devices.switch import AbodeSwitch
import abodepy.helpers.constants as CONST
import tests.mock.devices as DEVICES
import tests.mock.devices.door_contact as DOOR_CONTACT
import tests.mock.devices.door_lock as DOOR_LOCK
import tests.mock.devices.glass as GLASS
import tests.mock.devices.ir_camera as IR_CAMERA
import tests.mock.devices.keypad as KEYPAD
import tests.mock.devices.pir as PIR
import tests.mock.devices.power_switch_meter as POWERMETER
import tests.mock.devices.power_switch_sensor as POWERSENSOR
import tests.mock.devices.remote_controller as REMOTE_CONTROLLER
import tests.mock.devices.secure_barrier as SECUREBARRIER
import tests.mock.devices.siren as SIREN
import tests.mock.devices.status_display as STATUS_DISPLAY
import tests.mock.devices.water_sensor as WATER_SENSOR
import tests.mock.login as LOGIN
import tests.mock.logout as LOGOUT
import tests.mock.panel as PANEL


USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestDevice(unittest.TestCase):
    """Test the generic AbodePy device class."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    def tests_device_mapping_typetag(self):
        """Check the generic Abode device maps to none without typetag."""
        # Set up device
        device_text = GLASS.device(
            status=CONST.STATUS_ONLINE,
            low_battery=True, no_response=True,
            tampered=True, out_of_order=True)

        device_json = json.loads(device_text)

        with self.assertRaises(abodepy.AbodeException):
            device_json['type_tag'] = ""
            abodepy.new_device(device_json, self.abode)

        with self.assertRaises(abodepy.AbodeException):
            device_json['type_tag'] = None
            abodepy.new_device(device_json, self.abode)

        with self.assertRaises(abodepy.AbodeException):
            del device_json['type_tag']
            abodepy.new_device(device_json, self.abode)

    def tests_device_auto_naming(self):
        """Check the generic Abode device creates a name."""
        # Set up device
        device_text = GLASS.device(
            status=CONST.STATUS_ONLINE,
            low_battery=True, no_response=True,
            tampered=True, out_of_order=True)

        device_json = json.loads(device_text)

        device_json['name'] = ""
        device = abodepy.new_device(device_json, self.abode)
        generated_name = device.friendly_type + ' ' + device.device_id
        self.assertEqual(device.name, generated_name)

        device_json['name'] = None
        device = abodepy.new_device(device_json, self.abode)
        generated_name = device.friendly_type + ' ' + device.device_id
        self.assertEqual(device.name, generated_name)

        del device_json['name']
        device = abodepy.new_device(device_json, self.abode)
        generated_name = device.friendly_type + ' ' + device.device_id
        self.assertEqual(device.name, generated_name)

    @requests_mock.mock()
    def tests_device_init(self, m):
        """Check the generic Abode device class init's properly."""
        # Set up URLs
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        # Set up device
        device_text = '[' + GLASS.device(
            status=CONST.STATUS_ONLINE,
            low_battery=True, no_response=True,
            tampered=True, out_of_order=True) + ']'
        device_json = json.loads(device_text)

        m.get(CONST.DEVICES_URL, text=device_text)

        # Logout to reset everything
        self.abode.logout()

        # Get our specific device
        device = self.abode.get_device(GLASS.DEVICE_ID)

        # Check device states match
        self.assertIsNotNone(device)
        # pylint: disable=W0212
        self.assertEqual(device._json_state, device_json[0])
        self.assertEqual(device.name, device_json[0]['name'])
        self.assertEqual(device.type, device_json[0]['type_tag'])
        self.assertEqual(device.friendly_type, device_json[0]['type'])
        self.assertEqual(device.device_id, device_json[0]['id'])
        self.assertEqual(device.status, CONST.STATUS_ONLINE)
        self.assertTrue(device.battery_low)
        self.assertTrue(device.no_response)
        self.assertTrue(device.tampered)
        self.assertTrue(device.out_of_order)
        self.assertIsNotNone(device.desc)

    @requests_mock.mock()
    def tests_generic_device_refresh(self, m):
        """Check the generic Abode device class init's properly."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        # Set up online device
        device_text_online = '[' + \
            GLASS.device(status=CONST.STATUS_ONLINE) + ']'
        m.get(CONST.DEVICES_URL, text=device_text_online)

        # Set up offline device
        device_text_offline = '[' + \
            GLASS.device(status=CONST.STATUS_OFFLINE) + ']'
        device_url = str.replace(CONST.DEVICE_URL,
                                 '$DEVID$', GLASS.DEVICE_ID)
        m.get(device_url, text=device_text_offline)

        # Logout to reset everything
        self.abode.logout()

        # Get the first device and test
        device = self.abode.get_device(GLASS.DEVICE_ID)
        self.assertEqual(device.status, CONST.STATUS_ONLINE)

        # Refresh the device and test
        device = self.abode.get_device(
            GLASS.DEVICE_ID, refresh=True)
        self.assertEqual(device.status, CONST.STATUS_OFFLINE)

    @requests_mock.mock()
    def tests_multiple_devices(self, m):
        """Tests that multiple devices are returned properly."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))

        # Set up a list of devices
        dev_list = '[' + \
            POWERSENSOR.device() + "," + \
            DOOR_CONTACT.device() + "," + \
            GLASS.device() + ']'

        m.get(CONST.DEVICES_URL, text=dev_list)

        # Logout to reset everything
        self.abode.logout()

        # Get our devices
        devices = self.abode.get_devices()

        # Assert four devices - three from above + 1 alarm
        self.assertIsNotNone(devices)
        self.assertEqual(len(devices), 4)

        # Get each individual device by device ID
        psd = self.abode.get_device(POWERSENSOR.DEVICE_ID)
        self.assertIsNotNone(psd)

        # Get each individual device by device ID
        psd = self.abode.get_device(DOOR_CONTACT.DEVICE_ID)
        self.assertIsNotNone(psd)

        # Get each individual device by device ID
        psd = self.abode.get_device(GLASS.DEVICE_ID)
        self.assertIsNotNone(psd)

    @requests_mock.mock()
    def tests_device_category_filter(self, m):
        """Tests that device category filter returns requested results."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))

        # Set up a list of devices
        dev_list = '[' + \
            POWERSENSOR.device(devid='ps1',
                               status=CONST.STATUS_OFF,
                               low_battery=False,
                               no_response=False) + "," + \
            POWERSENSOR.device(devid='ps2',
                               status=CONST.STATUS_OFF,
                               low_battery=False,
                               no_response=False) + "," + \
            GLASS.device(devid='gb1',
                         status=CONST.STATUS_OFF,
                         low_battery=False,
                         no_response=False) + ']'

        m.get(CONST.DEVICES_URL, text=dev_list)

        # Logout to reset everything
        self.abode.logout()

        # Get our glass devices
        devices = self.abode.get_devices(
            type_filter=(CONST.DEVICE_GLASS_BREAK))

        self.assertIsNotNone(devices)
        self.assertEqual(len(devices), 1)

        # Get our power switch devices
        devices = self.abode.get_devices(
            type_filter=(CONST.DEVICE_POWER_SWITCH_SENSOR))

        self.assertIsNotNone(devices)
        self.assertEqual(len(devices), 2)

    @requests_mock.mock()
    def tests_no_control_url(self, m):
        """Check that devices return false without control url's."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        m.get(CONST.DEVICES_URL,
              text=GLASS.device(status=CONST.STATUS_ONLINE))

        # Logout to reset everything
        self.abode.logout()

        # Get device
        device = self.abode.get_device(GLASS.DEVICE_ID)

        self.assertIsNotNone(device)
        self.assertFalse(device.set_status('1'))
        self.assertFalse(device.set_level('99'))

    @requests_mock.mock()
    def tests_device_status_changes(self, m):
        """Tests that device status changes work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=POWERSENSOR.device(devid=POWERSENSOR.DEVICE_ID,
                                      status=CONST.STATUS_OFF,
                                      low_battery=False,
                                      no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our power switch
        device = self.abode.get_device(POWERSENSOR.DEVICE_ID)

        # Test that we have our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_OFF)
        self.assertFalse(device.is_on)

        # Set up control url response
        control_url = CONST.BASE_URL + POWERSENSOR.CONTROL_URL
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid=POWERSENSOR.DEVICE_ID,
                  status=CONST.STATUS_ON_INT))

        # Change the mode to "on"
        self.assertTrue(device.switch_on())
        self.assertEqual(device.status, CONST.STATUS_ON)
        self.assertTrue(device.is_on)

        # Change response
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid=POWERSENSOR.DEVICE_ID,
                  status=CONST.STATUS_OFF_INT))

        # Change the mode to "off"
        self.assertTrue(device.switch_off())
        self.assertEqual(device.status, CONST.STATUS_OFF)
        self.assertFalse(device.is_on)

        # Test that an invalid device ID in response throws exception
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid='ZW:deadbeef',
                  status=CONST.STATUS_OFF_INT))

        with self.assertRaises(abodepy.AbodeException):
            device.switch_on()

        # Test that an invalid status in response throws exception
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid=POWERSENSOR.DEVICE_ID,
                  status=CONST.STATUS_OFF_INT))

        with self.assertRaises(abodepy.AbodeException):
            device.switch_on()

    @requests_mock.mock()
    def tests_device_level_changes(self, m):
        """Tests that device level changes work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))

        # TODO: Test with a device that supports levels
        m.get(CONST.DEVICES_URL,
              text=POWERSENSOR.device(devid=POWERSENSOR.DEVICE_ID,
                                      status=CONST.STATUS_OFF,
                                      low_battery=False,
                                      no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our power switch
        device = self.abode.get_device(POWERSENSOR.DEVICE_ID)

        # Test that we have our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_OFF)
        self.assertFalse(device.is_on)

        # Set up control url response
        control_url = CONST.BASE_URL + POWERSENSOR.CONTROL_URL
        m.put(control_url,
              text=DEVICES.level_put_response_ok(
                  devid=POWERSENSOR.DEVICE_ID,
                  level='100'))

        # Change the level to int 100
        self.assertTrue(device.set_level(100))
        # self.assertEqual(device.level, '100')

        # Change response
        control_url = CONST.BASE_URL + POWERSENSOR.CONTROL_URL
        m.put(control_url,
              text=DEVICES.level_put_response_ok(
                  devid=POWERSENSOR.DEVICE_ID,
                  level='25'))

        # Change the level to str '25'
        self.assertTrue(device.set_level('25'))
        # self.assertEqual(device.level, '25')

        # Test that an invalid device ID in response throws exception
        m.put(control_url,
              text=DEVICES.level_put_response_ok(
                  devid='ZW:deadbeef',
                  level='25'))

        with self.assertRaises(abodepy.AbodeException):
            device.set_level(25)

        # Test that an invalid level in response throws exception
        m.put(control_url,
              text=DEVICES.level_put_response_ok(
                  devid=POWERSENSOR.DEVICE_ID,
                  level='98'))

        with self.assertRaises(abodepy.AbodeException):
            device.set_level('28')

    @requests_mock.mock()
    def tests_all_devices(self, m):
        """Tests that all supported devices are mapped correctly."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))

        # Create all devices
        all_devices = '[' + \
            DOOR_CONTACT.device() + ',' + \
            DOOR_LOCK.device() + ',' + \
            GLASS.device() + ',' + \
            IR_CAMERA.device() + ',' + \
            KEYPAD.device() + ',' + \
            PIR.device() + ',' + \
            POWERMETER.device() + ',' + \
            POWERSENSOR.device() + ',' + \
            REMOTE_CONTROLLER.device() + ',' + \
            SECUREBARRIER.device() + ',' + \
            SIREN.device() + ',' + \
            STATUS_DISPLAY.device() + ',' + \
            WATER_SENSOR.device() + ']'

        m.get(CONST.DEVICES_URL, text=all_devices)

        # Logout to reset everything
        self.abode.logout()

        # Loop through all devices
        for device in self.abode.get_devices():
            class_type = {
                CONST.DEVICE_ALARM: AbodeAlarm,
                CONST.DEVICE_GLASS_BREAK: AbodeBinarySensor,
                CONST.DEVICE_KEYPAD: AbodeBinarySensor,
                CONST.DEVICE_DOOR_CONTACT: AbodeBinarySensor,
                CONST.DEVICE_STATUS_DISPLAY: AbodeBinarySensor,
                CONST.DEVICE_MOTION_CAMERA: AbodeBinarySensor,
                CONST.DEVICE_DOOR_LOCK: AbodeLock,
                CONST.DEVICE_POWER_SWITCH_SENSOR: AbodeSwitch,
                CONST.DEVICE_POWER_SWITCH_METER: AbodeSwitch,
                CONST.DEVICE_WATER_SENSOR: AbodeBinarySensor,
                CONST.DEVICE_SECURE_BARRIER: AbodeCover,
                CONST.DEVICE_PIR: AbodeBinarySensor,
                CONST.DEVICE_REMOTE_CONTROLLER: AbodeBinarySensor,
                CONST.DEVICE_SIREN: AbodeBinarySensor
            }.get(device.type)

            self.assertIsNotNone(class_type, device.type + ' is not mapped.')
            self.assertTrue(isinstance(device, class_type))
