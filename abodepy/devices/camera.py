"""Abode camera device."""
import json
import logging
from shutil import copyfileobj
import requests

from abodepy.exceptions import AbodeException
from abodepy.devices import AbodeDevice
import abodepy.helpers.constants as CONST
import abodepy.helpers.errors as ERROR
import abodepy.helpers.timeline as TIMELINE

_LOGGER = logging.getLogger(__name__)


class AbodeCamera(AbodeDevice):
    """Class to represent a camera device."""

    def __init__(self, json_obj, abode):
        """Set up Abode alarm device."""
        AbodeDevice.__init__(self, json_obj, abode)
        self._image_url = None

    def capture(self):
        """Request a new camera image."""
        # Abode IP cameras use a different URL for image captures.
        if 'control_url_snapshot' in self._json_state:
            url = CONST.BASE_URL + self._json_state['control_url_snapshot']

        elif 'control_url' in self._json_state:
            url = CONST.BASE_URL + self._json_state['control_url']

        else:
            raise AbodeException((ERROR.MISSING_CONTROL_URL))

        try:
            response = self._abode.send_request("put", url)

            _LOGGER.debug("Capture image response: %s", response.text)

            return True

        except AbodeException as exc:
            _LOGGER.warning("Failed to capture image: %s", exc)

        return False

    def refresh_image(self):
        """Get the most recent camera image."""
        url = str.replace(CONST.TIMELINE_IMAGES_ID_URL,
                          '$DEVID$', self.device_id)
        response = self._abode.send_request("get", url)

        _LOGGER.debug("Get image response: %s", response.text)

        return self.update_image_location(json.loads(response.text))

    def update_image_location(self, timeline_json):
        """Update the image location."""
        if not timeline_json:
            return False

        # If we get a list of objects back (likely)
        # then we just want the first one as it should be the "newest"
        if isinstance(timeline_json, (tuple, list)):
            timeline_json = timeline_json[0]

        # Verify that the event code is of the "CAPTURE IMAGE" event
        event_code = timeline_json.get('event_code')
        if event_code != TIMELINE.CAPTURE_IMAGE['event_code']:
            raise AbodeException((ERROR.CAM_TIMELINE_EVENT_INVALID))

        # The timeline response has an entry for "file_path" that acts as the
        # location of the image within the Abode servers.
        file_path = timeline_json.get('file_path')
        if not file_path:
            raise AbodeException((ERROR.CAM_IMAGE_REFRESH_NO_FILE))

        # Perform a "head" request for the image and look for a
        # 302 Found response
        url = CONST.BASE_URL + file_path
        response = self._abode.send_request("head", url)

        if response.status_code != 302:
            _LOGGER.warning("Unexected response code %s with body: %s",
                            str(response.status_code), response.text)
            raise AbodeException((ERROR.CAM_IMAGE_UNEXPECTED_RESPONSE))

        # The response should have a location header that is the actual
        # location of the image stored on AWS
        location = response.headers.get('location')
        if not location:
            raise AbodeException((ERROR.CAM_IMAGE_NO_LOCATION_HEADER))

        self._image_url = location

        return True

    def image_to_file(self, path, get_image=True):
        """Write the image to a file."""
        if not self.image_url or get_image:
            if not self.refresh_image():
                return False

        response = requests.get(self.image_url, stream=True)

        if response.status_code != 200:
            _LOGGER.warning(
                "Unexpected response code %s when requesting image: %s",
                str(response.status_code), response.text)
            raise AbodeException((ERROR.CAM_IMAGE_REQUEST_INVALID))

        with open(path, 'wb') as imgfile:
            copyfileobj(response.raw, imgfile)

        return True

    def privacy_mode(self, enable):
        """Set camera privacy mode (camera on/off)."""
        if self._json_state['privacy']:
            privacy = '1' if enable else '0'

            url = CONST.PARAMS_URL + self.device_id

            camera_data = {
                'mac': self._json_state['camera_mac'],
                'privacy': privacy,
                'action': 'setParam',
                'id': self.device_id
            }

            response = self._abode.send_request(
                method="put", url=url, data=camera_data)
            response_object = json.loads(response.text)

            _LOGGER.debug("Camera Privacy Mode Response: %s", response.text)

            if response_object['id'] != self.device_id:
                raise AbodeException((ERROR.SET_STATUS_DEV_ID))

            if response_object['privacy'] != str(privacy):
                raise AbodeException((ERROR.SET_PRIVACY_MODE))

            _LOGGER.info("Set camera %s privacy mode to: %s",
                         self.device_id, privacy)

            return True

        return False

    @property
    def image_url(self):
        """Get image URL."""
        return self._image_url

    @property
    def is_on(self):
        """Get camera state (assumed on)."""
        return self.status not in (CONST.STATUS_OFF, CONST.STATUS_OFFLINE)
