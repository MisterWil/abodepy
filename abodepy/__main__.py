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
import json
import logging
import time

import argparse

import abodepy
import abodepy.helpers.timeline as TIMELINE
from abodepy.exceptions import AbodeException

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
        required=False)

    parser.add_argument(
        '-p', '--password',
        help='Password',
        required=False)

    parser.add_argument(
        '--mfa',
        help='Multifactor authentication code',
        required=False)

    parser.add_argument(
        '--cache',
        metavar='pickle_file',
        help='Create/update/use a pickle cache for the username and password.',
        required=False)

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
        '--json',
        metavar='device_id',
        help='Output the json for device_id',
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
        '--automations',
        help='Output all automations',
        required=False, default=False, action="store_true")

    parser.add_argument(
        '--activate',
        metavar='automation_id',
        help='Activate (enable) an automation by automation_id',
        required=False, action='append')

    parser.add_argument(
        '--deactivate',
        metavar='automation_id',
        help='Deactivate (disable) an automation by automation_id',
        required=False, action='append')

    parser.add_argument(
        '--trigger',
        metavar='automation_id',
        help='Trigger (apply) a manual (quick) automation by automation_id',
        required=False, action='append')

    parser.add_argument(
        '--capture',
        metavar='device_id',
        help='Trigger a new image capture for the given device_id',
        required=False, action='append')

    parser.add_argument(
        '--image',
        metavar='device_id=location/image.jpg',
        help='Save an image from a camera (if available) to the given path',
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

    if not args.cache:
        if not args.username or not args.password:
            raise Exception("Please supply a cache or username and password.")

    try:
        # Create abodepy instance.
        if args.cache and args.username and args.password:
            abode = abodepy.Abode(username=args.username,
                                  password=args.password,
                                  get_devices=args.mfa is None,
                                  cache_path=args.cache)
        elif args.cache and not (not args.username or not args.password):
            abode = abodepy.Abode(get_devices=args.mfa is None,
                                  cache_path=args.cache)
        else:
            abode = abodepy.Abode(username=args.username,
                                  password=args.password,
                                  get_devices=args.mfa is None)

        # Since the MFA code is very time sensitive, if the user has provided
        # one we should use it to log in as soon as possible
        if args.mfa:
            abode.login(mfa_code=args.mfa)
            # Now we can fetch devices from Abode
            abode.get_devices()

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

        # Output Json
        for device_id in args.json or []:
            device = abode.get_device(device_id)

            if device:
                # pylint: disable=protected-access
                print(json.dumps(device._json_state, sort_keys=True,
                                 indent=4, separators=(',', ': ')))
            else:
                _LOGGER.warning("Could not find device with id: %s", device_id)

        # Print
        def _device_print(dev, append=''):
            print("%s%s",
                  dev.desc, append)

        # Print out all automations
        if args.automations:
            for automation in abode.get_automations():
                _device_print(automation)

        # Enable automation
        for automation_id in args.activate or []:
            automation = abode.get_automation(automation_id)

            if automation:
                if automation.set_active(True):
                    _LOGGER.info(
                        "Activated automation with id: %s", automation_id)
            else:
                _LOGGER.warning(
                    "Could not find automation with id: %s", automation_id)

        # Disable automation
        for automation_id in args.deactivate or []:
            automation = abode.get_automation(automation_id)

            if automation:
                if automation.set_active(False):
                    _LOGGER.info(
                        "Deactivated automation with id: %s", automation_id)
            else:
                _LOGGER.warning(
                    "Could not find automation with id: %s", automation_id)

        # Trigger automation
        for automation_id in args.trigger or []:
            automation = abode.get_automation(automation_id)

            if automation:
                if automation.trigger():
                    _LOGGER.info(
                        "Triggered automation with id: %s", automation_id)
            else:
                _LOGGER.warning(
                    "Could not find automation with id: %s", automation_id)

        # Trigger image capture
        for device_id in args.capture or []:
            device = abode.get_device(device_id)

            if device:
                if device.capture():
                    _LOGGER.info(
                        "Image requested from device with id: %s", device_id)
                else:
                    _LOGGER.warning(
                        "Failed to request image from device with id: %s",
                        device_id)
            else:
                _LOGGER.warning("Could not find device with id: %s", device_id)

        # Save camera image
        for keyval in args.image or []:
            devloc = keyval.split("=")
            device = abode.get_device(devloc[0])

            if device:
                try:
                    if (device.refresh_image() and
                            device.image_to_file(devloc[1])):
                        _LOGGER.info(
                            "Saved image to %s for device id: %s", devloc[1],
                            devloc[0])
                except AbodeException as exc:
                    _LOGGER.warning("Unable to save image: %s", exc)
            else:
                _LOGGER.warning(
                    "Could not find device with id: %s", devloc[0])

        # Print out all devices.
        if args.devices:
            for device in abode.get_devices():
                _device_print(device)

        def _device_callback(dev):
            _device_print(dev, ", At: " + time.strftime("%Y-%m-%d %H:%M:%S"))

        def _timeline_callback(tl_json):
            event_code = int(tl_json['event_code'])
            if 5100 <= event_code <= 5199:
                # Ignore device changes
                return

            _LOGGER.info("%s - %s at %s %s",
                         tl_json['event_name'], tl_json['event_type'],
                         tl_json['date'], tl_json['time'])

        # Print out specific devices by device id.
        if args.device:
            for device_id in args.device:
                device = abode.get_device(device_id)

                if device:
                    _device_print(device)

                    # Register the specific devices if we decide to listen.
                    abode.events.add_device_callback(device_id,
                                                     _device_callback)
                else:
                    _LOGGER.warning(
                        "Could not find device with id: %s", device_id)

        # Start device change listener.
        if args.listen:
            # If no devices were specified then we listen to all devices.
            if args.device is None:
                _LOGGER.info("Adding all devices to listener...")

                for device in abode.get_devices():
                    abode.events.add_device_callback(device.device_id,
                                                     _device_callback)

            abode.events.add_timeline_callback(TIMELINE.ALL,
                                               _timeline_callback)

            _LOGGER.info("Listening for device and timeline updates...")
            abode.events.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                abode.events.stop()
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
