#!/usr/bin/python
"""
abodecl by Wil Schrader - An Abode alarm Python library command line interface.

https://github.com/MisterWil/abodepy

Published under the MIT license - See LICENSE file for more details.

"Abode" is a trademark owned by Abode Systems Inc., see www.goabode.com for
more information. I am in no way affiliated with Abode.

Thank you Abode for having a relatively simple API to reverse engineer.
Hopefully in the future you'll open it up for official use.

API calls faster than 60 seconds is not recommended as it can overwhelm
Abode's servers. Leverage the cloud push event notification functionality as
much as possible. Please use this module responsibly.
"""

import logging
import time

import argparse

import abodepy

_LOGGER = logging.getLogger('abodecl')


def setup_logging(log_level=logging.INFO):
    """Set up the logging."""
    logging.basicConfig(level=log_level)
    fmt = ("%(asctime)s %(levelname)s (%(threadName)s) "
           "[%(name)s] %(message)s")
    colorfmt = "%(log_color)s{}%(reset)s".format(fmt)
    datefmt = '%Y-%m-%d %H:%M:%S'

    # Suppress overly verbose logs from libraries that aren't helpful
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('aiohttp.access').setLevel(logging.WARNING)

    try:
        from colorlog import ColoredFormatter
        logging.getLogger().handlers[0].setFormatter(ColoredFormatter(
            colorfmt,
            datefmt=datefmt,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            }
        ))
    except ImportError:
        pass

    logger = logging.getLogger('')
    logger.setLevel(log_level)


def get_arguments():
    """Get parsed arguments."""
    parser = argparse.ArgumentParser("AbodePy: Command Line Utility")

    parser.add_argument(
        '-u', '--username',
        help='Username',
        required=True)

    parser.add_argument(
        '-p', '--password',
        help='Password',
        required=True)

    parser.add_argument(
        '--mode',
        help='Output current alarm mode',
        required=False, default=False,
        action="store_true")

    parser.add_argument(
        '--arm',
        metavar='mode',
        help='Arm alarm to mode',
        required=False)

    parser.add_argument(
        '--set',
        metavar='setting=value',
        help='Set setting to a value',
        required=False, action='append')

    parser.add_argument(
        '--devices',
        help='Output all devices',
        required=False, default=False, action="store_true")

    parser.add_argument(
        '--device',
        metavar='device_id',
        help='Output one device for device_id',
        required=False, action='append')

    parser.add_argument(
        '--on',
        metavar='device_id',
        help='Switch on a given device_id',
        required=False, action='append')

    parser.add_argument(
        '--off',
        metavar='device_id',
        help='Switch off a given device_id',
        required=False, action='append')

    parser.add_argument(
        '--lock',
        metavar='device_id',
        help='Lock a given device_id',
        required=False, action='append')

    parser.add_argument(
        '--unlock',
        metavar='device_id',
        help='Unlock a given device_id',
        required=False, action='append')

    parser.add_argument(
        '--listen',
        help='Block and listen for device_id',
        required=False, default=False, action="store_true")

    parser.add_argument(
        '--debug',
        help='Enable debug logging',
        required=False, default=False, action="store_true")

    parser.add_argument(
        '--quiet',
        help='Output only warnings and errors',
        required=False, default=False, action="store_true")

    return parser.parse_args()


def call():
    """Execute command line helper."""
    args = get_arguments()

    # Set up logging
    if args.debug:
        log_level = logging.DEBUG
    elif args.quiet:
        log_level = logging.WARN
    else:
        log_level = logging.INFO

    setup_logging(log_level)

    abode = None

    try:
        # Create abodepy instance.
        abode = abodepy.Abode(username=args.username,
                              password=args.password,
                              get_devices=True)

        # Output current mode.
        if args.mode:
            _LOGGER.info("Current alarm mode: %s", abode.get_alarm().mode)

        # Change system mode.
        if args.arm:
            if abode.get_alarm().set_mode(args.arm):
                _LOGGER.info("Alarm mode changed to: %s", args.arm)
            else:
                _LOGGER.warning("Failed to change alarm mode to: %s", args.arm)

        # Set setting
        for setting in args.set or []:
            keyval = setting.split("=")
            if abode.set_setting(keyval[0], keyval[1]):
                _LOGGER.info("Setting %s changed to %s", keyval[0], keyval[1])

        # Switch on
        for device_id in args.on or []:
            device = abode.get_device(device_id)

            if device:
                if device.switch_on():
                    _LOGGER.info("Switched on device with id: %s", device_id)
            else:
                _LOGGER.warning("Could not find device with id: %s", device_id)

        # Switch off
        for device_id in args.off or []:
            device = abode.get_device(device_id)

            if device:
                if device.switch_off():
                    _LOGGER.info("Switched off device with id: %s", device_id)
            else:
                _LOGGER.warning("Could not find device with id: %s", device_id)

        # Lock
        for device_id in args.lock or []:
            device = abode.get_device(device_id)

            if device:
                if device.lock():
                    _LOGGER.info("Locked device with id: %s", device_id)
            else:
                _LOGGER.warning("Could not find device with id: %s", device_id)

        # Unlock
        for device_id in args.unlock or []:
            device = abode.get_device(device_id)

            if device:
                if device.unlock():
                    _LOGGER.info("Unlocked device with id: %s", device_id)
            else:
                _LOGGER.warning("Could not find device with id: %s", device_id)

        # Print
        def _device_print(dev, append=''):
            _LOGGER.info("Device Name: %s, ID: %s, Type: %s, Status: %s%s",
                         dev.name, dev.device_id, dev.type, dev.status, append)

        # Print out all devices.
        if args.devices:
            for device in abode.get_devices():
                _device_print(device)

        def _device_callback(dev):
            _device_print(dev, ", At: " + time.strftime("%Y-%m-%d %H:%M:%S"))

        # Print out specific devices by device id.
        if args.device:
            for device_id in args.device:
                device = abode.get_device(device_id)

                if device:
                    _device_print(device)

                    # Register the specific devices if we decide to listen.
                    abode.register(device, _device_callback)
                else:
                    _LOGGER.warning(
                        "Could not find device with id: %s", device_id)

        # Start device change listener.
        if args.listen:
            # If no devices were specified then we listen to all devices.
            if args.device is None:
                _LOGGER.info("Adding all devices to listener...")

                for device in abode.get_devices():
                    abode.register(device, _device_callback)

            _LOGGER.info("Listening for device updates...")
            abode.start_listener()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                abode.stop_listener()
                _LOGGER.info("Device update listening stopped.")
    except abodepy.AbodeException as exc:
        _LOGGER.error(exc)
    finally:
        if abode:
            abode.logout()


def main():
    """Execute from command line."""
    call()


if __name__ == '__main__':
    main()
