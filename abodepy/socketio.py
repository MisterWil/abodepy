"""Small SocketIO client via Websockets."""
from lomond import WebSocket
from lomond import events
from lomond.persist import persist
import json
from datetime import datetime
import threading

PACKET_OPEN = "0"
PACKET_CLOSE = "1"
PACKET_PING = "2"
PACKET_PONG = "3"
PACKET_MESSAGE = "4"

MESSAGE_CONNECT = "0"
MESSAGE_DISCONNECT = "1"
MESSAGE_EVENT = "2"
MESSAGE_ERROR = "4"

PING_INTERVAL = "pingInterval"
PING_TIMEOUT = "pingTimeout"

COOKIE_HEADER = str.encode("Cookie")
ORIGIN_HEADER = str.encode("Origin")

URL_PARAMS = "?EIO=3&transport=websocket"

_LOGGER = logging.getLogger(__name__)

class SocketIO(object):
    """Class for using websockets to talk to a SocketIO server."""

    def __init__(self, url, cookie=None, origin=None):
        """Init socketio class."""

        self._url = url + URL_PARAMS

        if origin:
            self._origin = origin.encode()
        else
            self._origin = None

        if cookie:
            self._cookie = cookie.encode()
        else:
            self._cookie = None

        self._thread = None
        self._websocket = None
        self._running = False

        self._websocket_connected = False
        self._engineio_connected = False
        self._socketio_connected = False

        self._ping_interval_ms = 25000
        self._ping_timeout_ms = 60000

        self._last_ping_time = datetime.min
        self._last_packet_time = datetime.min

        self._callbacks = collections.defaultdict(list)

    def set_cookie(self, cookie=None):
        if cookie:
            self._cookie = cookie.encode()
        else:
            self._cookie = None

    def on(self, event_name, callback):
        """Register callback for a SocketIO event."""
        if not event_name:
            return False

        _LOGGER.debug("Adding callback for event name: %s", event_name)

        self._callbacks[event_name].append((callback))

        return True

    def start(self):
        """Start a thread to handle SocketIO notifications."""
        if not self._thread:
            _LOGGER.info("Starting SocketIO thread...")

            self._thread = threading.Thread(target=self._run_socketio_thread,
                                            name='SocketIOThread')
            self._thread.deamon = True
            self._thread.start()

    def stop(self):
        """Tell the SocketIO thread to terminate."""
        if self._thread:
            _LOGGER.info("Stopping SocketIO thread...")

            # pylint: disable=W0212
            self._running = False

            # Join thread to wait for termination
            self._thread.join()

    def _run_socketio_thread(self):
        self._running = True

        while self._running:
            _LOGGER.info(
                "Attempting to connect to SocketIO server...")

            websocket = WebSocket(self._url)

            if self._cookie:
                websocket.add_header(COOKIE_HEADER, self._cookie)

            if self._origin:
                websocket.add_header(ORIGIN_HEADER, self._origin)

            exit_event = threading.Event()
            for event in persist(websocket, ping_rate=0, poll=5.0, exit_event=exit_event):
                _LOGGER.debug(event)
                
                if isinstance(event, events.Connected):
                    self._on_websocket_connected(websocket, event)
                elif isinstance(event, events.Disconnected):
                    self._on_websocket_disconnected(websocket, event)
                elif isinstance(event, events.Text):
                    self._on_websocket_text(websocket, event)
                elif isinstance(event, events.Poll):
                    self._on_websocket_poll(websocket, event)
                elif isinstance(event, events.BackOff):
                    self._on_websocket_backoff(websocket, event)

                if not self._running:
                    exit_event.set()

    def _on_websocket_connected(self, websocket, event):
        self._websocket_connected = True
        
        _LOGGER.debug("Websocket Connected")
        
    def _on_websocket_disconnected(self, websocket, event):
        self._websocket_connected = False
        self._engineio_connected = False
        self._socketio_connected = False
        
        _LOGGER.debug("Websocket Disconnected")
            
    def _on_websocket_poll(self, websocket, event):
        last_packet_delta = datetime.now() - self._last_packet_time
        last_packet_ms = int(last_packet_delta.total_seconds() * 1000)
        
        if self._engineio_connected and last_packet_ms > self._ping_timeout_ms:
            _LOGGER.warning("SocketIO Server Ping Timeout")
            websocket.close()
            return
            
        last_ping_delta = datetime.now() - self._last_ping_time
        last_ping_ms = int(last_ping_delta.total_seconds() * 1000)
        
        if self._engineio_connected and last_ping_ms >= self._ping_interval_ms:
            websocket.send_text(PACKET_PING)
            last_ping_time = datetime.now()
            _LOGGER.debug("Client Ping!")

    def _on_websocket_text(self, websocket, event):
        self._last_packet_time = datetime.now()
        
        packet_type = event.text[:1]
        packet_data = event.text[1:]
        
        if packet_type == PACKET_OPEN:
            self._on_engineio_opened(websocket, packet_data)
        elif packet_type == PACKET_CLOSE:
            self._on_engineio_closed(websocket)
        elif packet_type == PACKET_PONG:
            self._on_engineio_pong(websocket)
        elif packet_type == PACKET_MESSAGE:
            self._on_engineio_message(websocket, packet_data)
        else:
            _LOGGER.debug("Ignoring EngineIO packet: %s" % text)

    def _on_engineio_opened(self, websocket, packet_data):
        json_data = json.loads(packet_data)
        
        if json_data and json_data[PING_INTERVAL]:
            ping_interval_ms = json_data[PING_INTERVAL]
            _LOGGER.debug("Set ping interval to: %d" % ping_interval_ms)
            
        if json_data and json_data[PING_TIMEOUT]:
            ping_timeout_ms = json_data[PING_TIMEOUT]
            _LOGGER.debug("Set ping timeout to: %d" % ping_timeout_ms)

        self._engineio_connected = True
        
        _LOGGER.debug("EngineIO Connected")
        
    def _on_engineio_closed(self, websocket):
        self._engineio_connected = False
        
        _LOGGER.debug("EngineIO Disconnected")
        
        websocket.close()
        
    def _on_engineio_pong(self, websocket):
        _LOGGER.debug("Server Pong!")

    def _on_engineio_message(self, websocket, packet_data):
        message_type = packet_data[:1]
        message_data = packet_data[1:]
        
        if message_type == MESSAGE_CONNECT:
            self._on_socketio_connected()
        elif message_type == MESSAGE_DISCONNECT:
            self._on_socketio_disconnected(websocket)
        elif message_type == MESSAGE_ERROR:
            self._on_socketio_error(websocket, message_data)
        elif message_type == MESSAGE_EVENT:
            self._on_socketio_event(message_data)
        else:
            _LOGGER.debug("Ignoring SocketIO message: %s" % packet_data)

    def _on_socketio_connected(self):
        self._socketio_connected = True
        
        _LOGGER.debug("SocketIO Connected")
        
    def _on_socketio_disconnected(self, websocket):
        self._socketio_connected = False
        
        _LOGGER.debug("SocketIO Disconnected")
        
        websocket.close()
        
    def _on_socketio_error(self, websocket, message_data):
        raise Error("SocketIO Error: %s" % message_data)
            
    def _on_socketio_event(self, message_data):
        l_bracket = message_data.find("[")
        r_bracket = message_data.rfind("]")
        
        if l_bracket == -1 or r_bracket == -1:
            _LOGGER.warning("Unable to find event [data]: %s" % message_data)
            return
        
        json_str = message_data[l_bracket:r_bracket+1]
        json_data = json.loads(json_str)
        
        self._handle_event(json_data[0], json_data[1:])

    def _handle_event(self, event_name, event_data):
        for callback in self._callbacks.get(event_name, ()):
             try:
                callback(*args, **kwargs)
            # pylint: disable=W0703
            except Exception as exc:
                _LOGGER.warning("Captured exception during SocketIO event callback: %s", exc)