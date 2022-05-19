"""Test the Abode camera class."""
import base64
import os
import unittest

import requests_mock

import abodepy
from abodepy.exceptions import AbodeException
import abodepy.helpers.constants as CONST
import abodepy.helpers.errors as ERROR
import tests.mock as MOCK
import tests.mock.devices.ipcam as IPCAM
import tests.mock.devices.ir_camera as IRCAMERA
import tests.mock.login as LOGIN
import tests.mock.logout as LOGOUT
import tests.mock.oauth_claims as OAUTH_CLAIMS
import tests.mock.panel as PANEL

USERNAME = "foobar"
PASSWORD = "deadbeef"


def set_cam_type(device_type):
    """Return camera type_tag."""
    if device_type == CONST.DEVICE_IP_CAM:
        return IPCAM

    if device_type == CONST.DEVICE_MOTION_CAMERA:
        return IRCAMERA

    return None


@requests_mock.Mocker()
class TestCamera(unittest.TestCase):
    """Test the AbodePy camera."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(
            username=USERNAME, password=PASSWORD, disable_cache=True
        )

        self.all_devices = (
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

        # Logout to reset everything
        self.abode.logout()

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    def tests_camera_properties(self, m):
        """Tests that camera properties work as expected."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL, text=self.all_devices)

        # Get our camera
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Specify which device module to use based on type_tag
            cam_type = set_cam_type(device.type_tag)

            # Test our device
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)
            self.assertFalse(device.battery_low)
            self.assertFalse(device.no_response)

            # Set up our direct device get url
            device_url = str.replace(CONST.DEVICE_URL,
                                     "$DEVID$", device.device_id)

            # Change device properties
            m.get(
                device_url,
                text=cam_type.device(
                    devid=cam_type.DEVICE_ID,
                    status=CONST.STATUS_OFFLINE,
                    low_battery=True,
                    no_response=True,
                ),
            )

            # Refesh device and test changes
            device.refresh()

            self.assertEqual(device.status, CONST.STATUS_OFFLINE)
            self.assertTrue(device.battery_low)
            self.assertTrue(device.no_response)

    def tests_camera_capture(self, m):
        """Tests that camera devices capture new images."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL, text=self.all_devices)

        # Test our camera devices
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Specify which device module to use based on type_tag
            cam_type = set_cam_type(device.type_tag)

            # Test that we have the camera devices
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)

            # Determine URL based on device type
            if device.type_tag == CONST.DEVICE_IP_CAM:
                url = CONST.BASE_URL + cam_type.CONTROL_URL_SNAPSHOT

            elif device.type_tag == CONST.DEVICE_MOTION_CAMERA:
                url = CONST.BASE_URL + cam_type.CONTROL_URL

            # Set up capture URL response
            m.put(url, text=MOCK.generic_response_ok())

            # Capture an image
            self.assertTrue(device.capture())

            # Change capture URL responses
            m.put(url, text=cam_type.get_capture_timeout(), status_code=600)

            # Capture an image with a failure
            self.assertFalse(device.capture())

            # Remove control URLs from JSON to test if Abode makes
            # changes to JSON
            # pylint: disable=protected-access
            for key in list(device._json_state.keys()):
                if key.startswith("control_url"):
                    # pylint: disable=protected-access
                    del device._json_state[key]

            # Test that AbodeException is raised with no control URLs
            with self.assertRaises(AbodeException) as exc:
                device.capture()
                self.assertEqual(str(exc.exception),
                                 ERROR.MISSING_CONTROL_URL)

    def tests_camera_image_update(self, m):
        """Tests that camera devices update correctly via timeline request."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL, text=self.all_devices)

        # Test our camera devices
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Specify which device module to use based on type_tag
            cam_type = set_cam_type(device.type_tag)

            # Test that we have our device
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)

            # Set up timeline response
            url = str.replace(CONST.TIMELINE_IMAGES_ID_URL,
                              "$DEVID$", device.device_id)

            m.get(url,
                  text="[" + cam_type.timeline_event(device.device_id) + "]")
            # Set up our file path response
            file_path = CONST.BASE_URL + cam_type.FILE_PATH
            m.head(
                file_path,
                status_code=302,
                headers={"Location": cam_type.LOCATION_HEADER},
            )

            # Refresh the image
            self.assertTrue(device.refresh_image())

            # Verify the image location
            self.assertEqual(device.image_url, cam_type.LOCATION_HEADER)

            # Test that a bad file_path response header results in an exception
            file_path = CONST.BASE_URL + cam_type.FILE_PATH
            m.head(file_path, status_code=302)

            with self.assertRaises(abodepy.AbodeException):
                device.refresh_image()

            # Test that a bad file_path response code results in an exception
            file_path = CONST.BASE_URL + cam_type.FILE_PATH
            m.head(
                file_path,
                status_code=200,
                headers={"Location": cam_type.LOCATION_HEADER},
            )

            with self.assertRaises(abodepy.AbodeException):
                device.refresh_image()

            # Test that an an empty timeline event throws exception
            url = str.replace(CONST.TIMELINE_IMAGES_ID_URL,
                              "$DEVID$", device.device_id)
            m.get(
                url,
                text="["
                + cam_type.timeline_event(device.device_id, file_path="")
                + "]",
            )

            with self.assertRaises(abodepy.AbodeException):
                device.refresh_image()

            # Test that an unexpected timeline event throws exception
            url = str.replace(CONST.TIMELINE_IMAGES_ID_URL,
                              "$DEVID$", device.device_id)
            m.get(
                url,
                text="["
                + cam_type.timeline_event(device.device_id, event_code="1234")
                + "]",
            )

            with self.assertRaises(abodepy.AbodeException):
                device.refresh_image()

    def tests_camera_no_image_update(self, m):
        """Tests that camera updates correctly with no timeline events."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL, text=self.all_devices)

        # Test our camera devices
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Test that we have our device
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)

            # Set up timeline response
            url = str.replace(CONST.TIMELINE_IMAGES_ID_URL,
                              "$DEVID$", device.device_id)
            m.get(url, text="[]")

            # Refresh the image
            self.assertFalse(device.refresh_image())
            self.assertIsNone(device.image_url)

    def tests_camera_image_write(self, m):
        """Tests that camera images will write to a file."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL, text=self.all_devices)

        # Test our camera devices
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Specify which device module to use based on type_tag
            cam_type = set_cam_type(device.type_tag)

            # Test that we have our device
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)

            # Set up timeline response
            url = str.replace(CONST.TIMELINE_IMAGES_ID_URL,
                              "$DEVID$", device.device_id)
            m.get(url,
                  text="[" + cam_type.timeline_event(device.device_id) + "]")

            # Set up our file path response
            file_path = CONST.BASE_URL + cam_type.FILE_PATH
            m.head(
                file_path,
                status_code=302,
                headers={"Location": cam_type.LOCATION_HEADER},
            )

            # Set up our image response
            image_response = "this is a beautiful jpeg image"
            m.get(cam_type.LOCATION_HEADER, text=image_response)

            # Refresh the image
            path = "test.jpg"
            self.assertTrue(device.image_to_file(path, get_image=True))

            # Test the file written and cleanup
            image_data = open(path, "r").read()
            self.assertTrue(image_response, image_data)
            os.remove(path)

            # Test that bad response returns False
            m.get(cam_type.LOCATION_HEADER, status_code=400)
            with self.assertRaises(abodepy.AbodeException):
                device.image_to_file(path, get_image=True)

            # Test that the image fails to update returns False
            m.get(url, text="[]")
            self.assertFalse(device.image_to_file(path, get_image=True))

    def tests_camera_snapshot(self, m):
        """Tests that camera devices capture new snapshots."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL, text=self.all_devices)

        # Test our camera devices
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Specify which device module to use based on type_tag
            cam_type = set_cam_type(device.type_tag)

            # Test that we have the camera devices
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)

            # Set up snapshot URL response
            snapshot_url = (CONST.CAMERA_INTEGRATIONS_URL +
                            device.device_uuid + '/snapshot')
            m.post(snapshot_url, text='{"base64Image":"test"}')

            # Retrieve a snapshot
            self.assertTrue(device.snapshot())

            # Failed snapshot retrieval due to timeout response
            m.post(snapshot_url, text=cam_type.get_capture_timeout(),
                   status_code=600)
            self.assertFalse(device.snapshot())

            # Failed snapshot retrieval due to missing data
            m.post(snapshot_url, text="{}")
            self.assertFalse(device.snapshot())

    def tests_camera_snapshot_write(self, m):
        """Tests that camera snapshots will write to a file."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL, text=self.all_devices)

        # Test our camera devices
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Specify which device module to use based on type_tag
            cam_type = set_cam_type(device.type_tag)

            # Test that we have our device
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)

            # Set up snapshot URL and image response
            snapshot_url = (CONST.CAMERA_INTEGRATIONS_URL +
                            device.device_uuid + '/snapshot')
            image_response = b'this is a beautiful jpeg image'
            b64_image = str(base64.b64encode(image_response), 'utf-8')
            m.post(snapshot_url,
                   text='{"base64Image":"' + b64_image + '"}')

            # Request the snapshot and write to file
            path = "test.jpg"
            self.assertTrue(device.snapshot_to_file(path, get_snapshot=True))

            # Test the file written and cleanup
            image_data = open(path, 'rb').read()
            self.assertTrue(image_response, image_data)
            os.remove(path)

            # Test that bad response returns False
            m.post(snapshot_url, text=cam_type.get_capture_timeout(),
                   status_code=600)
            self.assertFalse(device.snapshot_to_file(path, get_snapshot=True))

    def tests_camera_snapshot_data_url(self, m):
        """Tests that camera snapshots can be converted to a data url."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL, text=self.all_devices)

        # Test our camera devices
        for device in self.abode.get_devices():
            # Skip alarm devices
            if device.type_tag == CONST.DEVICE_ALARM:
                continue

            # Specify which device module to use based on type_tag
            cam_type = set_cam_type(device.type_tag)

            # Test that we have our device
            self.assertIsNotNone(device)
            self.assertEqual(device.status, CONST.STATUS_ONLINE)

            # Set up snapshot URL and image response
            snapshot_url = (CONST.CAMERA_INTEGRATIONS_URL +
                            device.device_uuid + '/snapshot')
            image_response = b'this is a beautiful jpeg image'
            b64_image = str(base64.b64encode(image_response), 'utf-8')
            m.post(snapshot_url,
                   text='{"base64Image":"' + b64_image + '"}')

            # Request the snapshot as a data url
            data_url = device.snapshot_data_url(get_snapshot=True)

            # Test the data url matches the image response
            header, encoded = data_url.split(',', 1)
            decoded = base64.b64decode(encoded)
            self.assertEqual(header, 'data:image/jpeg;base64')
            self.assertEqual(decoded, image_response)

            # Test that bad response returns an empty string
            m.post(snapshot_url, text=cam_type.get_capture_timeout(),
                   status_code=600)
            self.assertEqual(device.snapshot_data_url(get_snapshot=True), '')

    def tests_camera_privacy_mode(self, m):
        """Tests camera privacy mode."""
        # Set up mock URLs
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL,
              text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(CONST.DEVICES_URL, text=self.all_devices)

        # Get the IP camera and test we have it
        device = self.abode.get_device(IPCAM.DEVICE_ID)
        self.assertIsNotNone(device)
        self.assertEqual(device.status, CONST.STATUS_ONLINE)

        # Set up params URL response for privacy mode on
        m.put(CONST.PARAMS_URL + device.device_id,
              text=IPCAM.device(privacy=1))

        # Set privacy mode on
        self.assertTrue(device.privacy_mode(True))

        # Set up params URL response for privacy mode off
        m.put(CONST.PARAMS_URL + device.device_id,
              text=IPCAM.device(privacy=0))

        # Set privacy mode off
        self.assertTrue(device.privacy_mode(False))

        # Test that an invalid privacy response throws exception
        with self.assertRaises(abodepy.AbodeException):
            device.privacy_mode(True)
