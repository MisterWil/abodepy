# """Test the Abode event controller class."""
# import json
# import unittest
# import psutil
# import subprocess
# import time
# from unittest.mock import call, Mock
#
# import requests
# import requests_mock
#
# import abodepy
# import abodepy.helpers.constants as CONST
# import abodepy.helpers.timeline as TIMELINE
# import abodepy.socketio as sio
# from abodepy.devices.binary_sensor import AbodeBinarySensor
#
# import tests.mock.login as LOGIN
# import tests.mock.logout as LOGOUT
# import tests.mock.panel as PANEL
# import tests.mock.devices.secure_barrier as COVER
# import tests.mock.devices.door_contact as DOORCONTACT
# import tests.mock.devices.ir_camera as IRCAMERA
#
#
# USERNAME = 'foobar'
# PASSWORD = 'deadbeef'
#
# SERVER = "http://localhost:3000/"
# SOCKETIO_SERVER = "ws://localhost:3000/"
#
# SHUTDOWN = SERVER + "shutdown"
# EVENTS = SERVER + "events/"
# KILL_SOCKETS = SERVER + "killSockets"
# ENABLE_AUTH_ERROR = SERVER + "authError/true"
# DISABLE_AUTH_ERROR = SERVER + "authError/false"
#
#
# def kill(proc_pid):
#     process = psutil.Process(proc_pid)
#     for proc in process.children(recursive=True):
#         proc.kill()
#     process.kill()
#
#
# class TestEventController(unittest.TestCase):
#     """Test the AbodePy event controller."""
#
#     def setUp(self):
#         """Set up Abode module."""
#         self.abode = abodepy.Abode(username=USERNAME,
#                                    password=PASSWORD,
#                                    event_url=SOCKETIO_SERVER)
#
#         print("Starting proc")
#
#         self.proc = subprocess.Popen(["node", "./tests/mock_server/index.js"])
#
#         stdoutdata, stderrdata = self.proc.communicate()
#         print(stdoutdata)
#         print(stderrdata)
#
#     def tearDown(self):
#         """Clean up after test."""
#         self.abode = None
#
#         try:
#             requests.post(SHUTDOWN)
#         except Exception as exc:
#             print(exc)
#
#         try:
#             self.proc.wait(timeout=3)
#         except subprocess.TimeoutExpired:
#             kill(self.proc.pid)
#
#     @requests_mock.mock()
#     def test_connect_disconnect(self, m):
#         """Tests that we can connect and disconnect to a SocketIO server."""
# #         # Set up URL's
# #         m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
# #         m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
# #         m.get(CONST.PANEL_URL,
# #               text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
# #         m.get(CONST.DEVICES_URL,
# #               text=COVER.device(devid=COVER.DEVICE_ID,
# #                                 status=CONST.STATUS_CLOSED,
# #                                 low_battery=False,
# #                                 no_response=False))
# #
# #         # Logout to reset everything
# #         self.abode.logout()
#
# #         # Get our device
# #         device = self.abode.get_device(COVER.DEVICE_ID)
# #         self.assertIsNotNone(device)
# #
# #         # Get the event controller
# #         events = self.abode.events
# #         self.assertIsNotNone(events)
# #
# #         # Get the SocketIO server
# #         socketio = self.abode.events.socketio
# #
# #         # Create mock callbacks
# #         connect_callback = Mock()
# #         disconnect_callback = Mock()
# #
# #         # Register the connect and disconnect callbacks
# #         self.assertTrue(
# #             socketio.on(sio.CONNECTED, connect_callback))
# #
# #         self.assertTrue(
# #             socketio.on(sio.DISCONNECTED, disconnect_callback))
# #
# #         # Start event controller
# #         events.start()
# #
# #         # Wait for connection
# #         time.sleep(1)
# #
# #         # Assert Connected
# #         connect_callback.assert_called()
# #
# #         # Shutdown event controller
# #         events.stop()
# #
# #         # Wait for disconnection
# #         time.sleep(1)
# #
# #         # Assert Disconnected
# #         disconnect_callback.assert_called()
