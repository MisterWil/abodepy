"""Test the Abode event controller class."""
import json
import unittest
from unittest.mock import call, Mock

import requests_mock

import abodepy
import abodepy.helpers.constants as CONST
import abodepy.helpers.timeline as TIMELINE
from abodepy.devices.binary_sensor import AbodeBinarySensor

import tests.mock.login as LOGIN
import tests.mock.logout as LOGOUT
import tests.mock.panel as PANEL
import tests.mock.devices.secure_barrier as COVER
import tests.mock.devices.door_contact as DOORCONTACT
import tests.mock.devices.ir_camera as IRCAMERA


USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestEventController(unittest.TestCase):
    """Test the AbodePy event controller."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    @requests_mock.mock()
    def tests_device_id_registration(self, m):
        """Tests that we can register for device events with a device id."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=COVER.device(devid=COVER.DEVICE_ID,
                                status=CONST.STATUS_CLOSED,
                                low_battery=False,
                                no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our device
        device = self.abode.get_device(COVER.DEVICE_ID)
        self.assertIsNotNone(device)

        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        # Create mock callback
        callback = Mock()

        # Register our device id
        self.assertTrue(
            events.add_device_callback(device.device_id, callback))

    @requests_mock.mock()
    def tests_device_registration(self, m):
        """Tests that we can register for device events with a device."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=COVER.device(devid=COVER.DEVICE_ID,
                                status=CONST.STATUS_CLOSED,
                                low_battery=False,
                                no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our device
        device = self.abode.get_device(COVER.DEVICE_ID)
        self.assertIsNotNone(device)

        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        def _our_callback(device):
            self.assertIsNotNone(device)

        # Register our device
        self.assertTrue(events.add_device_callback(device, _our_callback))

    @requests_mock.mock()
    def tests_invalid_device(self, m):
        """Tests that invalid devices are not registered."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=COVER.device(devid=COVER.DEVICE_ID,
                                status=CONST.STATUS_CLOSED,
                                low_battery=False,
                                no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our device
        device = self.abode.get_device(COVER.DEVICE_ID)
        self.assertIsNotNone(device)

        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        # Create mock callback
        callback = Mock()

        # Test that no device returns false
        self.assertFalse(events.add_device_callback(None, callback))

        # Create a fake device and attempt to register that
        fake_device = AbodeBinarySensor(
            json.loads(DOORCONTACT.device()), self.abode)

        with self.assertRaises(abodepy.AbodeException):
            events.add_device_callback(fake_device, callback)

    def tests_event_registration(self):
        """Tests that events register correctly."""
        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        # Create mock callback
        callback = Mock()

        # Test that a valid event registers
        self.assertTrue(
            events.add_event_callback(TIMELINE.ALARM_GROUP, callback))

        # Test that no event group returns false
        self.assertFalse(events.add_event_callback(None, callback))

        # Test that an invalid event throws exception
        with self.assertRaises(abodepy.AbodeException):
            events.add_event_callback("lol", callback)

    def tests_timeline_registration(self):
        """Tests that timeline events register correctly."""
        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        # Create mock callback
        callback = Mock()

        # Test that a valid timeline event registers
        self.assertTrue(
            events.add_timeline_callback(
                TIMELINE.CAPTURE_IMAGE, callback))

        # Test that no timeline event returns false
        self.assertFalse(events.add_timeline_callback(None, callback))

        # Test that an invalid timeline event string throws exception
        with self.assertRaises(abodepy.AbodeException):
            events.add_timeline_callback("lol", callback)

        # Test that an invalid timeline event dict throws exception
        with self.assertRaises(abodepy.AbodeException):
            events.add_timeline_callback({"lol": "lol"}, callback)

    @requests_mock.mock()
    def tests_device_callback(self, m):
        """Tests that device updates callback correctly."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=COVER.device(devid=COVER.DEVICE_ID,
                                status=CONST.STATUS_CLOSED,
                                low_battery=False,
                                no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our device
        device = self.abode.get_device(COVER.DEVICE_ID)
        self.assertIsNotNone(device)

        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        callback = Mock()

        # Register our device id
        self.assertTrue(
            events.add_device_callback(device.device_id, callback))

        # Set up device update URL
        device_url = str.replace(CONST.DEVICE_URL,
                                 '$DEVID$', COVER.DEVICE_ID)
        m.get(device_url, text=COVER.device(devid=COVER.DEVICE_ID,
                                            status=CONST.STATUS_OPEN,
                                            low_battery=False,
                                            no_response=False))

        # Call our device callback method
        # pylint: disable=protected-access
        events._on_device_update(device.device_id)
        callback.assert_called_with(device)

        # Test that our device updated
        self.assertEqual(device.status, CONST.STATUS_OPEN)

        # Test that no device ID cleanly returns
        events._on_device_update(None)

        # Test that an unknown device cleanly returns
        events._on_device_update(DOORCONTACT.DEVICE_ID)

    def tests_events_callback(self):
        """Tests that event updates callback correctly."""
        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        # Create mock callbacks
        capture_callback = Mock()
        alarm_callback = Mock()

        # Register our events
        self.assertTrue(
            events.add_event_callback(
                TIMELINE.CAPTURE_GROUP, capture_callback))

        self.assertTrue(
            events.add_event_callback(TIMELINE.ALARM_GROUP, alarm_callback))

        # Call our events callback method and trigger a capture group event
        # pylint: disable=protected-access
        event_json = json.loads(IRCAMERA.timeline_event())
        events._on_timeline_update(event_json)

        # Our capture callback should get one, but our alarm should not
        capture_callback.assert_called_with(event_json)
        alarm_callback.assert_not_called()

        # Test that an invalid event exits cleanly
        events._on_timeline_update({"invalid": "event"})

    def tests_timeline_callback(self):
        """Tests that timeline updates callback correctly."""
        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        # Create mock callbacks
        all_callback = Mock()
        image_callback = Mock()
        opened_callback = Mock()

        # Register our events
        self.assertTrue(
            events.add_timeline_callback(
                TIMELINE.ALL, all_callback))

        self.assertTrue(
            events.add_timeline_callback(
                TIMELINE.CAPTURE_IMAGE, image_callback))

        self.assertTrue(
            events.add_timeline_callback(
                TIMELINE.OPENED, opened_callback))

        # Call our events callback method and trigger an image capture event
        # pylint: disable=protected-access
        event_json = json.loads(IRCAMERA.timeline_event())
        events._on_timeline_update(event_json)

        # all and image callbacks should have one, opened none
        all_callback.assert_called_with(event_json)
        image_callback.assert_called_with(event_json)
        opened_callback.assert_not_called()

        # Test that an invalid event exits cleanly
        events._on_timeline_update({"invalid": "event"})

    @requests_mock.mock()
    def tests_alarm_callback(self, m):
        """Tests that alarm device updates callback correctly."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text=COVER.device(devid=COVER.DEVICE_ID,
                                status=CONST.STATUS_CLOSED,
                                low_battery=False,
                                no_response=False))

        # Logout to reset everything
        self.abode.logout()

        # Get our alarm device
        alarm = self.abode.get_alarm()
        self.assertIsNotNone(alarm)

        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        callback = Mock()

        # Register our alarm for callback
        self.assertTrue(
            events.add_device_callback(alarm.device_id, callback))

        # Call our mode changed callback method
        # pylint: disable=protected-access
        events._on_mode_change(CONST.MODE_HOME)
        callback.assert_called_with(alarm)

        # Test that our alarm state is set properly
        self.assertEqual(alarm.mode, CONST.MODE_HOME)

        # Test that no mode cleanly returns
        events._on_mode_change(None)

        # Test that an unknown mode cleanly returns
        events._on_mode_change("lol")

    def tests_execute_callback(self):
        """Tests that callbacks that throw exceptions don't bomb."""
        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        # Create callbacks
        def _callback(event_json):
            raise Exception("CHAOS!!!")

        # Register events callback
        self.assertTrue(
            events.add_timeline_callback(TIMELINE.CAPTURE_IMAGE, _callback))

        # Call our events callback method and trigger an image capture event
        # pylint: disable=protected-access
        event_json = json.loads(IRCAMERA.timeline_event())
        events._on_timeline_update(event_json)

    @requests_mock.mock()
    def tests_multi_device_callback(self, m):
        """Tests that multiple device updates callback correctly."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL,
              text='[' +
              COVER.device(devid=COVER.DEVICE_ID,
                           status=CONST.STATUS_CLOSED,
                           low_battery=False,
                           no_response=False) + ", " +
              DOORCONTACT.device(devid=DOORCONTACT.DEVICE_ID,
                                 status=CONST.STATUS_CLOSED) + ']')

        # Logout to reset everything
        self.abode.logout()

        # Get our devices
        cover = self.abode.get_device(COVER.DEVICE_ID)
        self.assertIsNotNone(cover)

        doorcontact = self.abode.get_device(DOORCONTACT.DEVICE_ID)
        self.assertIsNotNone(doorcontact)

        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        callback = Mock()

        # Register our devices
        self.assertTrue(
            events.add_device_callback([cover, doorcontact], callback))

        # Set up device update URL's
        cover_url = str.replace(CONST.DEVICE_URL,
                                '$DEVID$', COVER.DEVICE_ID)
        m.get(cover_url, text=COVER.device(devid=COVER.DEVICE_ID,
                                           status=CONST.STATUS_OPEN,
                                           low_battery=False,
                                           no_response=False))

        door_url = str.replace(CONST.DEVICE_URL,
                               '$DEVID$', DOORCONTACT.DEVICE_ID)
        m.get(door_url, text=DOORCONTACT.device(devid=COVER.DEVICE_ID,
                                                status=CONST.STATUS_OPEN))

        # Call our device callback method for our cover
        # pylint: disable=protected-access
        events._on_device_update(cover.device_id)
        callback.assert_called_with(cover)

        # Test that our device updated
        self.assertEqual(cover.status, CONST.STATUS_OPEN)

        # Test that our other device didn't update
        self.assertEqual(doorcontact.status, CONST.STATUS_CLOSED)

        # Call our device callback method for our door contact
        events._on_device_update(doorcontact.device_id)
        callback.assert_has_calls([call(cover), call(doorcontact)])

        # Test that our door updated now
        self.assertEqual(doorcontact.status, CONST.STATUS_OPEN)

    def tests_multi_events_callback(self):
        """Tests that multiple event updates callback correctly."""
        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        # Create mock callback
        callback = Mock()

        # Register our events
        self.assertTrue(
            events.add_event_callback(
                [TIMELINE.ALARM_GROUP, TIMELINE.CAPTURE_GROUP],
                callback))

        # Call our events callback method and trigger a capture group event
        # pylint: disable=protected-access
        event_json = json.loads(IRCAMERA.timeline_event())
        events._on_timeline_update(event_json)

        # Ensure our callback was called
        callback.assert_called_with(event_json)

    def tests_multi_timeline_callback(self):
        """Tests that multiple timeline updates callback correctly."""
        # Get the event controller
        events = self.abode.events
        self.assertIsNotNone(events)

        # Create mock callback
        callback = Mock()

        # Register our events
        self.assertTrue(
            events.add_timeline_callback(
                [TIMELINE.CAPTURE_IMAGE, TIMELINE.OPENED], callback))

        # Call our events callback method and trigger a capture group event
        # pylint: disable=protected-access
        event_json = json.loads(IRCAMERA.timeline_event())
        events._on_timeline_update(event_json)

        # Ensure our callback was called
        callback.assert_called_with(event_json)
