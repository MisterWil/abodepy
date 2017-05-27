import argparse
import time

from abode import AbodeController

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

if args['arm'] is not None:
    args['arm'] = args['arm'].lower()
    if args['arm'] not in ('standby', 'away', 'home'):
        sys.exit("Arm mode must be one of 'standby', 'away', or 'home'.")

a = AbodeController(args['username'], args['password'], True, args['debug'])
    
if args['mode']:
    print("Mode: %s" % a.get_alarm().get_mode())

if args['arm']:
    print("Mode set to: %s" % a.get_alarm().set_mode(args['arm']))

if args['devices']:
    for device in a.get_devices():
        print("Device Name: %s, Device ID: %s, Device Type: %s, Device Status: %s" % (device.get_name(), device.get_device_id(), device.get_type(), device.get_status()))

if args['device']:
    for device_id in args['device']:
        device = a.get_device(device_id)

        if device:
            print("Device Name: %s, Device ID: %s, Device Type: %s, Device Status: %s" % (device.get_name(), device.get_device_id(), device.get_type(), device.get_status()))

            a.register(device, _device_callback)
        else:
            print("Could not find device with id: %s" % device_id)

def _device_callback(device):
    print("Device Name: %s, Device ID: %s, Status: %s, At: %s" % (device.name, device.get_device_id(), device.get_status(), time.strftime("%Y-%m-%d %H:%M:%S")))
    
if args['listen']:
    if args['device'] is  None:
        print("No devices specified, adding all devices to listener...")
        
        for device in a.get_devices():
            a.register(device, _device_callback)
    
    print("Listening for device updates...")
    a.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        a.stop()
        print("Device update listening stopped.")
        pass

a.logout()
