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
import tests.mock.devices.alarm as ALARM


USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestAlarm(unittest.TestCase):
    """Test the generic AbodePy device class."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD,
                                   disable_cache=True)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    @requests_mock.mock()
    def tests_abode_alarm_setup(self, m):
        """Check that Abode alarm device is set up properly."""
        panel = PANEL.get_response_ok(mode=CONST.MODE_STANDBY)
        alarm = ALARM.device(area='1', panel=panel)

        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.get(CONST.DEVICES_URL, text=DEVICES.EMPTY_DEVICE_RESPONSE)
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        alarm_device = self.abode.get_alarm()

        self.assertIsNotNone(alarm_device)
        # pylint: disable=W0212
        self.assertEqual(alarm_device._json_state, alarm)

    @requests_mock.mock()
    def tests_alarm_device_properties(self, m):
        """Check that the abode device properties are working."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(
            mode=CONST.MODE_STANDBY, battery=True, is_cellular=True,
            mac='01:AA:b3:C4:d5:66'))
        m.get(CONST.DEVICES_URL, text=DEVICES.EMPTY_DEVICE_RESPONSE)

        # Logout to reset everything
        self.abode.logout()

        # Get alarm and test
        alarm = self.abode.get_alarm()
        self.assertIsNotNone(alarm)
        self.assertEqual(alarm.mode, CONST.MODE_STANDBY)
        self.assertEqual(alarm.status, CONST.MODE_STANDBY)
        self.assertTrue(alarm.battery)
        self.assertTrue(alarm.is_cellular)
        self.assertFalse(alarm.is_on)
        self.assertEqual(alarm.device_uuid, '01aab3c4d566')
        self.assertEqual(alarm.mac_address, '01:AA:b3:C4:d5:66')

        # Change alarm properties and state to away and test
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(
            mode=CONST.MODE_AWAY, battery=False, is_cellular=False))

        # Refresh alarm and test
        alarm.refresh()

        self.assertEqual(alarm.mode, CONST.MODE_AWAY)
        self.assertEqual(alarm.status, CONST.MODE_AWAY)
        self.assertFalse(alarm.battery)
        self.assertFalse(alarm.is_cellular)
        self.assertTrue(alarm.is_on)

        # Change alarm state to final on state and test
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_HOME))

        # Refresh alarm and test
        alarm.refresh()
        self.assertEqual(alarm.mode, CONST.MODE_HOME)
        self.assertEqual(alarm.status, CONST.MODE_HOME)
        self.assertTrue(alarm.is_on)

    @requests_mock.mock()
    def tests_alarm_device_mode_changes(self, m):
        """Test that the abode alarm can change/report modes."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL, text=DEVICES.EMPTY_DEVICE_RESPONSE)

        # Logout to reset everything
        self.abode.logout()

        # Assert that after login we have our alarm device with standby mode
        alarm = self.abode.get_alarm()

        self.assertIsNotNone(alarm)
        self.assertEqual(alarm.status, CONST.MODE_STANDBY)

        # Set mode URLs
        m.put(CONST.get_panel_mode_url('1', CONST.MODE_STANDBY),
              text=PANEL.put_response_ok(mode=CONST.MODE_STANDBY))
        m.put(CONST.get_panel_mode_url('1', CONST.MODE_AWAY),
              text=PANEL.put_response_ok(mode=CONST.MODE_AWAY))
        m.put(CONST.get_panel_mode_url('1', CONST.MODE_HOME),
              text=PANEL.put_response_ok(mode=CONST.MODE_HOME))

        # Set and test text based mode changes
        self.assertTrue(alarm.set_mode(CONST.MODE_HOME))
        self.assertEqual(alarm.mode, CONST.MODE_HOME)
        self.assertFalse(alarm.is_standby)
        self.assertTrue(alarm.is_home)
        self.assertFalse(alarm.is_away)

        self.assertTrue(alarm.set_mode(CONST.MODE_AWAY))
        self.assertEqual(alarm.mode, CONST.MODE_AWAY)
        self.assertFalse(alarm.is_standby)
        self.assertFalse(alarm.is_home)
        self.assertTrue(alarm.is_away)

        self.assertTrue(alarm.set_mode(CONST.MODE_STANDBY))
        self.assertEqual(alarm.mode, CONST.MODE_STANDBY)
        self.assertTrue(alarm.is_standby)
        self.assertFalse(alarm.is_home)
        self.assertFalse(alarm.is_away)

        # Set and test direct mode changes
        self.assertTrue(alarm.set_home())
        self.assertEqual(alarm.mode, CONST.MODE_HOME)
        self.assertFalse(alarm.is_standby)
        self.assertTrue(alarm.is_home)
        self.assertFalse(alarm.is_away)

        self.assertTrue(alarm.set_away())
        self.assertEqual(alarm.mode, CONST.MODE_AWAY)
        self.assertFalse(alarm.is_standby)
        self.assertFalse(alarm.is_home)
        self.assertTrue(alarm.is_away)

        self.assertTrue(alarm.set_standby())
        self.assertEqual(alarm.mode, CONST.MODE_STANDBY)
        self.assertTrue(alarm.is_standby)
        self.assertFalse(alarm.is_home)
        self.assertFalse(alarm.is_away)

        # Set and test default mode changes
        self.assertTrue(alarm.switch_off())
        self.assertEqual(alarm.mode, CONST.MODE_STANDBY)
        self.assertTrue(alarm.is_standby)
        self.assertFalse(alarm.is_home)
        self.assertFalse(alarm.is_away)

        self.abode.set_default_mode(CONST.MODE_HOME)
        self.assertTrue(alarm.switch_on())
        self.assertEqual(alarm.mode, CONST.MODE_HOME)
        self.assertFalse(alarm.is_standby)
        self.assertTrue(alarm.is_home)
        self.assertFalse(alarm.is_away)

        self.assertTrue(alarm.switch_off())
        self.assertEqual(alarm.mode, CONST.MODE_STANDBY)
        self.assertTrue(alarm.is_standby)
        self.assertFalse(alarm.is_home)
        self.assertFalse(alarm.is_away)

        self.abode.set_default_mode(CONST.MODE_AWAY)
        self.assertTrue(alarm.switch_on())
        self.assertEqual(alarm.mode, CONST.MODE_AWAY)
        self.assertFalse(alarm.is_standby)
        self.assertFalse(alarm.is_home)
        self.assertTrue(alarm.is_away)

        # Test that no mode throws exception
        with self.assertRaises(abodepy.AbodeException):
            alarm.set_mode(mode=None)

        # Test that an invalid mode throws exception
        with self.assertRaises(abodepy.AbodeException):
            alarm.set_mode('chestnuts')

        # Test that an invalid mode change response throws exception
        m.put(CONST.get_panel_mode_url('1', CONST.MODE_HOME),
              text=PANEL.put_response_ok(mode=CONST.MODE_AWAY))

        with self.assertRaises(abodepy.AbodeException):
            alarm.set_mode(CONST.MODE_HOME)

        # Test that an invalid area in mode change response throws exception
        m.put(CONST.get_panel_mode_url('1', CONST.MODE_HOME),
              text=PANEL.put_response_ok(area='2', mode=CONST.MODE_HOME))

        with self.assertRaises(abodepy.AbodeException):
            alarm.set_mode(CONST.MODE_HOME)
