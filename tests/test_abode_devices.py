"""Test the Abode device classes."""
import json
import unittest

import requests_mock

import abodepy
import helpers.constants as const
import tests.mock_devices as mdev
import tests.mock_responses as mresp


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
        """Check the generic Abode device class init's properly."""
        # Set up URLs
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.panel_response())

        # Set up device
        device_text = '[' + mdev.glass_break_device(
            status=const.STATUS_ONLINE,
            low_battery=True, no_response=True,
            tampered=True, out_of_order=True) + ']'
        device_json = json.loads(device_text)

        m.get(const.DEVICES_URL, text=device_text)

        # Logout to reset everything
        self.abode.logout()

        # Get our specific device
        device = self.abode.get_device(mdev.GLASS_BREAK_DEVICE_ID)

        # Check device states match
        self.assertIsNotNone(device)
        # pylint: disable=W0212
        self.assertEqual(device._json_state, device_json[0])
        self.assertEqual(device.name, device_json[0]['name'])
        self.assertEqual(device.type, device_json[0]['type'])
        self.assertEqual(device.device_id, device_json[0]['id'])
        self.assertEqual(device.status, const.STATUS_ONLINE)
        self.assertTrue(device.battery_low)
        self.assertTrue(device.no_response)
        self.assertTrue(device.tampered)
        self.assertTrue(device.out_of_order)

    @requests_mock.mock()
    def test_generic_device_refresh(self, m):
        """Check the generic Abode device class init's properly."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.panel_response())

        # Set up online device
        device_text_online = '[' + \
            mdev.glass_break_device(status=const.STATUS_ONLINE) + ']'
        m.get(const.DEVICES_URL, text=device_text_online)

        # Set up offline device
        device_text_offline = '[' + \
            mdev.glass_break_device(status=const.STATUS_OFFLINE) + ']'
        device_url = str.replace(const.DEVICE_URL,
                                 '$DEVID$', mdev.GLASS_BREAK_DEVICE_ID)
        m.get(device_url, text=device_text_offline)

        # Logout to reset everything
        self.abode.logout()

        # Get the first device and test
        device = self.abode.get_device(mdev.GLASS_BREAK_DEVICE_ID)
        self.assertEqual(device.status, const.STATUS_ONLINE)

        # Refresh the device and test
        device = self.abode.get_device(
            mdev.GLASS_BREAK_DEVICE_ID, refresh=True)
        self.assertEqual(device.status, const.STATUS_OFFLINE)

    @requests_mock.mock()
    def test_multiple_devices(self, m):
        """Tests that multiple devices are returned properly."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL,
              text=mresp.panel_response(mode=const.MODE_STANDBY))

        # Set up a list of devices
        dev_list = '[' + \
            mdev.power_switch_device() + "," + \
            mdev.door_contact_device() + "," + \
            mdev.glass_break_device() + ']'

        m.get(const.DEVICES_URL, text=dev_list)

        # Logout to reset everything
        self.abode.logout()

        # Get our devices
        devices = self.abode.get_devices()

        # Assert four devices - three from above + 1 alarm
        self.assertIsNotNone(devices)
        self.assertEqual(len(devices), 4)

        # Get each individual device by device ID
        psd = self.abode.get_device(mdev.POWER_SWITCH_DEVICE_ID)
        self.assertIsNotNone(psd)

        # Get each individual device by device ID
        psd = self.abode.get_device(mdev.DOOR_CONTACT_DEVICE_ID)
        self.assertIsNotNone(psd)

        # Get each individual device by device ID
        psd = self.abode.get_device(mdev.GLASS_BREAK_DEVICE_ID)
        self.assertIsNotNone(psd)

    @requests_mock.mock()
    def test_device_category_filter(self, m):
        """Tests that device category filter returns requested results."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL,
              text=mresp.panel_response(mode=const.MODE_STANDBY))

        # Set up a list of devices
        dev_list = '[' + \
            mdev.power_switch_device(devid='ps1',
                                     status=const.STATUS_OFF,
                                     low_battery=False,
                                     no_response=False) + "," + \
            mdev.power_switch_device(devid='ps2',
                                     status=const.STATUS_OFF,
                                     low_battery=False,
                                     no_response=False) + "," + \
            mdev.glass_break_device(devid='gb1',
                                    status=const.STATUS_OFF,
                                    low_battery=False,
                                    no_response=False) + ']'

        m.get(const.DEVICES_URL, text=dev_list)

        # Logout to reset everything
        self.abode.logout()

        # Get our glass devices
        devices = self.abode.get_devices(('GLASS'))

        self.assertIsNotNone(devices)
        self.assertEqual(len(devices), 1)

        # Get our power switch devices
        devices = self.abode.get_devices(('Power Switch Sensor'))

        self.assertIsNotNone(devices)
        self.assertEqual(len(devices), 2)

    @requests_mock.mock()
    def test_no_control_url(self, m):
        """Check that devices return false without control url's."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.panel_response())

        m.get(const.DEVICES_URL,
              text=mdev.glass_break_device(status=const.STATUS_ONLINE))

        # Logout to reset everything
        self.abode.logout()

        # Get device
        device = self.abode.get_device(mdev.GLASS_BREAK_DEVICE_ID)

        self.assertIsNotNone(device)
        self.assertFalse(device.set_status('1'))
        self.assertFalse(device.set_level('99'))

    @requests_mock.mock()
    def test_alarm_device_properties(self, m):
        """Check that the abode device properties are working."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL, text=mresp.panel_response(
            mode=const.MODE_STANDBY, battery=True, is_cellular=True))
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
        m.get(const.PANEL_URL, text=mresp.panel_response(
            mode=const.MODE_AWAY, battery=False, is_cellular=False))

        # Refresh alarm and test
        alarm.refresh()

        self.assertEqual(alarm.mode, const.MODE_AWAY)
        self.assertEqual(alarm.status, const.MODE_AWAY)
        self.assertFalse(alarm.battery)
        self.assertFalse(alarm.is_cellular)
        self.assertTrue(alarm.is_on)

        # Change alarm state to final on state and test
        m.get(const.PANEL_URL, text=mresp.panel_response(mode=const.MODE_HOME))

        # Refresh alarm and test
        alarm.refresh()
        self.assertEqual(alarm.mode, const.MODE_HOME)
        self.assertEqual(alarm.status, const.MODE_HOME)
        self.assertTrue(alarm.is_on)

    @requests_mock.mock()
    def test_alarm_device_mode_changes(self, m):
        """Test that the abode alarm can change/report modes."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL,
              text=mresp.panel_response(mode=const.MODE_STANDBY))
        m.get(const.DEVICES_URL, text=mresp.EMPTY_DEVICE_RESPONSE)

        # Logout to reset everything
        self.abode.logout()

        # Assert that after login we have our alarm device with standby mode
        alarm = self.abode.get_alarm()

        self.assertIsNotNone(alarm)
        self.assertEqual(alarm.status, const.MODE_STANDBY)

        # Set mode URLs
        m.put(const.PANEL_MODE_URL('1', const.MODE_STANDBY),
              text=mresp.panel_mode_response(area='1',
                                             mode=const.MODE_STANDBY))
        m.put(const.PANEL_MODE_URL('1', const.MODE_AWAY),
              text=mresp.panel_mode_response(area='1', mode=const.MODE_AWAY))
        m.put(const.PANEL_MODE_URL('1', const.MODE_HOME),
              text=mresp.panel_mode_response(area='1', mode=const.MODE_HOME))

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

        # Set and test default mode changes
        self.assertTrue(alarm.switch_off())
        self.assertEqual(alarm.mode, const.MODE_STANDBY)

        self.abode.set_default_mode(const.MODE_HOME)
        self.assertTrue(alarm.switch_on())
        self.assertEqual(alarm.mode, const.MODE_HOME)

        self.assertTrue(alarm.switch_off())
        self.assertEqual(alarm.mode, const.MODE_STANDBY)

        self.abode.set_default_mode(const.MODE_AWAY)
        self.assertTrue(alarm.switch_on())
        self.assertEqual(alarm.mode, const.MODE_AWAY)

        # Test that no mode throws exception
        with self.assertRaises(abodepy.AbodeException):
            alarm.set_mode(mode=None)

        # Test that an invalid mode throws exception
        with self.assertRaises(abodepy.AbodeException):
            alarm.set_mode('chestnuts')

        # Test that an invalid mode change response throws exception
        m.put(const.PANEL_MODE_URL('1', const.MODE_HOME),
              text=mresp.panel_mode_response(area='1', mode=const.MODE_AWAY))

        with self.assertRaises(abodepy.AbodeException):
            alarm.set_mode(const.MODE_HOME)

        # Test that an invalid area in mode change response throws exception
        m.put(const.PANEL_MODE_URL('1', const.MODE_HOME),
              text=mresp.panel_mode_response(area='2', mode=const.MODE_HOME))

        with self.assertRaises(abodepy.AbodeException):
            alarm.set_mode(const.MODE_HOME)

    @requests_mock.mock()
    def test_switch_device_properties(self, m):
        """Tests that switch devices properties work as expected."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL,
              text=mresp.panel_response(mode=const.MODE_STANDBY))
        m.get(const.DEVICES_URL,
              text=mdev.power_switch_device(devid=mdev.POWER_SWITCH_DEVICE_ID,
                                            status=const.STATUS_OFF,
                                            low_battery=False,
                                            no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our power switch
        device = self.abode.get_device(mdev.POWER_SWITCH_DEVICE_ID)

        # Test our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, const.STATUS_OFF)
        self.assertFalse(device.battery_low)
        self.assertFalse(device.no_response)
        self.assertFalse(device.is_on)

        # Set up our direct device get url
        device_url = str.replace(const.DEVICE_URL,
                                 '$DEVID$', mdev.POWER_SWITCH_DEVICE_ID)

        # Change device properties
        m.get(device_url,
              text=mdev.power_switch_device(devid=mdev.POWER_SWITCH_DEVICE_ID,
                                            status=const.STATUS_ON,
                                            low_battery=True,
                                            no_response=True))

        # Refesh device and test changes
        device.refresh()

        self.assertEqual(device.status, const.STATUS_ON)
        self.assertTrue(device.battery_low)
        self.assertTrue(device.no_response)
        self.assertTrue(device.is_on)

    @requests_mock.mock()
    def test_switch_device_mode_changes(self, m):
        """Tests that switch device changes work as expected."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL,
              text=mresp.panel_response(mode=const.MODE_STANDBY))
        m.get(const.DEVICES_URL,
              text=mdev.power_switch_device(devid=mdev.POWER_SWITCH_DEVICE_ID,
                                            status=const.STATUS_OFF,
                                            low_battery=False,
                                            no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our power switch
        device = self.abode.get_device(mdev.POWER_SWITCH_DEVICE_ID)

        # Test that we have our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, const.STATUS_OFF)
        self.assertFalse(device.is_on)

        # Set up control url response
        control_url = const.BASE_URL + mdev.POWER_SWITCH_CONTROL_URL
        m.put(control_url,
              text=mresp.
              control_url_status_response(devid=mdev.POWER_SWITCH_DEVICE_ID,
                                          status=const.STATUS_ON_INT))

        # Change the mode to "on"
        self.assertTrue(device.switch_on())
        self.assertEqual(device.status, const.STATUS_ON)
        self.assertTrue(device.is_on)

        # Change response
        m.put(control_url,
              text=mresp.
              control_url_status_response(devid=mdev.POWER_SWITCH_DEVICE_ID,
                                          status=const.STATUS_OFF_INT))

        # Change the mode to "off"
        self.assertTrue(device.switch_off())
        self.assertEqual(device.status, const.STATUS_OFF)
        self.assertFalse(device.is_on)

        # Test that an invalid status response throws exception
        m.put(control_url,
              text=mresp.
              control_url_status_response(devid=mdev.POWER_SWITCH_DEVICE_ID,
                                          status=const.STATUS_OFF_INT))

        with self.assertRaises(abodepy.AbodeException):
            device.switch_on()

    @requests_mock.mock()
    def test_lock_device_properties(self, m):
        """Tests that lock devices properties work as expected."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL,
              text=mresp.panel_response(mode=const.MODE_STANDBY))
        m.get(const.DEVICES_URL,
              text=mdev.lock_device(devid=mdev.LOCK_DEVICE_ID,
                                    status=const.STATUS_LOCKCLOSED,
                                    low_battery=False,
                                    no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our lock
        device = self.abode.get_device(mdev.LOCK_DEVICE_ID)

        # Test our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, const.STATUS_LOCKCLOSED)
        self.assertFalse(device.battery_low)
        self.assertFalse(device.no_response)
        self.assertTrue(device.is_locked)

        # Set up our direct device get url
        device_url = str.replace(const.DEVICE_URL,
                                 '$DEVID$', mdev.LOCK_DEVICE_ID)

        # Change device properties
        m.get(device_url,
              text=mdev.power_switch_device(devid=mdev.LOCK_DEVICE_ID,
                                            status=const.STATUS_LOCKOPEN,
                                            low_battery=True,
                                            no_response=True))

        # Refesh device and test changes
        device.refresh()

        self.assertEqual(device.status, const.STATUS_LOCKOPEN)
        self.assertTrue(device.battery_low)
        self.assertTrue(device.no_response)
        self.assertFalse(device.is_locked)

    @requests_mock.mock()
    def test_lock_device_mode_changes(self, m):
        """Tests that lock device changes work as expected."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL,
              text=mresp.panel_response(mode=const.MODE_STANDBY))
        m.get(const.DEVICES_URL,
              text=mdev.lock_device(devid=mdev.LOCK_DEVICE_ID,
                                    status=const.STATUS_LOCKCLOSED,
                                    low_battery=False,
                                    no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our power switch
        device = self.abode.get_device(mdev.LOCK_DEVICE_ID)

        # Test that we have our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, const.STATUS_LOCKCLOSED)
        self.assertTrue(device.is_locked)

        # Set up control url response
        control_url = const.BASE_URL + mdev.LOCK_DEVICE_CONTROL_URL
        m.put(control_url,
              text=mresp.
              control_url_status_response(devid=mdev.LOCK_DEVICE_ID,
                                          status=const.STATUS_LOCKOPEN_INT))

        # Change the mode to "on"
        self.assertTrue(device.unlock())
        self.assertEqual(device.status, const.STATUS_LOCKOPEN)
        self.assertFalse(device.is_locked)

        # Change response
        m.put(control_url,
              text=mresp.
              control_url_status_response(devid=mdev.LOCK_DEVICE_ID,
                                          status=const.STATUS_LOCKCLOSED_INT))

        # Change the mode to "off"
        self.assertTrue(device.lock())
        self.assertEqual(device.status, const.STATUS_LOCKCLOSED)
        self.assertTrue(device.is_locked)

        # Test that an invalid status response throws exception
        m.put(control_url,
              text=mresp.
              control_url_status_response(devid=mdev.LOCK_DEVICE_ID,
                                          status=const.STATUS_LOCKCLOSED_INT))

        with self.assertRaises(abodepy.AbodeException):
            device.unlock()

    @requests_mock.mock()
    def test_contact_device_properties(self, m):
        """Tests that door contact device properties work as expected."""
        # Set up URL's
        m.post(const.LOGIN_URL, text=mresp.login_response())
        m.post(const.LOGOUT_URL, text=mresp.LOGOUT_RESPONSE)
        m.get(const.PANEL_URL,
              text=mresp.panel_response(mode=const.MODE_STANDBY))
        m.get(const.DEVICES_URL,
              text=mdev.door_contact_device(devid=mdev.DOOR_CONTACT_DEVICE_ID,
                                            status=const.STATUS_CLOSED,
                                            low_battery=False,
                                            no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our lock
        device = self.abode.get_device(mdev.DOOR_CONTACT_DEVICE_ID)

        # Test our device
        self.assertIsNotNone(device)
        self.assertEqual(device.status, const.STATUS_CLOSED)
        self.assertFalse(device.battery_low)
        self.assertFalse(device.no_response)
        self.assertTrue(device.is_on)

        # Set up our direct device get url
        device_url = str.replace(const.DEVICE_URL,
                                 '$DEVID$', mdev.DOOR_CONTACT_DEVICE_ID)

        # Change device properties
        m.get(device_url,
              text=mdev.door_contact_device(devid=mdev.DOOR_CONTACT_DEVICE_ID,
                                            status=const.STATUS_OPEN,
                                            low_battery=True,
                                            no_response=True))

        # Refesh device and test changes
        device.refresh()

        self.assertEqual(device.status, const.STATUS_OPEN)
        self.assertTrue(device.battery_low)
        self.assertTrue(device.no_response)
        self.assertFalse(device.is_on)
