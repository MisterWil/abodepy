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
import tests.mock.devices.hue as HUE


USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestHue(unittest.TestCase):
    """Test the AbodePy light device with Hue."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD,
                                   disable_cache=True)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    @requests_mock.mock()
    def tests_hue_device_properties(self, m):
        """Tests that hue light devices properties work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=HUE.device(devid=HUE.DEVICE_ID,
                              status=CONST.STATUS_OFF,
                              level=0,
                              saturation=57,
                              hue=60,
                              color_temp=6536,
                              color_mode=CONST.COLOR_MODE_ON,
                              low_battery=False,
                              no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our dimmer
        device = self.abode.get_device(HUE.DEVICE_ID)

        # Test our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_OFF)
        self.assertEqual(device.brightness, "0")
        self.assertEqual(device.color, (60, 57))  # (hue, saturation)
        self.assertEqual(device.color_temp, 6536)
        self.assertTrue(device.has_brightness)
        self.assertTrue(device.is_dimmable)
        self.assertTrue(device.has_color)
        self.assertTrue(device.is_color_capable)
        self.assertFalse(device.battery_low)
        self.assertFalse(device.no_response)
        self.assertFalse(device.is_on)

        # Set up our direct device get url
        device_url = str.replace(CONST.DEVICE_URL,
                                 '$DEVID$', HUE.DEVICE_ID)

        # Change device properties
        m.get(device_url,
              text=HUE.device(devid=HUE.DEVICE_ID,
                              status=CONST.STATUS_ON,
                              level=45,
                              saturation=22,
                              hue=104,
                              color_temp=4000,
                              color_mode=CONST.COLOR_MODE_OFF,
                              low_battery=True,
                              no_response=True))

        # Refesh device and test changes
        device.refresh()

        self.assertEqual(device.status, CONST.STATUS_ON)
        self.assertEqual(device.color, (104, 22))  # (hue, saturation)
        self.assertEqual(device.color_temp, 4000)
        self.assertTrue(device.has_brightness)
        self.assertTrue(device.is_dimmable)
        self.assertFalse(device.has_color)
        self.assertTrue(device.is_color_capable)
        self.assertTrue(device.battery_low)
        self.assertTrue(device.no_response)
        self.assertTrue(device.is_on)

    @requests_mock.mock()
    def tests_hue_status_changes(self, m):
        """Tests that hue device changes work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=HUE.device(devid=HUE.DEVICE_ID,
                              status=CONST.STATUS_OFF,
                              level=0,
                              saturation=57,
                              hue=60,
                              color_temp=6536,
                              color_mode=CONST.COLOR_MODE_ON,
                              low_battery=False,
                              no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our hue device
        device = self.abode.get_device(HUE.DEVICE_ID)

        # Test that we have our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_OFF)
        self.assertFalse(device.is_on)

        # Set up control url response
        control_url = CONST.BASE_URL + HUE.CONTROL_URL
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid=HUE.DEVICE_ID,
                  status=CONST.STATUS_ON_INT))

        # Change the mode to "on"
        self.assertTrue(device.switch_on())
        self.assertEqual(device.status, CONST.STATUS_ON)
        self.assertTrue(device.is_on)

        # Change response
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid=HUE.DEVICE_ID,
                  status=CONST.STATUS_OFF_INT))

        # Change the mode to "off"
        self.assertTrue(device.switch_off())
        self.assertEqual(device.status, CONST.STATUS_OFF)
        self.assertFalse(device.is_on)

        # Test that an invalid status response throws exception
        m.put(control_url,
              text=DEVICES.status_put_response_ok(
                  devid=HUE.DEVICE_ID,
                  status=CONST.STATUS_OFF_INT))

        with self.assertRaises(abodepy.AbodeException):
            device.switch_on()

    @requests_mock.mock()
    def tests_hue_color_temp_changes(self, m):
        """Tests that hue device color temp changes work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=HUE.device(devid=HUE.DEVICE_ID,
                              status=CONST.STATUS_OFF,
                              level=0,
                              saturation=57,
                              hue=60,
                              color_temp=6536,
                              color_mode=CONST.COLOR_MODE_ON,
                              low_battery=False,
                              no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our hue device
        device = self.abode.get_device(HUE.DEVICE_ID)

        # Test that we have our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_OFF)
        self.assertFalse(device.is_on)
        self.assertEqual(device.color_temp, 6536)

        # Set up integrations url response
        m.post(HUE.INTEGRATIONS_URL,
               text=HUE.color_temp_post_response_ok(
                   devid=HUE.DEVICE_ID,
                   color_temp=5554))

        # Change the color temp
        self.assertTrue(device.set_color_temp(5554))
        self.assertEqual(device.color_temp, 5554)

        # Change response
        m.post(HUE.INTEGRATIONS_URL,
               text=HUE.color_temp_post_response_ok(
                   devid=HUE.DEVICE_ID,
                   color_temp=4434))

        # Change the color to something that mismatches
        self.assertTrue(device.set_color_temp(4436))

        # Assert that the color is set to the response color
        self.assertEqual(device.color_temp, 4434)

        # Test that an invalid ID in response throws exception
        m.post(HUE.INTEGRATIONS_URL,
               text=HUE.color_temp_post_response_ok(
                   devid=(HUE.DEVICE_ID + "23"),
                   color_temp=4434))

        with self.assertRaises(abodepy.AbodeException):
            device.set_color_temp(4434)

    @requests_mock.mock()
    def tests_hue_color_changes(self, m):
        """Tests that hue device color changes work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=HUE.device(devid=HUE.DEVICE_ID,
                              status=CONST.STATUS_OFF,
                              level=0,
                              saturation=57,
                              hue=60,
                              color_temp=6536,
                              color_mode=CONST.COLOR_MODE_ON,
                              low_battery=False,
                              no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our hue device
        device = self.abode.get_device(HUE.DEVICE_ID)

        # Test that we have our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_OFF)
        self.assertFalse(device.is_on)
        self.assertEqual(device.color, (60, 57))  # (hue, saturation)

        # Set up integrations url response
        m.post(HUE.INTEGRATIONS_URL,
               text=HUE.color_post_response_ok(
                   devid=HUE.DEVICE_ID,
                   hue=70,
                   saturation=80))

        # Change the color temp
        self.assertTrue(device.set_color((70, 80)))
        self.assertEqual(device.color, (70, 80))  # (hue, saturation)

        # Change response
        m.post(HUE.INTEGRATIONS_URL,
               text=HUE.color_post_response_ok(
                   devid=HUE.DEVICE_ID,
                   hue=55,
                   saturation=85))

        # Change the color to something that mismatches
        self.assertTrue(device.set_color((44, 44)))

        # Assert that the color is set to the response color
        self.assertEqual(device.color, (55, 85))  # (hue, saturation)

        # Test that an invalid ID in response throws exception
        m.post(HUE.INTEGRATIONS_URL,
               text=HUE.color_post_response_ok(
                   devid=(HUE.DEVICE_ID + "23"),
                   hue=55,
                   saturation=85))

        with self.assertRaises(abodepy.AbodeException):
            device.set_color((44, 44))
