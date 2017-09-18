"""Abode cloud push events."""
import collections
import logging
import threading
import time

from socketIO_client import SocketIO, LoggingNamespace
from socketIO_client.exceptions import SocketIOError

from abodepy.devices import AbodeDevice
from abodepy.exceptions import AbodeException
import abodepy.helpers.constants as CONST
import abodepy.helpers.errors as ERROR
import abodepy.helpers.timeline as TIMELINE
from urllib3.exceptions import HTTPError

_LOGGER = logging.getLogger(__name__)


class AbodeEventController(object):
    """Class for subscribing to abode events."""

    def __init__(self, abode):
        """Init event subscription class."""
        self._abode = abode
        self._thread = None
        self._socketio = None
        self._running = False

        # Setup callback dicts
        self._device_callbacks = collections.defaultdict(list)
        self._event_callbacks = collections.defaultdict(list)
        self._timeline_callbacks = collections.defaultdict(list)

        # Default "sane" values
        self._ping_interval = 25.0
        self._ping_timeout = 60.0
        self._last_pong = None

    def start(self):
        """Start a thread to handle Abode blocked SocketIO notifications."""
        if not self._thread:
            _LOGGER.info("Starting SocketIO thread...")

            self._thread = threading.Thread(target=self._run_socketio_thread,
                                            name='SocketIOThread')
            self._thread.deamon = True
            self._thread.start()

    def stop(self):
        """Tell the subscription thread to terminate."""
        if self._thread:
            _LOGGER.info("Stopping SocketIO thread...")

            # pylint: disable=W0212
            self._running = False

            if self._socketio:
                self._socketio.disconnect()

    def join(self):
        """Don't allow the main thread to terminate until we have."""
        self._thread.join()

    def add_device_callback(self, devices, callback):
        """Register a device callback."""
        if not devices:
            return False

        if not isinstance(devices, (tuple, list)):
            devices = [devices]

        for device in devices:
            # Device may be a device_id
            device_id = device

            # If they gave us an actual device, get that devices ID
            if isinstance(device, AbodeDevice):
                device_id = device.device_id

            # Validate the device is valid
            if not self._abode.get_device(device_id):
                raise AbodeException((ERROR.EVENT_DEVICE_INVALID))

            _LOGGER.debug(
                "Subscribing to updated for device_id: %s", device_id)

            self._device_callbacks[device_id].append((callback))

        return True

    def add_event_callback(self, event_groups, callback):
        """Register callback for a group of timeline events."""
        if not event_groups:
            return False

        if not isinstance(event_groups, (tuple, list)):
            event_groups = [event_groups]

        for event_group in event_groups:
            if event_group not in TIMELINE.ALL_EVENT_GROUPS:
                raise AbodeException(ERROR.EVENT_GROUP_INVALID,
                                     TIMELINE.ALL_EVENT_GROUPS)

            _LOGGER.debug("Subscribing to event group: %s", event_group)

            self._event_callbacks[event_group].append((callback))

        return True

    def add_timeline_callback(self, timeline_events, callback):
        """Register a callback for a specific timeline event."""
        if not timeline_events:
            return False

        if not isinstance(timeline_events, (tuple, list)):
            timeline_events = [timeline_events]

        for timeline_event in timeline_events:
            if not isinstance(timeline_event, dict):
                raise AbodeException((ERROR.EVENT_CODE_MISSING))

            event_code = timeline_event.get('event_code')

            if not event_code:
                raise AbodeException((ERROR.EVENT_CODE_MISSING))

            _LOGGER.debug("Subscribing to timeline event: %s", timeline_event)

            self._timeline_callbacks[event_code].append((callback))

        return True

    def _on_device_update(self, devid):
        """Device callback from Abode SocketIO server."""
        if devid is None:
            _LOGGER.warning("Device update with no device id.")
            return

        _LOGGER.debug("Device update event for device ID: %s", devid)

        device = self._abode.get_device(devid, True)

        if not device:
            _LOGGER.warning("Got device update for unknown device: %s", devid)
            return

        for callback in self._device_callbacks.get(device.device_id, ()):
            _execute_callback(callback, device)

    def _on_mode_change(self, mode):
        """Mode change broadcast from Abode SocketIO server."""
        if mode is None:
            _LOGGER.warning("Mode change event with no mode.")
            return

        if not mode or mode.lower() not in CONST.ALL_MODES:
            _LOGGER.warning("Mode change event with unknown mode: %s", mode)
            return

        _LOGGER.debug("Alarm mode change event to: %s", mode)

        # We're just going to convert it to an Alarm device
        alarm_device = self._abode.get_alarm(refresh=True)

        # At the time of development, refreshing after mode change notification
        # didn't seem to get the latest update immediately. As such, we will
        # force the mode status now to match the notification.
        # pylint: disable=W0212
        alarm_device._json_state['mode']['area_1'] = mode

        for callback in self._device_callbacks.get(alarm_device.device_id, ()):
            _execute_callback(callback, alarm_device)

    def _on_timeline_update(self, event):
        """Timeline update broadcast from Abode SocketIO server."""
        event_type = event.get('event_type')
        event_code = event.get('event_code')

        if not event_type or not event_code:
            _LOGGER.warning("Invalid timeline update event: %s", event)
            return

        _LOGGER.debug("Timeline event received: %s - %s (%s)",
                      event.get('event_name'), event_type, event_code)

        # Compress our callbacks into those that match this event_code
        # or ones registered to get callbacks for all events
        codes = (event_code, TIMELINE.ALL['event_code'])
        all_callbacks = [self._timeline_callbacks[code] for code in codes]

        for callbacks in all_callbacks:
            for callback in callbacks:
                _execute_callback(callback, event)

        # Attempt to map the event code to a group and callback
        event_group = TIMELINE.map_event_code(event_code)

        if event_group:
            for callback in self._event_callbacks.get(event_group, ()):
                _execute_callback(callback, event)

    def _on_automation_update(self, event):
        """Automation update broadcast from Abode SocketIO server."""
        event_group = TIMELINE.AUTOMATION_EDIT_GROUP

        for callback in self._event_callbacks.get(event_group, ()):
            _execute_callback(callback, event)

    def _on_socket_connect(self, socket):
        # We will try to see what our ping check should be. It does use
        # _variables, so we'll have a fallback value
        # pylint: disable=W0212
        interval = socket._engineIO_session.ping_interval
        if interval > 0:
            self._ping_interval = interval

        timeout = socket._engineIO_session.ping_timeout
        if timeout > 0:
            self._ping_timeout = timeout

        self._last_pong = time.time()

        _LOGGER.info("Connected to Abode SocketIO server")

    def _on_socket_pong(self, _data):
        self._last_pong = time.time()

    def _on_message(self, _data):
        self._last_pong = time.time()

    def _get_socket_io(self, url=CONST.SOCKETIO_URL, port=443):
        # pylint: disable=W0212
        socketio = SocketIO(
            url, port, headers=CONST.SOCKETIO_HEADERS,
            cookies=self._abode._get_session().cookies.get_dict(),
            namespace=LoggingNamespace, wait_for_connection=False)

        socketio.on('connect', lambda: self._on_socket_connect(socketio))
        socketio.on('pong', self._on_socket_pong)
        socketio.on('message', self._on_message)

        socketio.on(CONST.DEVICE_UPDATE_EVENT, self._on_device_update)
        socketio.on(CONST.GATEWAY_MODE_EVENT, self._on_mode_change)
        socketio.on(CONST.TIMELINE_EVENT, self._on_timeline_update)
        socketio.on(CONST.AUTOMATION_EVENT, self._on_automation_update)

        return socketio

    def _clear_internal_socketio(self):
        if self._socketio:
            try:
                self._socketio.off('connect')
                self._socketio.off('pong')
                self._socketio.off('message')
                self._socketio.off(CONST.DEVICE_UPDATE_EVENT)
                self._socketio.off(CONST.GATEWAY_MODE_EVENT)
                self._socketio.off(CONST.TIMELINE_EVENT)
                self._socketio.off(CONST.AUTOMATION_EVENT)
                self._socketio.disconnect()
            # pylint: disable=w0703
            except Exception as exc:
                _LOGGER.warning(
                    "Caught exception clearing SocketIO object: " + str(exc))

    def _run_socketio_thread(self):
        self._running = True

        while self._running:
            try:
                _LOGGER.info(
                    "Attempting to connect to Abode SocketIO server...")

                with self._get_socket_io() as socketio:
                    self._clear_internal_socketio()
                    self._socketio = socketio

                    while self._running:
                        # We need to wait for at least our ping interval,
                        # otherwise the wait will trigger a ping itself.
                        socketio.wait(seconds=self._ping_timeout)

                        # Check that we have gotten pongs or data sometime in
                        # the last XX seconds. If not, we are going to assume
                        # we need to reconnect
                        now = time.time()
                        diff = int(now - (self._last_pong or now))

                        if diff > self._ping_interval:
                            _LOGGER.info(
                                "SocketIO server timeout (%s seconds)",
                                str(self._ping_interval))
                            break
            except SocketIOError as exc:
                _LOGGER.info(
                    "SocketIO error: " + str(exc))
                time.sleep(5)
            except ConnectionError as exc:
                _LOGGER.info("Connection error: " + str(exc))
                time.sleep(5)
            except HTTPError as exc:
                _LOGGER.info("HTTP error: " + str(exc))
                time.sleep(5)
            except OSError as exc:
                _LOGGER.info("OS error: " + str(exc))
                time.sleep(5)
            except Exception as exc:
                _LOGGER.warning(
                    "Unknown exception in SocketIO thread: " + str(exc))
                self._running = False
                raise
            finally:
                _LOGGER.info("Attempting to reconnect...")
                self._clear_internal_socketio()

        _LOGGER.info("Disconnected from Abode SocketIO server")


def _execute_callback(callback, *args, **kwargs):
    # Callback with some data, capturing any exceptions to prevent chaos
    try:
        callback(*args, **kwargs)
    # pylint: disable=W0703
    except Exception as exc:
        _LOGGER.warning("Captured exception during callback: %s", exc)
