"""Test the Abode device classes."""
import unittest

import requests_mock

import abodepy
import abodepy.helpers.constants as CONST

import tests.mock.login as LOGIN
import tests.mock.logout as LOGOUT
import tests.mock.panel as PANEL
import tests.mock.devices as DEVICES
import tests.mock.devices.secure_barrier as COVER


USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestSecureBarrier(unittest.TestCase):
    """Test the AbodePy cover class."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    @requests_mock.mock()
    def tests_cover_device_properties(self, m):
        """Tests that cover devices properties work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=COVER.device(devid=COVER.DEVICE_ID,
                                status=CONST.STATUS_CLOSED,
                                low_battery=False,
                                no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our power switch
        device = self.abode.get_device(COVER.DEVICE_ID)

        # Test our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_CLOSED)
        self.assertFalse(device.battery_low)
        self.assertFalse(device.no_response)
        self.assertFalse(device.is_on)
        self.assertFalse(device.is_open)

        # Set up our direct device get url
        device_url = str.replace(CONST.DEVICE_URL,
                                 '$DEVID$', COVER.DEVICE_ID)

        # Change device properties
        m.get(device_url,
              text=COVER.device(devid=COVER.DEVICE_ID,
                                status=CONST.STATUS_OPEN,
                                low_battery=True,
                                no_response=True))

        # Refesh device and test changes
        device.refresh()

        self.assertEqual(device.status, CONST.STATUS_OPEN)
        self.assertTrue(device.battery_low)
        self.assertTrue(device.no_response)
        self.assertTrue(device.is_on)
        self.assertTrue(device.is_open)

    @requests_mock.mock()
    def tests_cover_status_changes(self, m):
        """Tests that cover device changes work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=COVER.device(devid=COVER.DEVICE_ID,
                                status=CONST.STATUS_CLOSED,
                                low_battery=False,
                                no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our power switch
        device = self.abode.get_device(COVER.DEVICE_ID)

        # Test that we have our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_CLOSED)
        self.assertFalse(device.is_open)

        # Set up control url response
        control_url = CONST.BASE_URL + COVER.CONTROL_URL
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid=COVER.DEVICE_ID,
                  status=CONST.STATUS_OPEN_INT))

        # Change the cover to open
        self.assertTrue(device.open_cover())
        self.assertEqual(device.status, CONST.STATUS_OPEN)
        self.assertTrue(device.is_open)

        # Change response
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid=COVER.DEVICE_ID,
                  status=CONST.STATUS_CLOSED_INT))

        # Change the mode to "off"
        self.assertTrue(device.close_cover())
        self.assertEqual(device.status, CONST.STATUS_CLOSED)
        self.assertFalse(device.is_open)
