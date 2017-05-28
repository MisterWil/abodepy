import argparse
import time
import abodepy

from helpers.constants import (MODE_STANDBY, MODE_HOME, MODE_AWAY,
                               ALL_MODES, ALL_MODES_STR)

'''Set up arguments for command line interface.'''
parser = argparse.ArgumentParser()

parser.add_argument('--username', help='Username', required=True)
parser.add_argument('--password', help='Password', required=True)
parser.add_argument('--mode', help='Output Alarm Mode',
                    required=False, default=False, action="store_true")
parser.add_argument('--arm', help='Arm Alarm To Mode', required=False)
parser.add_argument('--devices', help='List All Devices',
                    required=False, default=False, action="store_true")
parser.add_argument('--device', help='Get Device', required=False, action='append')
parser.add_argument('--listen', help='Listen For Device Updates',
                    required=False, default=False, action="store_true")
parser.add_argument('--debug', help='Output Debugging',
                    required=False, default=False, action="store_true")

args = vars(parser.parse_args())

'''Validate arm mode.'''
if args['arm'] is not None:
    args['arm'] = args['arm'].lower()
    if args['arm'] not in ALL_MODES:
        sys.exit("Arm mode must be one of %s" % ALL_MODES_STR)

'''Create abodepy instance.'''
abode = abodepy.Abode(username=args['username'], password=args['password'], debug=args['debug'])

'''Output current mode.'''
if args['mode']:
    print("Mode: %s" % abode.get_alarm().get_mode())

'''Change system mode.'''
if args['arm']:
    print("Mode set to: %s" % abode.get_alarm().set_mode(args['arm']))

def _device_print(device, append=''):
    print("Device Name: %s, Device ID: %s, Device Type: %s, Device Status: %s%s" % (device.get_name(), device.get_device_id(), device.get_type(), device.get_status(), append))
    
'''Print out all devices.'''
if args['devices']:
    for device in abode.get_devices():
        _device_print(device)

'''Print out specific devices by device id.'''
if args['device']:
    for device_id in args['device']:
        device = abode.get_device(device_id)

        if device:
            _device_print(device)
            
            '''Register the specific devices if we decide to listen.'''
            abode.register(device, _device_callback)
        else:
            print("Could not find device with id: %s" % device_id)

def _device_callback(device):
    _device_print(device, time.strftime("%Y-%m-%d %H:%M:%S"))

'''Start device change listener.'''
if args['listen']:
    '''If no devices were specified then we listen to all devices.'''
    if args['device'] is None:
        print("No devices specified, adding all devices to listener...")
        
        for device in abode.get_devices():
            abode.register(device, _device_callback)
    
    print("Listening for device updates...")
    abode.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        abode.stop()
        print("Device update listening stopped.")
        pass

abode.logout()
