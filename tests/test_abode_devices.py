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
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE)
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE)
        
        device_text = '[' + mdev.GLASS_BREAK_DEVICE(status=const.STATUS_ONLINE) + ']'
        device_json = json.loads(device_text)

        m.get(const.DEVICES_URL, text=device_text)
        
        self.abode.devices = []
        device = self.abode.get_device(mdev.GLASS_BREAK_DEVICE_ID)
        
        self.assertIsNotNone(device)
        self.assertEquals(device.json_state, device_json[0])
        self.assertEquals(device.get_name(), device_json[0]['name'])
        self.assertEquals(device.get_type(), device_json[0]['type'])
        self.assertEquals(device.get_device_id(), device_json[0]['id'])
        self.assertEquals(device.get_status(), const.STATUS_ONLINE)
        
    @requests_mock.mock()
    def test_generic_device_refresh(self, m):
        """Check the generic Abode device class inits properly."""
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE)
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE)
        
        device_text_online = '[' + mdev.GLASS_BREAK_DEVICE(status=const.STATUS_ONLINE) + ']'
        device_json_online = json.loads(device_text_online)
        m.get(const.DEVICES_URL, text=device_text_online)
        
        device_text_offline = '[' + mdev.GLASS_BREAK_DEVICE(status=const.STATUS_OFFLINE) + ']'
        device_json_offline = json.loads(device_text_offline)
        device_url = const.DEVICE_URL.replace('$DEVID$', mdev.GLASS_BREAK_DEVICE_ID);
        m.get(device_url, text=device_text_offline)
        
        self.abode.devices = []
        device = self.abode.get_device(mdev.GLASS_BREAK_DEVICE_ID)
        self.assertEquals(device.get_status(), const.STATUS_ONLINE)
        
        device = self.abode.get_device(mdev.GLASS_BREAK_DEVICE_ID, refresh=True)
        self.assertEquals(device.get_status(), const.STATUS_OFFLINE)