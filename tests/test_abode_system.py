"""
Test Abode system setup, shutdown, and general functionality.

Tests the system initialization and attributes of the main Abode system.
"""
import json
import unittest

import requests
import requests_mock

import abodepy
import helpers.constants as const
import tests.mock_devices as mdev
import tests.mock_responses as mresp


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
        m.post(const.LOGIN_URL, text=mresp.login_response())

        self.abode_no_cred.login(username=USERNAME, password=PASSWORD)

        # pylint: disable=protected-access
        self.assertEqual(self.abode_no_cred._username, USERNAME)
        # pylint: disable=protected-access
        self.assertEqual(self.abode_no_cred._password, PASSWORD)

    @requests_mock.mock()
    def test_auto_login(self, m):
        """Test that automatic login, device retrieval, and debug mode work."""
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.get(const.DEVICES_URL, text=mresp.EMPTY_DEVICE_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.panel_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)

        abode = abodepy.Abode(username='fizz',
                              password='buzz',
                              auto_login=True,
                              get_devices=True)

        # pylint: disable=W0212
        self.assertEqual(abode._username, 'fizz')
        self.assertEqual(abode._password, 'buzz')
        self.assertEqual(abode._token, mresp.AUTH_TOKEN)
        self.assertEqual(abode._panel, json.loads(mresp.panel_response()))
        self.assertEqual(abode._user, json.loads(mresp.USER_RESPONSE))
        self.assertIsNotNone(abode._device_id_lookup['1'])

        abode.logout()

        abode = None

    @requests_mock.mock()
    def test_login_failure(self, m):
        """Test login failed."""
        m.post(const.LOGIN_URL,
               text=mresp.LOGIN_FAIL_RESPONSE, status_code=400)

        # Check that we raise an Exception with a failed login request.
        with self.assertRaises(abodepy.AbodeAuthenticationException):
            self.abode_no_cred.login(username=USERNAME, password=PASSWORD)

    @requests_mock.mock()
    def test_logout_failure(self, m):
        """Test logout failed."""
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.get(const.DEVICES_URL, text=mresp.EMPTY_DEVICE_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.panel_response())
        m.post(const.LOGOUT_URL,
               text=mresp.LOGOUT_FAIL_RESPONSE, status_code=400)

        self.abode_no_cred.login(username=USERNAME, password=PASSWORD)

        # Check that we raise an Exception with a failed login request.
        with self.assertRaises(abodepy.AbodeAuthenticationException):
            self.abode_no_cred.logout()

    @requests_mock.mock()
    def test_full_setup(self, m):
        """Check that Abode is set up properly."""
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.DEVICES_URL, text=mresp.EMPTY_DEVICE_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.panel_response())

        self.abode.get_devices()

        # pylint: disable=W0212
        self.assertEqual(self.abode._username, USERNAME)
        self.assertEqual(self.abode._password, PASSWORD)
        self.assertEqual(self.abode._token, mresp.AUTH_TOKEN)
        self.assertEqual(self.abode._panel, json.loads(mresp.panel_response()))
        self.assertEqual(self.abode._user, json.loads(mresp.USER_RESPONSE))
        self.assertIsNotNone(self.abode._device_id_lookup['1'])

        self.abode.logout()

        # pylint: disable=W0212
        self.assertIsNone(self.abode._token)
        self.assertIsNone(self.abode._panel)
        self.assertIsNone(self.abode._user)
        self.assertListEqual(self.abode._devices, [])
        self.assertDictEqual(self.abode._device_id_lookup, {})

    @requests_mock.mock()
    def test_abode_alarm_setup(self, m):
        """Check that Abode alarm device is set up properly."""
        test_alarm = json.loads(mresp.panel_response())
        test_alarm['id'] = '1'
        test_alarm['type'] = 'Alarm'

        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.get(const.DEVICES_URL, text=mresp.EMPTY_DEVICE_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.panel_response())

        alarm_device = self.abode.get_alarm()

        self.assertIsNotNone(alarm_device)
        # pylint: disable=W0212
        self.assertEqual(alarm_device._json_state, test_alarm)

    @requests_mock.mock()
    def test_reauthorize(self, m):
        """Check that Abode can reauthorize after token timeout."""
        new_token = "FOOBAR"
        m.post(const.LOGIN_URL, [
            {'text': mresp.login_response(
                auth_token=new_token), 'status_code': 200}
        ])

        m.get(const.DEVICES_URL, [
            {'text': mresp.API_KEY_INVALID_RESPONSE, 'status_code': 403},
            {'text': mresp.EMPTY_DEVICE_RESPONSE, 'status_code': 200}
        ])
        m.get(const.PANEL_URL, text=mresp.panel_response())

        # Forces a device update
        self.abode.get_devices()

        # pylint: disable=W0212
        self.assertEqual(self.abode._token, new_token)

    @requests_mock.mock()
    def test_send_request_exception(self, m):
        """Check that send_request recovers from an exception."""
        new_token = "DEADBEEF"
        m.post(const.LOGIN_URL, [
            {'text': mresp.login_response(
                auth_token=new_token), 'status_code': 200}
        ])

        m.get(const.DEVICES_URL, [
            {'exc': requests.exceptions.ConnectTimeout},
            {'text': mresp.EMPTY_DEVICE_RESPONSE, 'status_code': 200}
        ])
        m.get(const.PANEL_URL, text=mresp.panel_response())

        # Forces a device update
        self.abode.get_devices()

        # pylint: disable=W0212
        self.assertEqual(self.abode._token, new_token)

    @requests_mock.mock()
    def test_continuous_bad_auth(self, m):
        """Check that Abode won't get stuck with repeated failed retries."""
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.get(const.DEVICES_URL,
              text=mresp.API_KEY_INVALID_RESPONSE, status_code=403)

        with self.assertRaises(abodepy.AbodeException):
            self.abode.get_devices()

    def test_default_mode(self):
        """Test that the default mode fails if not of type home or away."""
        self.abode.set_default_mode(const.MODE_HOME)
        self.assertEqual(self.abode.default_mode, const.MODE_HOME)

        self.abode.set_default_mode(const.MODE_AWAY)
        self.assertEqual(self.abode.default_mode, const.MODE_AWAY)

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_default_mode('foobar')

    @requests_mock.mock()
    def test_device_event_registration(self, m):
        """Check that device registration is working."""
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.DEVICES_URL, text=mdev.door_contact_device())
        m.get(const.PANEL_URL, text=mresp.panel_response())

        # Reset
        self.abode.logout()

        # Get devices
        device = self.abode.get_device(mdev.DOOR_CONTACT_DEVICE_ID)

        self.assertIsNotNone(device)

        # Register device
        self.assertTrue(self.abode.register(device, None))

        # Test that you can register a device by devid
        self.assertTrue(self.abode.register(mdev.DOOR_CONTACT_DEVICE_ID, None))

        # Test that an invalid device raises exception
        with self.assertRaises(abodepy.AbodeException):
            self.abode.register('slapstick', None)
