"""
Test full system.
Tests the system initialization and attributes of the main Abode system.
"""
import json
import unittest
import requests_mock
from unittest import mock
import abodepy
import tests.mock_responses as mresp
import helpers.constants as const

USERNAME = 'foobar'
PASSWORD = 'deadbeef'

class TestAbodeSetup(unittest.TestCase):
    """Test the Abode class in abodepy."""

    def setUp(self):
        """Set up Abode module."""
        self.abode_no_cred = abodepy.Abode()
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None
        self.abode_no_cred = None

    def test_initialization(self):
        """Verify we can initialize abode."""
        # pylint: disable=protected-access
        self.assertEqual(self.abode._username, USERNAME)
        # pylint: disable=protected-access
        self.assertEqual(self.abode._password, PASSWORD)

    def test_no_credentials(self):
        """Check that we throw an exception when no username/password."""
        with self.assertRaises(abodepy.AbodeAuthenticationException):
            self.abode_no_cred.login()
            
        # pylint: disable=protected-access
        self.abode_no_cred._username = USERNAME
        with self.assertRaises(abodepy.AbodeAuthenticationException):
            self.abode_no_cred.login()
    
    @requests_mock.mock()
    def test_manual_login(self, m):
        """Check that we can manually use the login() function."""
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE)
        
        self.abode_no_cred.login(username=USERNAME, password=PASSWORD)
        
        # pylint: disable=protected-access
        self.assertEqual(self.abode_no_cred._username, USERNAME)
        # pylint: disable=protected-access
        self.assertEqual(self.abode_no_cred._password, PASSWORD)
    
    @requests_mock.mock()
    def test_login_failure(self, m):
        m.post(const.LOGIN_URL, text=mresp.LOGIN_FAIL_RESPONSE, status_code=400)
        
        """Check that we raise an Exception with a failed login request."""
        with self.assertRaises(abodepy.AbodeAuthenticationException):
            # pylint: disable=protected-access
            self.abode_no_cred.login(username=USERNAME, password=PASSWORD)
            
    @requests_mock.mock()
    def test_full_setup(self, m):
        """Check that Abode is set up properly."""
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE)
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.DEVICES_URL, text=mresp.EMPTY_DEVICE_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE)
        
        self.abode.get_devices()
        
        self.assertEqual(self.abode._username, USERNAME)
        self.assertEqual(self.abode._password, PASSWORD)
        self.assertEqual(self.abode._token, mresp.AUTH_TOKEN)
        self.assertEqual(self.abode._panel, json.loads(mresp.PANEL_RESPONSE))
        self.assertEqual(self.abode._user, json.loads(mresp.USER_RESPONSE))
        self.assertIsNotNone(self.abode._device_id_lookup['1'])

        self.abode.logout()
        
        self.assertIsNone(self.abode._token)
        self.assertIsNone(self.abode._panel)
        self.assertIsNone(self.abode._user)
        
    @requests_mock.mock()
    def test_abode_alarm_setup(self, m):
        """Check that Abode alarm device is set up properly."""
        test_alarm = json.loads(mresp.PANEL_RESPONSE)
        test_alarm['id'] = '1'
        test_alarm['type'] = 'Alarm'
        
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE)
        m.get(const.DEVICES_URL, text=mresp.EMPTY_DEVICE_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE)
        
        alarmDevice = self.abode.get_alarm()
        
        self.assertIsNotNone(alarmDevice)
        self.assertEqual(alarmDevice.json_state, test_alarm)
        
    @requests_mock.mock()
    def test_reauthorize(self, m):
        """Check that Abode can reauthorize after token timeout."""
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE_2)
        m.get(const.DEVICES_URL, [{'text': mresp.API_KEY_INVALID_RESPONSE, 'status_code':403},
                                 {'text': mresp.EMPTY_DEVICE_RESPONSE, 'status_code':200}])
        m.get(const.PANEL_URL, text=mresp.PANEL_RESPONSE)
        
        alarmDevice = self.abode.get_devices()
        
        self.assertEqual(self.abode._token, mresp.AUTH_TOKEN_2)
        
    @requests_mock.mock()
    def test_continuous_bad_auth(self, m):
        """Check that Abode won't get stuck with repeated failed retries."""
        m.post(const.LOGIN_URL, text=mresp.LOGIN_RESPONSE)
        m.get(const.DEVICES_URL, text=mresp.API_KEY_INVALID_RESPONSE, status_code=403)
        
        with self.assertRaises(abodepy.AbodeException):
            alarmDevice = self.abode.get_devices()
        