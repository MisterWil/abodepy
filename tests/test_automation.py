"""Test the Abode device classes."""
import json
import unittest

import requests_mock

import abodepy
import abodepy.helpers.constants as CONST

import tests.mock.login as LOGIN
import tests.mock.logout as LOGOUT
import tests.mock.panel as PANEL
import tests.mock.automation as AUTOMATION
# from abodepy.exceptions import AbodeException


USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestDevice(unittest.TestCase):
    """Test the generic AbodePy device class."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(username=USERNAME,
                                   password=PASSWORD)

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    @requests_mock.mock()
    def tests_automation_init(self, m):
        """Check the Abode automation class init's properly."""
        # Set up URLs
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        # Set up automation
        automation_text = '[' + \
            AUTOMATION.get_response_ok(
                aid=1,
                name='Test Automation',
                is_active=True,
                the_type=CONST.AUTOMATION_TYPE_LOCATION,
                sub_type=CONST.AUTOMATION_SUBTYPE_ENTERING_HOME) + ']'

        automation_json = json.loads(automation_text)

        m.get(CONST.AUTOMATION_URL, text=automation_text)

        # Logout to reset everything
        self.abode.logout()

        # Get our specific device
        automation = self.abode.get_automation(1)

        # Check device states match
        self.assertIsNotNone(automation)
        # pylint: disable=W0212
        self.assertEqual(automation._automation, automation_json[0])
        self.assertEqual(automation.name, automation_json[0]['name'])
        self.assertEqual(automation.type, automation_json[0]['type'])
        self.assertEqual(automation.sub_type, automation_json[0]['sub_type'])
        self.assertEqual(automation.automation_id,
                         str(automation_json[0]['id']))
        self.assertEqual(automation.is_active, True)
        self.assertEqual(automation.is_quick_action, False)
