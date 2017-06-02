"""
Test the Abode device classes.
"""
import json
import unittest
import requests_mock
from unittest import mock
import abodepy
import tests.mock_responses as mresp
import tests.mock_devices as mdev
import helpers.constants as const

USERNAME = 'foobar'
PASSWORD = 'deadbeef'

class TestAbodeDevicesSetup(unittest.TestCase):
    """Test the Abode device classes in abodepy."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None
        
    @requests_mock.mock()
    def test_generic_device_init(self, m):
        """Check the generic Abode device class inits properly."""
        # Set up URLs
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE)
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE())
        
        # Set up device
        device_text = '[' + mdev.GLASS_BREAK_DEVICE(status=const.STATUS_ONLINE, low_battery=True, no_response=True) + ']'
        device_json = json.loads(device_text)

        m.get(const.DEVICES_URL, text=device_text)
        
        # Logout to reset everything
        self.abode.logout()
        
        # Get our specific device
        device = self.abode.get_device(mdev.GLASS_BREAK_DEVICE_ID)
        
        # Check device states match
        self.assertIsNotNone(device)
        self.assertEqual(device._json_state, device_json[0])
        self.assertEqual(device.name, device_json[0]['name'])
        self.assertEqual(device.type, device_json[0]['type'])
        self.assertEqual(device.device_id, device_json[0]['id'])
        self.assertEqual(device.status, const.STATUS_ONLINE)
        self.assertTrue(device.battery_low)
        self.assertTrue(device.no_response)
        
    @requests_mock.mock()
    def test_generic_device_refresh(self, m):
        """Check the generic Abode device class inits properly."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE)
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE())
        
        # Set up online device
        device_text_online = '[' + mdev.GLASS_BREAK_DEVICE(status=const.STATUS_ONLINE) + ']'
        device_json_online = json.loads(device_text_online)
        m.get(const.DEVICES_URL, text=device_text_online)
        
        # Set up offline device
        device_text_offline = '[' + mdev.GLASS_BREAK_DEVICE(status=const.STATUS_OFFLINE) + ']'
        device_json_offline = json.loads(device_text_offline)
        device_url = const.DEVICE_URL.replace('$DEVID$', mdev.GLASS_BREAK_DEVICE_ID);
        m.get(device_url, text=device_text_offline)
        
        # Logout to reset everything
        self.abode.logout()
        
        # Get the first device and test
        device = self.abode.get_device(mdev.GLASS_BREAK_DEVICE_ID)
        self.assertEqual(device.status, const.STATUS_ONLINE)
        
        # Refresh the device and test
        device = self.abode.get_device(mdev.GLASS_BREAK_DEVICE_ID, refresh=True)
        self.assertEqual(device.status, const.STATUS_OFFLINE)
    
    @requests_mock.mock()
    def test_alarm_device_properties(self, m):
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE)
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE(mode=const.MODE_STANDBY, battery=True, is_cellular=True))
        m.get(const.DEVICES_URL, text=mresp.EMPTY_DEVICE_RESPONSE)
        
        # Logout to reset everything
        self.abode.logout()
        
        # Get alarm and test
        alarm = self.abode.get_alarm()
        self.assertIsNotNone(alarm)
        self.assertEqual(alarm.mode, const.MODE_STANDBY)
        self.assertEqual(alarm.status, const.MODE_STANDBY)
        self.assertTrue(alarm.battery)
        self.assertTrue(alarm.is_cellular)
        self.assertFalse(alarm.is_on)
        
        # Change alarm properties and state to away and test
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE(mode=const.MODE_AWAY, battery=False, is_cellular=False))
        
        # Refresh alarm and test
        alarm.refresh()
        
        self.assertEqual(alarm.mode, const.MODE_AWAY)
        self.assertEqual(alarm.status, const.MODE_AWAY)
        self.assertFalse(alarm.battery)
        self.assertFalse(alarm.is_cellular)
        self.assertTrue(alarm.is_on)
        
        # Change alarm state to final on state and test
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE(mode=const.MODE_HOME))
        
        # Refresh alarm and test
        alarm.refresh()
        self.assertEqual(alarm.mode, const.MODE_HOME)
        self.assertEqual(alarm.status, const.MODE_HOME)
        self.assertTrue(alarm.is_on)
    
    @requests_mock.mock()
    def test_alarm_device_refresh(self, m):
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE)
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE(mode=const.MODE_STANDBY))
        m.get(const.DEVICES_URL, text=mresp.EMPTY_DEVICE_RESPONSE)
        
        # Logout to reset everything
        self.abode.logout()
        
        # Assert that after login we have our alarm device
        alarm = self.abode.get_alarm()
        
        self.assertIsNotNone(alarm)
        self.assertEqual(alarm.mode, const.MODE_STANDBY)
        
        # Set new status response
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE(mode=const.MODE_AWAY))
        
        alarm.refresh()
        
        self.assertEqual(alarm.mode, const.MODE_AWAY)
        
    @requests_mock.mock()
    def test_alarm_device_mode_changes(self, m):
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE)
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE(mode=const.MODE_STANDBY))
        m.get(const.DEVICES_URL, text=mresp.EMPTY_DEVICE_RESPONSE)
        
        # Logout to reset everything
        self.abode.logout()
        
        # Assert that after login we have our alarm device with standby mode
        alarm = self.abode.get_alarm()
        
        self.assertIsNotNone(alarm)
        self.assertEqual(alarm.status, const.MODE_STANDBY)
        
        # Set mode URLs
        m.put(const.PANEL_MODE_URL('1', const.MODE_STANDBY),
              text=mresp.PANEL_MODE_RESPONSE(area='1', mode=const.MODE_STANDBY))
        m.put(const.PANEL_MODE_URL('1', const.MODE_AWAY),
              text=mresp.PANEL_MODE_RESPONSE(area='1', mode=const.MODE_AWAY))
        m.put(const.PANEL_MODE_URL('1', const.MODE_HOME),
              text=mresp.PANEL_MODE_RESPONSE(area='1', mode=const.MODE_HOME))

        # Set and test text based mode changes
        self.assertTrue(alarm.set_mode(const.MODE_HOME))
        self.assertEqual(alarm.mode, const.MODE_HOME)
        
        self.assertTrue(alarm.set_mode(const.MODE_AWAY))
        self.assertEqual(alarm.mode, const.MODE_AWAY)
        
        self.assertTrue(alarm.set_mode(const.MODE_STANDBY))
        self.assertEqual(alarm.mode, const.MODE_STANDBY)
        
        # Set and test direct mode changes
        self.assertTrue(alarm.set_home())
        self.assertEqual(alarm.mode, const.MODE_HOME)
        
        self.assertTrue(alarm.set_away())
        self.assertEqual(alarm.mode, const.MODE_AWAY)
        
        self.assertTrue(alarm.set_standby())
        self.assertEqual(alarm.mode, const.MODE_STANDBY)