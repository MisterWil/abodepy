"""Test the Abode device classes."""
import unittest

import requests_mock

import abodepy
import abodepy.helpers.constants as CONST

import tests.mock.login as LOGIN
import tests.mock.logout as LOGOUT
import tests.mock.panel as PANEL
import tests.mock.devices.lm as LM


USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestLM(unittest.TestCase):
    """Test the AbodePy sensor class/LM."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    @requests_mock.mock()
    def tests_cover_lm_properties(self, m):
        """Tests that sensor/LM devices properties work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=LM.device(devid=LM.DEVICE_ID,
                             status='72 °F',
                             temp='72 °F',
                             lux='14 lx',
                             humidity='34 %',
                             low_battery=False,
                             no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our power switch
        device = self.abode.get_device(LM.DEVICE_ID)

        # Test our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, '72 °F')
        self.assertFalse(device.battery_low)
        self.assertFalse(device.no_response)
        self.assertFalse(device.has_motion)
        self.assertFalse(device.has_occupancy)
        self.assertTrue(device.has_temp)
        self.assertTrue(device.has_humidity)
        self.assertTrue(device.has_lux)
        self.assertEqual(device.temp, 72)
        self.assertEqual(device.temp_unit, '°F')
        self.assertEqual(device.humidity, 34)
        self.assertEqual(device.humidity_unit, '%')
        self.assertEqual(device.lux, 14)
        self.assertEqual(device.lux_unit, 'lux')

        # Set up our direct device get url
        device_url = str.replace(CONST.DEVICE_URL,
                                 '$DEVID$', LM.DEVICE_ID)

        # Change device properties
        m.get(device_url,
              text=LM.device(devid=LM.DEVICE_ID,
                             status='12 °C',
                             temp='12 °C',
                             lux='100 lx',
                             humidity='100 %',
                             low_battery=True,
                             no_response=True))

        # Refesh device and test changes
        device.refresh()

        self.assertEqual(device.status, '12 °C')
        self.assertTrue(device.battery_low)
        self.assertTrue(device.no_response)
        self.assertTrue(device.has_temp)
        self.assertTrue(device.has_humidity)
        self.assertTrue(device.has_lux)
        self.assertEqual(device.temp, 12)
        self.assertEqual(device.temp_unit, '°C')
        self.assertEqual(device.humidity, 100)
        self.assertEqual(device.humidity_unit, '%')
        self.assertEqual(device.lux, 100)
        self.assertEqual(device.lux_unit, 'lux')

    @requests_mock.mock()
    def tests_lm_float_units(self, m):
        """Tests that sensor/LM devices properties work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=LM.device(devid=LM.DEVICE_ID,
                             status='72.23 °F',
                             temp='72.23 °F',
                             lux='14.11 lx',
                             humidity='34.38 %',
                             low_battery=False,
                             no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our power switch
        device = self.abode.get_device(LM.DEVICE_ID)

        # Test our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, '72.23 °F')
        self.assertFalse(device.battery_low)
        self.assertFalse(device.no_response)
        self.assertTrue(device.has_temp)
        self.assertTrue(device.has_humidity)
        self.assertTrue(device.has_lux)
        self.assertEqual(device.temp, 72.23)
        self.assertEqual(device.temp_unit, '°F')
        self.assertEqual(device.humidity, 34.38)
        self.assertEqual(device.humidity_unit, '%')
        self.assertEqual(device.lux, 14.11)
        self.assertEqual(device.lux_unit, 'lux')

    @requests_mock.mock()
    def tests_lm_temp_only(self, m):
        """Tests that sensor/LM devices properties work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=LM.device(devid=LM.DEVICE_ID,
                             status='72 °F',
                             temp='72 °F',
                             lux='',
                             humidity=''))

        # Logout to reset everything
        self.abode.logout()

        # Get our power switch
        device = self.abode.get_device(LM.DEVICE_ID)

        # Test our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, '72 °F')
        self.assertTrue(device.has_temp)
        self.assertFalse(device.has_humidity)
        self.assertFalse(device.has_lux)
        self.assertEqual(device.temp, 72)
        self.assertEqual(device.temp_unit, '°F')
        self.assertIsNone(device.humidity)
        self.assertIsNone(device.humidity_unit)
        self.assertIsNone(device.lux)
        self.assertIsNone(device.lux_unit)
