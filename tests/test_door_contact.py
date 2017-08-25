"""Test the Abode device classes."""
import unittest

import requests_mock

import abodepy
import abodepy.helpers.constants as CONST

import tests.mock.login as LOGIN
import tests.mock.logout as LOGOUT
import tests.mock.panel as PANEL
import tests.mock.devices.door_contact as DOOR_CONTACT


USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestDoorContact(unittest.TestCase):
    """Test the generic AbodePy device class."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    @requests_mock.mock()
    def tests_contact_device_properties(self, m):
        """Tests that door contact device properties work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=DOOR_CONTACT.device(devid=DOOR_CONTACT.DEVICE_ID,
                                       status=CONST.STATUS_CLOSED,
                                       low_battery=False,
                                       no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our lock
        device = self.abode.get_device(DOOR_CONTACT.DEVICE_ID)

        # Test our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_CLOSED)
        self.assertFalse(device.battery_low)
        self.assertFalse(device.no_response)
        self.assertFalse(device.is_on)

        # Set up our direct device get url
        device_url = str.replace(CONST.DEVICE_URL,
                                 '$DEVID$', DOOR_CONTACT.DEVICE_ID)

        # Change device properties
        m.get(device_url,
              text=DOOR_CONTACT.device(devid=DOOR_CONTACT.DEVICE_ID,
                                       status=CONST.STATUS_OPEN,
                                       low_battery=True,
                                       no_response=True))

        # Refesh device and test changes
        device.refresh()

        self.assertEqual(device.status, CONST.STATUS_OPEN)
        self.assertTrue(device.battery_low)
        self.assertTrue(device.no_response)
        self.assertTrue(device.is_on)
