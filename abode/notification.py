import collections
import threading
import logging
import abode

from socketIO_client import SocketIO, LoggingNamespace

logging.basicConfig(level=logging.WARN)

SOCKETIO_URL = 'https://io.goabode.com'

SOCKETIO_HEADERS = {'Origin': 'https://my.goabode.com'}

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

class NotificationRegistry(object):
    """Class for subscribing to abode events."""

    def __init__(self, abode, debug=False):
        """Setup subscription."""
        self._abode = abode;
        self._devices = collections.defaultdict(list)
        self._callbacks = collections.defaultdict(list)
        self._thread = None

        if debug:
            LOG.setLevel(logging.DEBUG)

    def register(self, device, callback):
        """Register a callback.
        device: device to be updated by subscription
        callback: callback for notification of changes
        """
        if not device or not isinstance(device, abode.AbodeDevice):
            LOG.error("Received an invalid device: %s", device)
            return

        LOG.debug("Subscribing to events for device: %s (%s)", device.name, device.device_id)
        self._devices[device.device_id].append(device)
        self._callbacks[device].append((callback))

    def _on_device_update(self, devid):
        if devid is None:
            return

        LOG.debug("Device Update Received: %s", devid)

        device = self._abode.get_device(devid, True)

        for callback in self._callbacks.get(device, ()):
            callback(device)

    def _on_mode_change(self, mode):
        if mode is None:
            return

        if not mode in ('standby', 'home', 'away'):
            LOG.warn("Mode update changed with unknown status: %s" % mode)
            return

        LOG.debug("Device Status Update Received: %s", mode)

        alarm_device = self._abode.get_device('area_1', True)

        for callback in self._callbacks.get(alarm_device, ()):
            callback(alarm_device)

    def join(self):
        """Don't allow the main thread to terminate until we have."""
        self._thread.join()

    def start(self):
        """Start a thread to handle Abode blocked SocketIO notifications."""
        if not self._thread:
            self._thread = threading.Thread(target=self._run_socketio_thread,
                                                 name='Abode SocketIO Thread')
            self._thread.deamon = True
            self._thread.start()
            LOG.debug("Terminated started")

    def stop(self):
        """Tell the subscription thread to terminate."""
        if self._thread:
            self._socketio._close()
            self.join()
            self._thread = None
            LOG.debug("Terminated thread")

    def _run_socketio_thread(self):
        self._socketio = SocketIO(
            SOCKETIO_URL, 443, LoggingNamespace,
            headers=SOCKETIO_HEADERS,
            cookies=self._abode.session.cookies.get_dict())

        self._socketio.on('com.goabode.device.update', self._on_device_update)
        self._socketio.on('com.goabode.gateway.mode', self._on_mode_change)

        LOG.debug("Starting Abode SocketIO Notification Service")

        self._socketio.wait()

        LOG.debug("Shutdown Abode SocketIO Notification Service")
