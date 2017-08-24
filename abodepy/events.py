"""Abode cloud push events."""
import collections
import logging
import threading
import time

from socketIO_client import SocketIO, LoggingNamespace
from socketIO_client.exceptions import SocketIOError

from abodepy.devices.switch import AbodeDevice
from abodepy.exceptions import AbodeException
import abodepy.helpers.constants as CONST
import abodepy.helpers.errors as ERROR

_LOGGER = logging.getLogger(__name__)


class AbodeEvents(object):
    """Class for subscribing to abode events."""

    def __init__(self, abode):
        """Init event subscription class."""
        self._abode = abode
        self._callbacks = collections.defaultdict(list)
        self._thread = None
        self._socketio = None
        self._running = False

        # Default "sane" values
        self._ping_interval = 25.0
        self._ping_timeout = 60.0
        self._last_pong = None

    def register(self, device, callback):
        """Register a callback.

        device: device to be updated by subscription
        callback: callback for notification of changes
        """
        if not device or not isinstance(device, AbodeDevice):
            raise AbodeException(ERROR.EVENT_DEVICE_INVALID)

        _LOGGER.info("Subscribing to events for device: %s (%s)",
                     device.name, device.device_id)

        self._callbacks[device.device_id].append((callback))

        return True

    def _on_device_update(self, devid):
        if devid is None:
            return

        _LOGGER.info("Device update event from device ID: %s", devid)

        device = self._abode.get_device(devid, True)

        for callback in self._callbacks.get(device.device_id, ()):
            callback(device)

    def _on_mode_change(self, mode):
        if mode is None:
            return

        if not mode or mode.lower() not in CONST.ALL_MODES:
            raise AbodeException(ERROR.INVALID_ALARM_MODE)

        _LOGGER.info("Alarm mode change event to: %s", mode)

        alarm_device = self._abode.get_alarm(refresh=True)

        # At the time of development, refreshing after mode change notification
        # didn't seem to get the latest update immediately. As such, we will
        # force the mode status now to match the notification.
        # pylint: disable=W0212
        alarm_device._json_state['mode']['area_1'] = mode

        for callback in self._callbacks.get(alarm_device.device_id, ()):
            callback(alarm_device)

    def join(self):
        """Don't allow the main thread to terminate until we have."""
        self._thread.join()

    def start(self):
        """Start a thread to handle Abode blocked SocketIO notifications."""
        if not self._thread:
            _LOGGER.info("Starting SocketIO thread...")

            self._thread = threading.Thread(target=self._run_socketio_thread,
                                            name='Abode SocketIO Thread')
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

    def _get_socket_io(self, url=CONST.SOCKETIO_URL, port=443):
        # pylint: disable=W0212
        socketio = SocketIO(
            url, port, headers=CONST.SOCKETIO_HEADERS,
            cookies=self._abode._get_session().cookies.get_dict(),
            namespace=LoggingNamespace)

        socketio.on('connect', lambda: self._on_socket_connect(socketio))
        socketio.on('pong', self._on_socket_pong)

        socketio.on(CONST.DEVICE_UPDATE_EVENT, self._on_device_update)
        socketio.on(CONST.GATEWAY_MODE_EVENT, self._on_mode_change)

        return socketio

    def _clear_internal_socketio(self):
        if self._socketio:
            try:
                self._socketio.off('connect')
                self._socketio.off('pong')
                self._socketio.off(CONST.DEVICE_UPDATE_EVENT)
                self._socketio.off(CONST.GATEWAY_MODE_EVENT)
                self._socketio.disconnect()
            except Exception:
                _LOGGER.warning(
                    "Caught exception clearing old SocketIO object...")
                raise

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
                                "SocketIO server timeout, reconnecting...")
                            break
            except SocketIOError:
                _LOGGER.info(
                    "SocketIO server connection error, reconnecting...")
                time.sleep(5)
            except Exception:
                _LOGGER.warning("Caught exception in SocketIO thread...")
                raise
            finally:
                self._clear_internal_socketio()

        _LOGGER.info("Disconnected from Abode SocketIO server")
