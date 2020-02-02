"""Representation of an automation configured in Abode."""
import json
import logging

from abodepy.exceptions import AbodeException

import abodepy.helpers.constants as CONST
import abodepy.helpers.errors as ERROR

_LOGGER = logging.getLogger(__name__)


class AbodeAutomation:
    """Class for viewing and controlling automations."""

    def __init__(self, abode, automation):
        """Init AbodeAutomation class."""
        self._abode = abode
        self._automation = automation

    def enable(self):
        """Enable an automation."""
        url = CONST.AUTOMATION_URL + self.automation_id

        response = self._abode.send_request(
            method="patch", url=url, data={'enabled': True})

        response_object = json.loads(response.text)

        _LOGGER.info("Automation enabled: %s", response_object['name'])
        _LOGGER.debug("Enable automation response: %s", response.text)

        if isinstance(response_object, (tuple, list)):
            response_object = response_object[0]

        if str(response_object['id']) != str(self._automation['id']):
            raise AbodeException((ERROR.INVALID_AUTOMATION_EDIT_RESPONSE))

        self.update(response_object)

        return True

    def disable(self):
        """Disable an automation."""
        url = CONST.AUTOMATION_URL + self.automation_id

        response = self._abode.send_request(
            method="patch", url=url, data={'enabled': False})

        response_object = json.loads(response.text)

        _LOGGER.info("Automation disabled: %s", response_object['name'])
        _LOGGER.debug("Disable automation response: %s", response.text)

        if isinstance(response_object, (tuple, list)):
            response_object = response_object[0]

        if str(response_object['id']) != str(self._automation['id']):
            raise AbodeException((ERROR.INVALID_AUTOMATION_EDIT_RESPONSE))

        self.update(response_object)

        return True

    def trigger(self):
        """Trigger an automation."""
        url = CONST.AUTOMATION_APPLY_URL
        url = url.replace(
            '$AUTOMATIONID$', self.automation_id)

        self._abode.send_request(
            method="post", url=url)

        return True

    def refresh(self):
        """Refresh the automation."""
        url = CONST.AUTOMATION_ID_URL
        url = url.replace(
            '$AUTOMATIONID$', self.automation_id)

        response = self._abode.send_request(method="get", url=url)
        response_object = json.loads(response.text)

        if isinstance(response_object, (tuple, list)):
            response_object = response_object[0]

        if str(response_object['id']) != self.automation_id:
            raise AbodeException((ERROR.INVALID_AUTOMATION_REFRESH_RESPONSE))

        self.update(response_object)

    def update(self, automation):
        """Update the internal automation json."""
        self._automation.update(
            {k: automation[k] for k in automation if self._automation.get(k)})

    @property
    def automation_id(self):
        """Get the id of the automation."""
        return str(self._automation['id'])

    @property
    def name(self):
        """Get the name of the automation."""
        return self._automation['name']

    @property
    def is_enabled(self):
        """Return True if the automation is enabled."""
        return self._automation['enabled']

    @property
    def generic_type(self):
        """Get the generic type of the automation."""
        return CONST.TYPE_AUTOMATION

    @property
    def sub_type(self):
        """Get the sub type of the automation."""
        return self._automation['subType']

    @property
    def desc(self):
        """Get a short description of the automation."""
        return '{0} (ID: {1}, Enabled: {2})'.format(
            self.name, self.automation_id, self.is_enabled)
