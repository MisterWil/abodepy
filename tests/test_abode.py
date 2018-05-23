"""
Test Abode system setup, shutdown, and general functionality.

Tests the system initialization and attributes of the main Abode system.
"""
import json
import unittest

import requests
import requests_mock

import abodepy
import abodepy.helpers.constants as CONST

import tests.mock as MOCK
import tests.mock.login as LOGIN
import tests.mock.logout as LOGOUT
import tests.mock.panel as PANEL
import tests.mock.devices as DEVICES
import tests.mock.devices.door_contact as DOOR_CONTACT
import tests.mock.user as USER

USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestAbode(unittest.TestCase):
    """Test the Abode class in abodepy."""

    def setUp(self):
        """Set up Abode module."""
        self.abode_no_cred = abodepy.Abode(disable_cache=True)
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD,
                                   disable_cache=True)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None
        self.abode_no_cred = None

    def tests_initialization(self):
        """Verify we can initialize abode."""
        # pylint: disable=protected-access
        self.assertEqual(self.abode._cache[CONST.ID], USERNAME)
        # pylint: disable=protected-access
        self.assertEqual(self.abode._cache[CONST.PASSWORD], PASSWORD)

    def tests_no_credentials(self):
        """Check that we throw an exception when no username/password."""
        with self.assertRaises(abodepy.AbodeAuthenticationException):
            self.abode_no_cred.login()

        # pylint: disable=protected-access
        self.abode_no_cred._cache[CONST.ID] = USERNAME
        with self.assertRaises(abodepy.AbodeAuthenticationException):
            self.abode_no_cred.login()

    @requests_mock.mock()
    def tests_manual_login(self, m):
        """Check that we can manually use the login() function."""
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())

        self.abode_no_cred.login(username=USERNAME, password=PASSWORD)

        # pylint: disable=protected-access
        self.assertEqual(self.abode_no_cred._cache[CONST.ID], USERNAME)
        # pylint: disable=protected-access
        self.assertEqual(self.abode_no_cred._cache[CONST.PASSWORD], PASSWORD)

    @requests_mock.mock()
    def tests_auto_login(self, m):
        """Test that automatic login works."""
        auth_token = MOCK.AUTH_TOKEN
        user_json = USER.get_response_ok()
        login_json = LOGIN.post_response_ok(auth_token, user_json)
        panel_json = PANEL.get_response_ok()

        m.post(CONST.LOGIN_URL, text=login_json)
        m.get(CONST.PANEL_URL, text=panel_json)
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())

        abode = abodepy.Abode(username='fizz',
                              password='buzz',
                              auto_login=True,
                              get_devices=False,
                              disable_cache=True)

        # pylint: disable=W0212
        self.assertEqual(abode._cache[CONST.ID], 'fizz')
        self.assertEqual(abode._cache[CONST.PASSWORD], 'buzz')
        self.assertEqual(abode._token, MOCK.AUTH_TOKEN)
        self.assertEqual(abode._panel, json.loads(panel_json))
        self.assertEqual(abode._user, json.loads(user_json))
        self.assertIsNone(abode._devices)
        self.assertIsNone(abode._automations)

        abode.logout()

        abode = None

    @requests_mock.mock()
    def tests_auto_fetch(self, m):
        """Test that automatic device and automation retrieval works."""
        auth_token = MOCK.AUTH_TOKEN
        user_json = USER.get_response_ok()
        login_json = LOGIN.post_response_ok(auth_token, user_json)
        panel_json = PANEL.get_response_ok()

        m.post(CONST.LOGIN_URL, text=login_json)
        m.get(CONST.PANEL_URL, text=panel_json)
        m.get(CONST.DEVICES_URL, text=DEVICES.EMPTY_DEVICE_RESPONSE)
        m.get(CONST.AUTOMATION_URL, text=DEVICES.EMPTY_DEVICE_RESPONSE)
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())

        abode = abodepy.Abode(username='fizz',
                              password='buzz',
                              auto_login=False,
                              get_devices=True,
                              get_automations=True,
                              disable_cache=True)

        # pylint: disable=W0212
        self.assertEqual(abode._cache[CONST.ID], 'fizz')
        self.assertEqual(abode._cache[CONST.PASSWORD], 'buzz')
        self.assertEqual(abode._token, MOCK.AUTH_TOKEN)
        self.assertEqual(abode._panel, json.loads(panel_json))
        self.assertEqual(abode._user, json.loads(user_json))

        # Contains one device, our alarm
        self.assertEqual(abode._devices, {'area_1': abode.get_alarm()})

        # Contains no automations
        self.assertEqual(abode._automations, {})

        abode.logout()

        abode = None

    @requests_mock.mock()
    def tests_login_failure(self, m):
        """Test login failed."""
        m.post(CONST.LOGIN_URL,
               text=LOGIN.post_response_bad_request(), status_code=400)

        # Check that we raise an Exception with a failed login request.
        with self.assertRaises(abodepy.AbodeAuthenticationException):
            self.abode_no_cred.login(username=USERNAME, password=PASSWORD)

    @requests_mock.mock()
    def tests_logout_failure(self, m):
        """Test logout failed."""
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.DEVICES_URL, text=DEVICES.EMPTY_DEVICE_RESPONSE)
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())
        m.post(CONST.LOGOUT_URL,
               text=LOGOUT.post_response_bad_request(), status_code=400)

        self.abode_no_cred.login(username=USERNAME, password=PASSWORD)

        # Check that we raise an Exception with a failed logout request.
        with self.assertRaises(abodepy.AbodeAuthenticationException):
            self.abode_no_cred.logout()

    @requests_mock.mock()
    def tests_logout_exception(self, m):
        """Test logout exception."""
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.DEVICES_URL, text=DEVICES.EMPTY_DEVICE_RESPONSE)
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())
        m.post(CONST.LOGOUT_URL, exc=requests.exceptions.ConnectTimeout)

        self.abode.login()

        # Check that we eat the exception gracefully
        self.assertFalse(self.abode.logout())

    @requests_mock.mock()
    def tests_full_setup(self, m):
        """Check that Abode is set up properly."""
        auth_token = MOCK.AUTH_TOKEN
        user_json = USER.get_response_ok()
        login_json = LOGIN.post_response_ok(auth_token, user_json)
        panel_json = PANEL.get_response_ok()

        m.post(CONST.LOGIN_URL, text=login_json)
        m.get(CONST.PANEL_URL, text=panel_json)
        m.get(CONST.DEVICES_URL, text=DEVICES.EMPTY_DEVICE_RESPONSE)
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())

        self.abode.get_devices()

        # pylint: disable=protected-access
        original_session = self.abode._session

        # pylint: disable=W0212
        self.assertEqual(self.abode._cache[CONST.ID], USERNAME)
        self.assertEqual(self.abode._cache[CONST.PASSWORD], PASSWORD)
        self.assertEqual(self.abode._token, auth_token)
        self.assertEqual(self.abode._panel, json.loads(panel_json))
        self.assertEqual(self.abode._user, json.loads(user_json))
        self.assertIsNotNone(self.abode.get_alarm())
        self.assertIsNotNone(self.abode._get_session())
        self.assertEqual(self.abode._get_session(), original_session)
        self.assertIsNotNone(self.abode.events)

        self.abode.logout()

        # pylint: disable=W0212
        self.assertIsNone(self.abode._token)
        self.assertIsNone(self.abode._panel)
        self.assertIsNone(self.abode._user)
        self.assertIsNone(self.abode._devices)
        self.assertIsNone(self.abode._automations)
        self.assertIsNotNone(self.abode._session)
        self.assertNotEqual(self.abode._get_session(), original_session)

    @requests_mock.mock()
    def tests_reauthorize(self, m):
        """Check that Abode can reauthorize after token timeout."""
        new_token = "FOOBAR"
        m.post(CONST.LOGIN_URL, [
            {'text': LOGIN.post_response_ok(
                auth_token=new_token), 'status_code': 200}
        ])

        m.get(CONST.DEVICES_URL, [
            {'text': MOCK.response_forbidden(), 'status_code': 403},
            {'text': DEVICES.EMPTY_DEVICE_RESPONSE, 'status_code': 200}
        ])
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        # Forces a device update
        self.abode.get_devices()

        # pylint: disable=W0212
        self.assertEqual(self.abode._token, new_token)

    @requests_mock.mock()
    def tests_send_request_exception(self, m):
        """Check that send_request recovers from an exception."""
        new_token = "DEADBEEF"
        m.post(CONST.LOGIN_URL, [
            {'text': LOGIN.post_response_ok(
                auth_token=new_token), 'status_code': 200}
        ])

        m.get(CONST.DEVICES_URL, [
            {'exc': requests.exceptions.ConnectTimeout},
            {'text': DEVICES.EMPTY_DEVICE_RESPONSE, 'status_code': 200}
        ])
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        # Forces a device update
        self.abode.get_devices()

        # pylint: disable=W0212
        self.assertEqual(self.abode._token, new_token)

    @requests_mock.mock()
    def tests_continuous_bad_auth(self, m):
        """Check that Abode won't get stuck with repeated failed retries."""
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.DEVICES_URL,
              text=MOCK.response_forbidden(), status_code=403)

        with self.assertRaises(abodepy.AbodeException):
            self.abode.get_devices()

    def tests_default_mode(self):
        """Test that the default mode fails if not of type home or away."""
        self.abode.set_default_mode(CONST.MODE_HOME)
        self.assertEqual(self.abode.default_mode, CONST.MODE_HOME)

        self.abode.set_default_mode(CONST.MODE_AWAY)
        self.assertEqual(self.abode.default_mode, CONST.MODE_AWAY)

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_default_mode('foobar')

    @requests_mock.mock()
    def test_all_device_refresh(self, m):
        """Check that device refresh works and reuses the same objects."""
        dc1_devid = 'RF:01'
        dc1a = DOOR_CONTACT.device(
            devid=dc1_devid, status=CONST.STATUS_ON)

        dc2_devid = 'RF:02'
        dc2a = DOOR_CONTACT.device(
            devid=dc2_devid, status=CONST.STATUS_OFF)

        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.DEVICES_URL, text='[' + dc1a + ',' + dc2a + ']')
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        # Reset
        self.abode.logout()

        # Get all devices
        self.abode.get_devices()

        # Get and check devices
        # pylint: disable=W0212
        dc1a_dev = self.abode.get_device(dc1_devid)
        self.assertEqual(json.loads(dc1a)['id'], dc1a_dev.device_id)

        dc2a_dev = self.abode.get_device(dc2_devid)
        self.assertEqual(json.loads(dc2a)['id'], dc2a_dev.device_id)

        # Change device states
        dc1b = DOOR_CONTACT.device(
            devid=dc1_devid, status=CONST.STATUS_OFF)

        dc2b = DOOR_CONTACT.device(
            devid=dc2_devid, status=CONST.STATUS_ON)

        m.get(CONST.DEVICES_URL, text='[' + dc1b + ',' + dc2b + ']')

        # Refresh all devices
        self.abode.get_devices(refresh=True)

        # Get and check devices again, ensuring they are the same object
        # Future note: "if a is b" tests that the object is the same
        # Thus asserting dc1a_dev is dc1b_dev tests if they are the same object
        dc1b_dev = self.abode.get_device(dc1_devid)
        self.assertEqual(json.loads(dc1b)['id'], dc1b_dev.device_id)
        self.assertIs(dc1a_dev, dc1b_dev)

        dc2b_dev = self.abode.get_device(dc2_devid)
        self.assertEqual(json.loads(dc2b)['id'], dc2b_dev.device_id)
        self.assertIs(dc2a_dev, dc2b_dev)

    @requests_mock.mock()
    def tests_settings_validation(self, m):
        """Check that device panel general settings are working."""
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())
        m.get(CONST.SETTINGS_URL, text=MOCK.generic_response_ok())

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting("fliptrix", "foobar")

    @requests_mock.mock()
    def tests_general_settings(self, m):
        """Check that device panel general settings are working."""
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())
        m.put(CONST.SETTINGS_URL, text=MOCK.generic_response_ok())

        try:
            self.abode.set_setting(CONST.SETTING_CAMERA_RESOLUTION,
                                   CONST.SETTING_CAMERA_RES_640_480)

            self.abode.set_setting(CONST.SETTING_CAMERA_GRAYSCALE,
                                   CONST.SETTING_ENABLE)

            self.abode.set_setting(CONST.SETTING_SILENCE_SOUNDS,
                                   CONST.SETTING_ENABLE)
        except abodepy.AbodeException:
            self.fail("set_setting() raised AbodeException unexpectedly")

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting(CONST.SETTING_CAMERA_RESOLUTION,
                                   "foobar")

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting(CONST.SETTING_CAMERA_GRAYSCALE,
                                   "foobar")

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting(CONST.SETTING_SILENCE_SOUNDS,
                                   "foobar")

    @requests_mock.mock()
    def tests_area_settings(self, m):
        """Check that device panel areas settings are working."""
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())
        m.put(CONST.AREAS_URL, text=MOCK.generic_response_ok())

        try:
            self.abode.set_setting(CONST.SETTING_ENTRY_DELAY_AWAY,
                                   CONST.SETTING_ENTRY_EXIT_DELAY_10SEC)

            self.abode.set_setting(CONST.SETTING_EXIT_DELAY_AWAY,
                                   CONST.SETTING_ENTRY_EXIT_DELAY_30SEC)

        except abodepy.AbodeException:
            self.fail("set_setting() raised AbodeException unexpectedly")

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting(CONST.SETTING_ENTRY_DELAY_AWAY,
                                   "foobar")

        # 10 seconds is invalid here
        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting(CONST.SETTING_EXIT_DELAY_AWAY,
                                   CONST.SETTING_ENTRY_EXIT_DELAY_10SEC)

    @requests_mock.mock()
    def tests_sound_settings(self, m):
        """Check that device panel sound settings are working."""
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())
        m.put(CONST.SOUNDS_URL, text=MOCK.generic_response_ok())

        try:
            self.abode.set_setting(CONST.SETTING_DOOR_CHIME,
                                   CONST.SETTING_SOUND_LOW)

            self.abode.set_setting(CONST.SETTING_ALARM_LENGTH,
                                   CONST.SETTING_ALARM_LENGTH_2MIN)

            self.abode.set_setting(CONST.SETTING_FINAL_BEEPS,
                                   CONST.SETTING_FINAL_BEEPS_3SEC)

        except abodepy.AbodeException:
            self.fail("set_setting() raised AbodeException unexpectedly")

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting(CONST.SETTING_DOOR_CHIME,
                                   "foobar")

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting(CONST.SETTING_ALARM_LENGTH,
                                   "foobar")

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting(CONST.SETTING_FINAL_BEEPS,
                                   "foobar")

    @requests_mock.mock()
    def tests_siren_settings(self, m):
        """Check that device panel siren settings are working."""
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())
        m.put(CONST.SIREN_URL, text=MOCK.generic_response_ok())

        try:
            self.abode.set_setting(CONST.SETTING_SIREN_ENTRY_EXIT_SOUNDS,
                                   CONST.SETTING_ENABLE)

            self.abode.set_setting(CONST.SETTING_SIREN_CONFIRM_SOUNDS,
                                   CONST.SETTING_ENABLE)

            self.abode.set_setting(CONST.SETTING_SIREN_TAMPER_SOUNDS,
                                   CONST.SETTING_ENABLE)

        except abodepy.AbodeException:
            self.fail("set_setting() raised AbodeException unexpectedly")

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting(CONST.SETTING_SIREN_ENTRY_EXIT_SOUNDS,
                                   "foobar")

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting(CONST.SETTING_SIREN_CONFIRM_SOUNDS,
                                   "foobar")

        with self.assertRaises(abodepy.AbodeException):
            self.abode.set_setting(CONST.SETTING_SIREN_TAMPER_SOUNDS,
                                   "foobar")
