"""Test the Abode device classes."""
import json
import unittest

import requests_mock

import abodepy
import abodepy.helpers.constants as CONST

import tests.mock as MOCK
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
        automation_text = AUTOMATION.get_response_ok(
            aid=1,
            name='Test Automation',
            is_active=True,
            the_type=CONST.AUTOMATION_TYPE_LOCATION,
            sub_type=CONST.AUTOMATION_SUBTYPE_ENTERING_HOME)

        automation_json = json.loads(automation_text)

        m.get(CONST.AUTOMATION_URL, text=automation_text)

        # Logout to reset everything
        self.abode.logout()

        # Get our specific automation
        automation = self.abode.get_automation(1)

        # Check automation states match
        self.assertIsNotNone(automation)
        # pylint: disable=W0212
        self.assertEqual(automation._automation, automation_json)
        self.assertEqual(automation.name, automation_json['name'])
        self.assertEqual(automation.type, automation_json['type'])
        self.assertEqual(automation.sub_type, automation_json['sub_type'])
        self.assertEqual(automation.automation_id,
                         str(automation_json['id']))
        self.assertEqual(automation.is_active, True)
        self.assertEqual(automation.is_quick_action, False)
        self.assertEqual(automation.generic_type, CONST.TYPE_AUTOMATION)
        self.assertIsNotNone(automation.desc)

    @requests_mock.mock()
    def tests_automation_refresh(self, m):
        """Check the automation Abode class refreshes."""
        # Set up URL's
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

        # Set up refreshed automation
        automation_text_changed = '[' + \
            AUTOMATION.get_response_ok(
                aid=1,
                name='Test Automation Changed',
                is_active=False,
                the_type=CONST.AUTOMATION_TYPE_SCHEDULE,
                sub_type="Foobar") + ']'

        automation_json_changed = json.loads(automation_text_changed)

        automation_id_url = str.replace(CONST.AUTOMATION_ID_URL,
                                        '$AUTOMATIONID$',
                                        str(automation_json[0]['id']))
        m.get(automation_id_url, text=automation_text_changed)

        # Logout to reset everything
        self.abode.logout()

        # Get the first automation and test
        automation = self.abode.get_automation(1)

        # Check automation states match
        # pylint: disable=W0212
        self.assertIsNotNone(automation)
        self.assertEqual(automation._automation, automation_json[0])

        # Refresh and retest
        automation.refresh()
        self.assertEqual(automation._automation, automation_json_changed[0])

        # Refresh with get_automation() and test
        automation_text_changed = '[' + \
            AUTOMATION.get_response_ok(
                aid=1,
                name='Test Automation Changed Again',
                is_active=True,
                the_type=CONST.AUTOMATION_TYPE_MANUAL,
                sub_type="Deadbeef") + ']'

        automation_json_changed = json.loads(automation_text_changed)
        m.get(automation_id_url, text=automation_text_changed)

        # Refresh and retest
        automation = self.abode.get_automation(1, refresh=True)
        self.assertEqual(automation._automation, automation_json_changed[0])

        # Test refresh returning an incorrect ID throws exception
        # Set up refreshed automation
        automation_text_changed = '[' + \
            AUTOMATION.get_response_ok(
                aid=2,
                name='Test Automation Changed',
                is_active=False,
                the_type=CONST.AUTOMATION_TYPE_SCHEDULE) + ']'

        m.get(automation_id_url, text=automation_text_changed)

        with self.assertRaises(abodepy.AbodeException):
            automation.refresh()

    @requests_mock.mock()
    def tests_multiple_automations(self, m):
        """Check that multiple automations work and return correctly."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        # Set up automations
        automation_text = '[' + \
            AUTOMATION.get_response_ok(
                aid=1,
                name='Test Automation Uno',
                is_active=True,
                the_type=CONST.AUTOMATION_TYPE_LOCATION,
                sub_type=CONST.AUTOMATION_SUBTYPE_ENTERING_HOME) + ',' + \
            AUTOMATION.get_response_ok(
                aid=2,
                name='Test Automation Dos',
                is_active=True,
                the_type=CONST.AUTOMATION_TYPE_STATUS) + ',' + \
            AUTOMATION.get_response_ok(
                aid=3,
                name='Test Automation Tres',
                is_active=True,
                the_type=CONST.AUTOMATION_TYPE_SCHEDULE) + ']'

        automation_json = json.loads(automation_text)

        m.get(CONST.AUTOMATION_URL, text=automation_text)

        # Logout to reset everything
        self.abode.logout()

        # Test that the automations return the correct number
        automations = self.abode.get_automations()
        self.assertEqual(len(automations), 3)

        # Get the first automation and test
        # pylint: disable=W0212
        automation_1 = self.abode.get_automation(1)
        self.assertIsNotNone(automation_1)
        self.assertEqual(automation_1._automation, automation_json[0])

        automation_2 = self.abode.get_automation(2)
        self.assertIsNotNone(automation_2)
        self.assertEqual(automation_2._automation, automation_json[1])

        automation_3 = self.abode.get_automation(3)
        self.assertIsNotNone(automation_3)
        self.assertEqual(automation_3._automation, automation_json[2])

    @requests_mock.mock()
    def tests_automation_class_reuse(self, m):
        """Check that automations reuse the same classes when refreshed."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        # Set up automations
        automation_text = '[' + \
            AUTOMATION.get_response_ok(
                aid=1,
                name='Test Automation Uno',
                is_active=True,
                the_type=CONST.AUTOMATION_TYPE_LOCATION,
                sub_type=CONST.AUTOMATION_SUBTYPE_ENTERING_HOME) + ',' + \
            AUTOMATION.get_response_ok(
                aid=2,
                name='Test Automation Dos',
                is_active=True,
                the_type=CONST.AUTOMATION_TYPE_STATUS) + ']'

        automation_json = json.loads(automation_text)

        m.get(CONST.AUTOMATION_URL, text=automation_text)

        # Logout to reset everything
        self.abode.logout()

        # Test that the automations return the correct number
        automations = self.abode.get_automations()
        self.assertEqual(len(automations), 2)

        # Get the automations and test
        # pylint: disable=W0212
        automation_1 = self.abode.get_automation(1)
        self.assertIsNotNone(automation_1)
        self.assertEqual(automation_1._automation, automation_json[0])

        automation_2 = self.abode.get_automation(2)
        self.assertIsNotNone(automation_2)
        self.assertEqual(automation_2._automation, automation_json[1])

        # Update the automations
        automation_text = '[' + \
            AUTOMATION.get_response_ok(
                aid=1,
                name='Test Automation Uno Changed',
                is_active=False,
                the_type=CONST.AUTOMATION_TYPE_LOCATION,
                sub_type=CONST.AUTOMATION_SUBTYPE_ENTERING_HOME) + ',' + \
            AUTOMATION.get_response_ok(
                aid=2,
                name='Test Automation Dos Changed',
                is_active=False,
                the_type=CONST.AUTOMATION_TYPE_STATUS) + ',' + \
            AUTOMATION.get_response_ok(
                aid=3,
                name='Test Automation Tres New',
                is_active=True,
                the_type=CONST.AUTOMATION_TYPE_SCHEDULE) + ']'

        automation_json_changed = json.loads(automation_text)

        m.get(CONST.AUTOMATION_URL, text=automation_text)

        # Update
        automations_changed = self.abode.get_automations(refresh=True)
        self.assertEqual(len(automations_changed), 3)

        # Check that the original two automations have updated
        # and are using the same class
        automation_1_changed = self.abode.get_automation(1)
        self.assertIsNotNone(automation_1_changed)
        self.assertEqual(automation_1_changed._automation,
                         automation_json_changed[0])
        self.assertIs(automation_1, automation_1_changed)

        automation_2_changed = self.abode.get_automation(2)
        self.assertIsNotNone(automation_2_changed)
        self.assertEqual(automation_2_changed._automation,
                         automation_json_changed[1])
        self.assertIs(automation_2, automation_2_changed)

        # Check that the third new automation is correct
        automation_3 = self.abode.get_automation(3)
        self.assertIsNotNone(automation_3)
        self.assertEqual(automation_3._automation, automation_json_changed[2])

    @requests_mock.mock()
    def tests_automation_set_active(self, m):
        """Check that automations can change their active state."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        # Set up automation
        automation_text = '[' + \
            AUTOMATION.get_response_ok(
                aid=1,
                name='Test Automation Uno',
                is_active=True,
                the_type=CONST.AUTOMATION_TYPE_LOCATION,
                sub_type=CONST.AUTOMATION_SUBTYPE_ENTERING_HOME) + ']'

        automation_json = json.loads(automation_text)

        m.get(CONST.AUTOMATION_URL, text=automation_text)

        # Logout to reset everything
        self.abode.logout()

        # Get the automation and test
        # pylint: disable=W0212
        automation = self.abode.get_automation(1)
        self.assertIsNotNone(automation)
        self.assertEqual(automation._automation, automation_json[0])
        self.assertTrue(automation.is_active)

        # Set up our active state change and URL
        set_active_url = str.replace(CONST.AUTOMATION_EDIT_URL,
                                     '$AUTOMATIONID$',
                                     str(automation_json[0]['id']))
        m.put(set_active_url,
              text=AUTOMATION.get_response_ok(
                  aid=1,
                  name='Test Automation Uno',
                  is_active=False,
                  the_type=CONST.AUTOMATION_TYPE_LOCATION,
                  sub_type=CONST.AUTOMATION_SUBTYPE_ENTERING_HOME))

        # Test the changed state
        automation.set_active(False)
        self.assertFalse(automation.is_active)

        # Change the state back, this time with an array response
        m.put(set_active_url,
              text='[' + AUTOMATION.get_response_ok(
                  aid=1,
                  name='Test Automation Uno',
                  is_active=True,
                  the_type=CONST.AUTOMATION_TYPE_LOCATION,
                  sub_type=CONST.AUTOMATION_SUBTYPE_ENTERING_HOME) + ']')

        # Test the changed state
        automation.set_active(True)
        self.assertTrue(automation.is_active)

        # Test that the response returns the wrong state
        m.put(set_active_url,
              text='[' + AUTOMATION.get_response_ok(
                  aid=1,
                  name='Test Automation Uno',
                  is_active=True,
                  the_type=CONST.AUTOMATION_TYPE_LOCATION,
                  sub_type=CONST.AUTOMATION_SUBTYPE_ENTERING_HOME) + ']')

        with self.assertRaises(abodepy.AbodeException):
            automation.set_active(False)

        # Test that the response returns the wrong id
        m.put(set_active_url,
              text='[' + AUTOMATION.get_response_ok(
                  aid=2,
                  name='Test Automation Uno',
                  is_active=True,
                  the_type=CONST.AUTOMATION_TYPE_LOCATION,
                  sub_type=CONST.AUTOMATION_SUBTYPE_ENTERING_HOME) + ']')

        with self.assertRaises(abodepy.AbodeException):
            automation.set_active(True)

    @requests_mock.mock()
    def tests_automation_trigger(self, m):
        """Check that automations can be triggered."""
        # Set up URL's
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

        m.get(CONST.AUTOMATION_URL, text=automation_text)

        # Logout to reset everything
        self.abode.logout()

        # Get the automation and test
        # pylint: disable=W0212
        automation = self.abode.get_automation(1)
        self.assertIsNotNone(automation)

        # Test that non-quick-actions will throw an exception
        self.assertFalse(automation.is_quick_action)

        with self.assertRaises(abodepy.AbodeException):
            automation.trigger()

        # Set up our quick action reply
        set_active_url = str.replace(CONST.AUTOMATION_APPLY_URL,
                                     '$AUTOMATIONID$',
                                     automation.automation_id)
        m.put(set_active_url, text=MOCK.generic_response_ok())

        # Test triggering
        self.assertTrue(automation.trigger(only_manual=False))

    @requests_mock.mock()
    def tests_automation_filtering(self, m):
        """Check that automations can be filtered by generic type."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok())

        # Set up automations
        automation_text = '[' + \
            AUTOMATION.get_response_ok(
                aid=1,
                name='Test Automation Uno',
                is_active=False,
                the_type=CONST.AUTOMATION_TYPE_LOCATION,
                sub_type=CONST.AUTOMATION_SUBTYPE_ENTERING_HOME) + ',' + \
            AUTOMATION.get_response_ok(
                aid=2,
                name='Test Automation Dos',
                is_active=True,
                the_type=CONST.AUTOMATION_TYPE_MANUAL) + ']'

        automation_json = json.loads(automation_text)

        m.get(CONST.AUTOMATION_URL, text=automation_text)

        # Logout to reset everything
        self.abode.logout()

        # Get the automation and test
        automations = self.abode.get_automations(
            generic_type=CONST.TYPE_AUTOMATION)

        quick_actions = self.abode.get_automations(
            generic_type=CONST.TYPE_QUICK_ACTION)

        # Tests
        self.assertTrue(len(automations), 1)
        self.assertTrue(len(quick_actions), 1)

        # pylint: disable=W0212
        self.assertEqual(automations[0]._automation, automation_json[0])
        self.assertEqual(quick_actions[0]._automation, automation_json[1])
