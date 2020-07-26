"""Abode cloud push events."""
import collections
import logging

from abodepy.devices import AbodeDevice
from abodepy.exceptions import AbodeException
import abodepy.helpers.constants as CONST
import abodepy.helpers.errors as ERROR
import abodepy.helpers.timeline as TIMELINE
import abodepy.socketio as sio

_LOGGER = logging.getLogger(__name__)


class AbodeEventController():
    """Class for subscribing to abode events."""

    def __init__(self, abode, url=CONST.SOCKETIO_URL):
        """Init event subscription class."""
        self._abode = abode
        self._thread = None
        self._running = False
        self._connected = False

        # Setup callback dicts
        self._connection_status_callbacks = collections.defaultdict(list)
        self._device_callbacks = collections.defaultdict(list)
        self._event_callbacks = collections.defaultdict(list)
        self._timeline_callbacks = collections.defaultdict(list)

        # Setup SocketIO
        self._socketio = sio.SocketIO(url=url,
                                      origin=CONST.BASE_URL)

        # Setup SocketIO Callbacks
        self._socketio.on(sio.STARTED, self._on_socket_started)
        self._socketio.on(sio.CONNECTED, self._on_socket_connected)
        self._socketio.on(sio.DISCONNECTED, self._on_socket_disconnected)
        self._socketio.on(CONST.DEVICE_UPDATE_EVENT, self._on_device_update)
        self._socketio.on(CONST.GATEWAY_MODE_EVENT, self._on_mode_change)
        self._socketio.on(CONST.TIMELINE_EVENT, self._on_timeline_update)
        self._socketio.on(CONST.AUTOMATION_EVENT, self._on_automation_update)

    def start(self):
        """Start a thread to handle Abode SocketIO notifications."""
        self._socketio.start()

    def stop(self):
        """Tell the subscription thread to terminate - will block."""
        self._socketio.stop()

    def add_connection_status_callback(self, unique_id, callback):
        """Register callback for Abode server connection status."""
        if not unique_id:
            return False

        _LOGGER.debug(
            "Subscribing to Abode connection updates for: %s", unique_id)

        self._connection_status_callbacks[unique_id].append((callback))

        return True

    def remove_connection_status_callback(self, unique_id):
        """Unregister connection status callbacks."""
        if not unique_id:
            return False

        _LOGGER.debug(
            "Unsubscribing from Abode connection updates for : %s", unique_id)

        self._connection_status_callbacks[unique_id].clear()

        return True

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
                "Subscribing to updates for device_id: %s", device_id)

            self._device_callbacks[device_id].append((callback))

        return True

    def remove_all_device_callbacks(self, devices):
        """Unregister all callbacks for a device."""
        if not devices:
            return False

        if not isinstance(devices, (tuple, list)):
            devices = [devices]

        for device in devices:
            device_id = device

            if isinstance(device, AbodeDevice):
                device_id = device.device_id

            if not self._abode.get_device(device_id):
                raise AbodeException((ERROR.EVENT_DEVICE_INVALID))

            if device_id not in self._device_callbacks:
                return False

            _LOGGER.debug(
                "Unsubscribing from all updates for device_id: %s", device_id)

            self._device_callbacks[device_id].clear()

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

    @property
    def connected(self):
        """Get the Abode connection status."""
        return self._connected

    @property
    def socketio(self):
        """Get the SocketIO instance."""
        return self._socketio

    def _on_socket_started(self):
        """Socket IO startup callback."""
        # pylint: disable=W0212
        cookies = self._abode._get_session().cookies.get_dict()
        cookie_string = "; ".join(
            [str(x) + "=" + str(y) for x, y in cookies.items()])

        self._socketio.set_cookie(cookie_string)

    def _on_socket_connected(self):
        """Socket IO connected callback."""
        self._connected = True

        try:
            self._abode.refresh()
        # pylint: disable=W0703
        except Exception as exc:
            _LOGGER.warning("Captured exception during Abode refresh: %s", exc)
        finally:
            # Callbacks should still execute even if refresh fails (Abode
            # server issues) so that the entity availability in Home Assistant
            # is updated since we are in fact connected to the web socket.
            for callbacks in self._connection_status_callbacks.items():
                for callback in callbacks[1]:
                    _execute_callback(callback)

    def _on_socket_disconnected(self):
        """Socket IO disconnected callback."""
        self._connected = False

        for callbacks in self._connection_status_callbacks.items():
            # Check if list is not empty.
            # Applicable when remove_all_device_callbacks
            # is called before _on_socket_disconnected.
            if callbacks[1]:
                for callback in callbacks[1]:
                    _execute_callback(callback)

    def _on_device_update(self, devid):
        """Device callback from Abode SocketIO server."""
        if isinstance(devid, (tuple, list)):
            devid = devid[0]

        if devid is None:
            _LOGGER.warning("Device update with no device id.")
            return

        _LOGGER.debug("Device update event for device ID: %s", devid)

        device = self._abode.get_device(devid, True)

        if not device:
            _LOGGER.debug("Got device update for unknown device: %s", devid)
            return

        for callback in self._device_callbacks.get(device.device_id, ()):
            _execute_callback(callback, device)

    def _on_mode_change(self, mode):
        """Mode change broadcast from Abode SocketIO server."""
        if isinstance(mode, (tuple, list)):
            mode = mode[0]

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
        if isinstance(event, (tuple, list)):
            event = event[0]

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

        if isinstance(event, (tuple, list)):
            event = event[0]

        for callback in self._event_callbacks.get(event_group, ()):
            _execute_callback(callback, event)


def _execute_callback(callback, *args, **kwargs):
    # Callback with some data, capturing any exceptions to prevent chaos
    try:
        callback(*args, **kwargs)
    # pylint: disable=W0703
    except Exception as exc:
        _LOGGER.warning("Captured exception during callback: %s", exc)
