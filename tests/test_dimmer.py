"""Test the Abode device classes."""
import unittest

import requests_mock

import abodepy
import abodepy.helpers.constants as CONST

import tests.mock.login as LOGIN
import tests.mock.oauth_claims as OAUTH_CLAIMS
import tests.mock.logout as LOGOUT
import tests.mock.panel as PANEL
import tests.mock.devices as DEVICES
import tests.mock.devices.dimmer as DIMMER


USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestDimmer(unittest.TestCase):
    """Test the AbodePy light device with a dimmer."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD,
                                   disable_cache=True)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    @requests_mock.mock()
    def tests_dimmer_device_properties(self, m):
        """Tests that dimmer light devices properties work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=DIMMER.device(devid=DIMMER.DEVICE_ID,
                                 status=CONST.STATUS_OFF,
                                 level=0,
                                 low_battery=False,
                                 no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our dimmer
        device = self.abode.get_device(DIMMER.DEVICE_ID)

        # Test our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_OFF)
        self.assertEqual(device.brightness, "0")
        self.assertTrue(device.has_brightness)
        self.assertTrue(device.is_dimmable)
        self.assertFalse(device.has_color)
        self.assertFalse(device.is_color_capable)
        self.assertFalse(device.battery_low)
        self.assertFalse(device.no_response)
        self.assertFalse(device.is_on)

        # Set up our direct device get url
        device_url = str.replace(CONST.DEVICE_URL,
                                 '$DEVID$', DIMMER.DEVICE_ID)

        # Change device properties
        m.get(device_url,
              text=DIMMER.device(devid=DIMMER.DEVICE_ID,
                                 status=CONST.STATUS_ON,
                                 level=87,
                                 low_battery=True,
                                 no_response=True))

        # Refesh device and test changes
        device.refresh()

        self.assertEqual(device.status, CONST.STATUS_ON)
        self.assertEqual(device.brightness, "87")
        self.assertTrue(device.battery_low)
        self.assertTrue(device.no_response)
        self.assertTrue(device.is_on)

    @requests_mock.mock()
    def tests_dimmer_status_changes(self, m):
        """Tests that dimmer device changes work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=DIMMER.device(devid=DIMMER.DEVICE_ID,
                                 status=CONST.STATUS_OFF,
                                 level=0,
                                 low_battery=False,
                                 no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our dimmer
        device = self.abode.get_device(DIMMER.DEVICE_ID)

        # Test that we have our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_OFF)
        self.assertFalse(device.is_on)

        # Set up control url response
        control_url = CONST.BASE_URL + DIMMER.CONTROL_URL
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid=DIMMER.DEVICE_ID,
                  status=CONST.STATUS_ON_INT))

        # Change the mode to "on"
        self.assertTrue(device.switch_on())
        self.assertEqual(device.status, CONST.STATUS_ON)
        self.assertTrue(device.is_on)

        # Change response
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid=DIMMER.DEVICE_ID,
                  status=CONST.STATUS_OFF_INT))

        # Change the mode to "off"
        self.assertTrue(device.switch_off())
        self.assertEqual(device.status, CONST.STATUS_OFF)
        self.assertFalse(device.is_on)

        # Test that an invalid status response throws exception
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid=DIMMER.DEVICE_ID,
                  status=CONST.STATUS_OFF_INT))

        with self.assertRaises(abodepy.AbodeException):
            device.switch_on()
