"""Test the Abode device classes."""
import json
import unittest

import requests_mock

import abodepy
import abodepy.helpers.constants as CONST

import tests.mock.login as LOGIN
import tests.mock.logout as LOGOUT
import tests.mock.panel as PANEL
import tests.mock.devices as DEVICES
import tests.mock.devices.door_contact as DOOR_CONTACT
import tests.mock.devices.glass as GLASS
import tests.mock.devices.power_switch_sensor as POWERSENSOR


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
