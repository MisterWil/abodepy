"""Test the Abode camera class."""
import os
import unittest

import requests_mock

import abodepy
import abodepy.helpers.constants as CONST
import abodepy.helpers.errors as ERROR
import tests.mock as MOCK
import tests.mock.devices.ipcam as IPCAM
import tests.mock.devices.ir_camera as IRCAMERA
import tests.mock.login as LOGIN
import tests.mock.logout as LOGOUT
import tests.mock.oauth_claims as OAUTH_CLAIMS
import tests.mock.panel as PANEL
from abodepy.exceptions import AbodeException

USERNAME = "foobar"
PASSWORD = "deadbeef"


class TestCamera(unittest.TestCase):
    """Test the AbodePy camera."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(
            username=USERNAME, password=PASSWORD, disable_cache=True
        )

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    @requests_mock.mock()
    def tests_camera_properties(self, m):
        """Tests that camera properties work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))

        all_devices = (
            "["
            + IRCAMERA.device(
                devid=IRCAMERA.DEVICE_ID,
                status=CONST.STATUS_ONLINE,
                low_battery=False,
                no_response=False,
            )
            + ","
            + IPCAM.device(
                devid=IPCAM.DEVICE_ID,
                status=CONST.STATUS_ONLINE,
                low_battery=False,
                no_response=False,
            )
            + "]"
        )

        m.get(CONST.DEVICES_URL, text=all_devices)

        # Logout to reset everything
        self.abode.logout()

        # Get our camera
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Test our device
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)
            self.assertFalse(device.battery_low)
            self.assertFalse(device.no_response)

            # Set up our direct device get url
            device_url = str.replace(CONST.DEVICE_URL, "$DEVID$", device.device_id)

            # Change device properties
            all_devices = (
                "["
                + IRCAMERA.device(
                    devid=IRCAMERA.DEVICE_ID,
                    status=CONST.STATUS_OFFLINE,
                    low_battery=True,
                    no_response=True,
                )
                + ","
                + IPCAM.device(
                    devid=IPCAM.DEVICE_ID,
                    status=CONST.STATUS_OFFLINE,
                    low_battery=True,
                    no_response=True,
                )
                + "]"
            )

            m.get(device_url, text=all_devices)

            # Refesh device and test changes
            device.refresh()

            self.assertEqual(device.status, CONST.STATUS_OFFLINE)
            self.assertTrue(device.battery_low)
            self.assertTrue(device.no_response)

    @requests_mock.mock()
    def tests_camera_capture(self, m):
        """Tests that camera devices capture new images."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))

        all_devices = (
            "["
            + IRCAMERA.device(
                devid=IRCAMERA.DEVICE_ID,
                status=CONST.STATUS_ONLINE,
                low_battery=False,
                no_response=False,
            )
            + ","
            + IPCAM.device(
                devid=IPCAM.DEVICE_ID,
                status=CONST.STATUS_ONLINE,
                low_battery=False,
                no_response=False,
            )
            + "]"
        )

        m.get(CONST.DEVICES_URL, text=all_devices)

        # Logout to reset everything
        self.abode.logout()

        # Test our camera devices
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Specify which device module to use based on type_tag
            if device.type_tag == CONST.DEVICE_IP_CAM:
                CAM_TYPE = IPCAM
                url = CONST.BASE_URL + CAM_TYPE.CONTROL_URL_SNAPSHOT

            elif device.type_tag == CONST.DEVICE_MOTION_CAMERA:
                CAM_TYPE = IRCAMERA
                url = CONST.BASE_URL + CAM_TYPE.CONTROL_URL

            # Test that we have the camera devices
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)

            # Set up capture URL response
            m.put(url, text=MOCK.generic_response_ok())

            # Capture an image
            self.assertTrue(device.capture())

            # Change capture URL responses
            m.put(url, text=CAM_TYPE.get_capture_timeout(), status_code=600)

            # Capture an image with a failure
            self.assertFalse(device.capture())

            # Remove 'control_url' from JSON to test if Abode makes changes to JSON
            for key in list(device._json_state.keys()):
                if key.startswith("control_url"):
                    del device._json_state[key]

            # Test that AbodeException is raised
            with self.assertRaises(AbodeException) as exc:
                device.capture()
                self.assertEqual(str(exc.exception), ERROR.MISSING_CONTROL_URL)

    @requests_mock.mock()
    def tests_camera_image_update(self, m):
        """Tests that camera devices update correctly via timeline request."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))

        all_devices = (
            "["
            + IRCAMERA.device(
                devid=IRCAMERA.DEVICE_ID,
                status=CONST.STATUS_ONLINE,
                low_battery=False,
                no_response=False,
            )
            + ","
            + IPCAM.device(
                devid=IPCAM.DEVICE_ID,
                status=CONST.STATUS_ONLINE,
                low_battery=False,
                no_response=False,
            )
            + "]"
        )

        m.get(CONST.DEVICES_URL, text=all_devices)

        # Logout to reset everything
        self.abode.logout()

        # Test our camera devices
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Specify which device module to use based on type_tag
            if device.type_tag == CONST.DEVICE_IP_CAM:
                CAM_TYPE = IPCAM

            elif device.type_tag == CONST.DEVICE_MOTION_CAMERA:
                CAM_TYPE = IRCAMERA

            # Test that we have our device
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)

            # Set up timeline response
            url = str.replace(CONST.TIMELINE_IMAGES_ID_URL, "$DEVID$", device.device_id)

            m.get(url, text="[" + CAM_TYPE.timeline_event(device.device_id) + "]")
            # Set up our file path response
            file_path = CONST.BASE_URL + CAM_TYPE.FILE_PATH
            m.head(
                file_path,
                status_code=302,
                headers={"Location": CAM_TYPE.LOCATION_HEADER},
            )

            # Refresh the image
            self.assertTrue(device.refresh_image())

            # Verify the image location
            self.assertEqual(device.image_url, CAM_TYPE.LOCATION_HEADER)

            # Test that a bad file_path response header results in an exception
            file_path = CONST.BASE_URL + CAM_TYPE.FILE_PATH
            m.head(file_path, status_code=302)

            with self.assertRaises(abodepy.AbodeException):
                device.refresh_image()

            # Test that a bad file_path response code results in an exception
            file_path = CONST.BASE_URL + CAM_TYPE.FILE_PATH
            m.head(
                file_path,
                status_code=200,
                headers={"Location": CAM_TYPE.LOCATION_HEADER},
            )

            with self.assertRaises(abodepy.AbodeException):
                device.refresh_image()

            # Test that an an empty timeline event throws exception
            url = str.replace(CONST.TIMELINE_IMAGES_ID_URL, "$DEVID$", device.device_id)
            m.get(
                url,
                text="["
                + CAM_TYPE.timeline_event(device.device_id, file_path="")
                + "]",
            )

            with self.assertRaises(abodepy.AbodeException):
                device.refresh_image()

            # Test that an unexpected timeline event throws exception
            url = str.replace(CONST.TIMELINE_IMAGES_ID_URL, "$DEVID$", device.device_id)
            m.get(
                url,
                text="["
                + CAM_TYPE.timeline_event(device.device_id, event_code="1234")
                + "]",
            )

            with self.assertRaises(abodepy.AbodeException):
                device.refresh_image()

    @requests_mock.mock()
    def tests_camera_no_image_update(self, m):
        """Tests that camera updates correctly with no timeline events."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))

        all_devices = (
            "["
            + IRCAMERA.device(
                devid=IRCAMERA.DEVICE_ID,
                status=CONST.STATUS_ONLINE,
                low_battery=False,
                no_response=False,
            )
            + ","
            + IPCAM.device(
                devid=IPCAM.DEVICE_ID,
                status=CONST.STATUS_ONLINE,
                low_battery=False,
                no_response=False,
            )
            + "]"
        )

        m.get(CONST.DEVICES_URL, text=all_devices)

        # Logout to reset everything
        self.abode.logout()

        # Test our camera devices
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Test that we have our device
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)

            # Set up timeline response
            url = str.replace(CONST.TIMELINE_IMAGES_ID_URL, "$DEVID$", device.device_id)
            m.get(url, text="[]")

            # Refresh the image
            self.assertFalse(device.refresh_image())
            self.assertIsNone(device.image_url)

    @requests_mock.mock()
    def tests_camera_image_write(self, m):
        """Tests that camera images will write to a file."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))

        all_devices = (
            "["
            + IRCAMERA.device(
                devid=IRCAMERA.DEVICE_ID,
                status=CONST.STATUS_ONLINE,
                low_battery=False,
                no_response=False,
            )
            + ","
            + IPCAM.device(
                devid=IPCAM.DEVICE_ID,
                status=CONST.STATUS_ONLINE,
                low_battery=False,
                no_response=False,
            )
            + "]"
        )

        m.get(CONST.DEVICES_URL, text=all_devices)

        # Logout to reset everything
        self.abode.logout()

        # Test our camera devices
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Specify which device module to use based on type_tag
            if device.type_tag == CONST.DEVICE_IP_CAM:
                CAM_TYPE = IPCAM

            elif device.type_tag == CONST.DEVICE_MOTION_CAMERA:
                CAM_TYPE = IRCAMERA

            # Test that we have our device
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)

            # Set up timeline response
            url = str.replace(CONST.TIMELINE_IMAGES_ID_URL, "$DEVID$", device.device_id)
            m.get(url, text="[" + CAM_TYPE.timeline_event(device.device_id) + "]")

            # Set up our file path response
            file_path = CONST.BASE_URL + CAM_TYPE.FILE_PATH
            m.head(
                file_path,
                status_code=302,
                headers={"Location": CAM_TYPE.LOCATION_HEADER},
            )

            # Set up our image response
            image_response = "this is a beautiful jpeg image"
            m.get(CAM_TYPE.LOCATION_HEADER, text=image_response)

            # Refresh the image
            path = "test.jpg"
            self.assertTrue(device.image_to_file(path, get_image=True))

            # Test the file written and cleanup
            image_data = open(path, "r").read()
            self.assertTrue(image_response, image_data)
            os.remove(path)

            # Test that bad response returns False
            m.get(CAM_TYPE.LOCATION_HEADER, status_code=400)
            with self.assertRaises(abodepy.AbodeException):
                device.image_to_file(path, get_image=True)

            # Test that the image fails to update returns False
            m.get(url, text="[]")
            self.assertFalse(device.image_to_file(path, get_image=True))
