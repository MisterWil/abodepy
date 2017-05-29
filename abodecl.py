#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
abodecl by Wil Schrader - An Abode alarm Python library command line interface.
https://github.com/MisterWil/abodepy

Published under the MIT license - See LICENSE file for more details.
"Blink Wire-Free HS Home Monitoring & Alert Systems" is a trademark
owned by Immedia Inc., see www.blinkforhome.com for more information.
I am in no way affiliated with Blink, nor Immedia Inc.
"""

import sys
import argparse
import time
import abodepy

from helpers.constants import (ALL_MODES, ALL_MODES_STR)

PARSER = argparse.ArgumentParser()

PARSER.add_argument('--username', help='Username', required=True)
PARSER.add_argument('--password', help='Password', required=True)
PARSER.add_argument('--mode', help='Output Alarm Mode',
                    required=False, default=False, action="store_true")
PARSER.add_argument('--arm', help='Arm Alarm To Mode', required=False)
PARSER.add_argument('--devices', help='List All Devices',
                    required=False, default=False, action="store_true")
PARSER.add_argument('--device', help='Get Device', required=False, action='append')
PARSER.add_argument('--listen', help='Listen For Device Updates',
                    required=False, default=False, action="store_true")
PARSER.add_argument('--debug', help='Output Debugging',
                    required=False, default=False, action="store_true")

ARGS = vars(PARSER.parse_args())

# Validate arm mode.
if ARGS['arm'] is not None:
    ARGS['arm'] = ARGS['arm'].lower()
    if ARGS['arm'] not in ALL_MODES:
        sys.exit("Arm mode must be one of %s" % ALL_MODES_STR)

# Create abodepy instance.
ABODE = abodepy.Abode(username=ARGS['username'], password=ARGS['password'],
                      get_devices=True, debug=ARGS['debug'])

# Output current mode.
if ARGS['mode']:
    print("Mode: %s" % ABODE.get_alarm().get_mode())

# Change system mode.
if ARGS['arm']:
    print("Mode set to: %s" % ABODE.get_alarm().set_mode(ARGS['arm']))

def _device_print(dev, append=''):
    print("Device Name: %s, Device ID: %s, Device Type: %s, Device Status: %s%s" % (
                dev.get_name(), dev.get_device_id(),
                dev.get_type(), dev.get_status(),
                append))

# Print out all devices.
if ARGS['devices']:
    for device in ABODE.get_devices():
        _device_print(device)

# Print out specific devices by device id.
if ARGS['device']:
    for device_id in ARGS['device']:
        device = ABODE.get_device(device_id)

        if device:
            _device_print(device)

            # Register the specific devices if we decide to listen.
            ABODE.register(device, _device_callback)
        else:
            print("Could not find device with id: %s" % device_id)

def _device_callback(dev):
    _device_print(dev, ", At: " + time.strftime("%Y-%m-%d %H:%M:%S"))

# Start device change listener.
if ARGS['listen']:
    # If no devices were specified then we listen to all devices.
    if ARGS['device'] is None:
        print("No devices specified, adding all devices to listener...")

        for device in ABODE.get_devices():
            ABODE.register(device, _device_callback)

    print("Listening for device updates...")
    ABODE.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ABODE.stop()
        print("Device update listening stopped.")

ABODE.logout()
